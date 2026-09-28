import base64
import json
import os
import smtplib
import socket
import sys
import urllib.request
import uuid
from collections.abc import Generator
from dataclasses import dataclass
from email.message import EmailMessage
from typing import ClassVar

import pytest
from dokker import Deployment, testing
from dokker.log_watcher import LogWatcher
from rath.links.aiohttp import AIOHttpLink
from rath.links.auth import ComposedAuthLink
from rath.links.compose import compose
from rath.links.graphql_ws import GraphQLWSLink
from rath.links.timeout import TimeoutLink

from graphql import OperationType
from kuvert.kuvert import Kuvert
from kuvert.rath import (
    KuvertRath,
    SplitLink,
)


def pytest_configure(config: pytest.Config) -> None:
    """Register custom platform markers."""
    config.addinivalue_line("markers", "linux_only: skip on non-Linux platforms")
    config.addinivalue_line("markers", "no_windows: skip on Windows")


def pytest_collection_modifyitems(config: pytest.Config, items: list) -> None:
    """Skip tests marked linux_only or no_windows on the wrong platform."""
    for item in items:
        if item.get_closest_marker("linux_only") and sys.platform != "linux":
            item.add_marker(pytest.mark.skip(reason="Linux only"))
        if item.get_closest_marker("no_windows") and sys.platform == "win32":
            item.add_marker(pytest.mark.skip(reason="Not supported on Windows"))


project_path = os.path.join(os.path.dirname(__file__), "integration")
docker_compose_file = os.path.join(project_path, "docker-compose.yml")
#: Optional, gitignored: mounts a local kuvert-server checkout over the image's
#: /workspace, so the suite can test server changes that are not published yet.
#: See tests/integration/docker-compose.local.yml.
local_override_file = os.path.join(project_path, "docker-compose.local.yml")
compose_files = [docker_compose_file] + (
    [local_override_file] if os.path.exists(local_override_file) else []
)


def _reserve_free_ports(count: int) -> list[int]:
    """Ask the OS for `count` distinct free TCP ports.

    All sockets are held open until every port has been assigned, so the kernel
    cannot hand out the same port twice within one call. They are released
    before compose binds them -- a race in theory, but the ephemeral range is
    large and this is what keeps concurrent runs (and the leftovers of a crashed
    one) from colliding on a fixed port.
    """
    sockets: list[socket.socket] = []
    try:
        for _ in range(count):
            sock = socket.socket()
            sock.bind(("127.0.0.1", 0))
            sockets.append(sock)
        return [int(sock.getsockname()[1]) for sock in sockets]
    finally:
        for sock in sockets:
            sock.close()


@pytest.fixture(scope="session")
def integration_ports() -> Generator[dict[str, int], None, None]:
    """Pick this run's host ports and point compose at them.

    Reserved rather than left to docker (`ports: - "80"`) because
    `Deployment.spec` is rendered by `docker compose config`, which is static:
    an unpublished port reads back as ``None`` and the test URLs would quietly
    become ``http://localhost:None`` instead of failing loudly.
    """
    kuvert_port, mail_api_port, mail_smtp_port = _reserve_free_ports(3)
    env = {
        "KUVERT_HOST_PORT": str(kuvert_port),
        "MAIL_API_HOST_PORT": str(mail_api_port),
        "MAIL_SMTP_HOST_PORT": str(mail_smtp_port),
    }
    previous = {key: os.environ.get(key) for key in env}
    os.environ.update(env)
    try:
        yield {
            "kuvert": kuvert_port,
            "mail_api": mail_api_port,
            "mail_smtp": mail_smtp_port,
        }
    finally:
        for key, value in previous.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def _write_fernet_key() -> None:
    """A fresh Fernet key for this run, where the stack mounts ``/secrets``.

    kuvert encrypts mailbox passwords with it. Generated rather than committed: a
    key in the repository is a key anyone can read. (A Fernet key is 32 random
    bytes, urlsafe-base64 encoded; no cryptography dependency needed for that.)
    """
    secrets_dir = os.path.join(project_path, "secrets")
    os.makedirs(secrets_dir, exist_ok=True)
    with open(os.path.join(secrets_dir, "kuvert.fernet"), "w") as f:
        f.write(base64.urlsafe_b64encode(os.urandom(32)).decode() + "\n")


async def token_loader() -> str:
    """The static token configured in tests/integration/configs/kuvert.yaml."""
    return "test"


@dataclass
class DeployedKuvert:
    """Deployed Kuvert instance."""

    deployment: Deployment
    kuvert_watcher: LogWatcher
    kuvert: Kuvert
    mail_api_url: str
    mail_smtp_port: int


@pytest.fixture(scope="session")
def deployed_app(
    integration_ports: dict[str, int],
) -> Generator[DeployedKuvert, None, None]:
    """kuvert, its database and a real mail server (GreenMail), via Docker Compose."""
    # testing(): a per-run `dokker-test-<hash>` project that is torn down on
    # exit, so concurrent or crashed runs (and sibling repos, which all name
    # their stack `integration`) never share containers.
    setup = testing(compose_files)
    setup.add_health_check(
        url=lambda spec: (
            f"http://localhost:{spec.find_service('kuvert').get_port_for_internal(80).published}/graphql"
        ),
        service="kuvert",
        timeout=5,
        # dokker sleeps `timeout` seconds between attempts: 20 x 5 s covers a
        # cold backend on a two-core runner, where 10 did not.
        max_retries=20,
    )

    watcher = setup.create_watcher("kuvert")
    _write_fernet_key()

    with setup:
        setup.down()
        try:
            setup.pull()
        except Exception as error:  # noqa: BLE001 -- best effort, see below
            # Best effort: Docker Hub rate-limits anonymous pulls, and failing the
            # whole suite over a refreshed tag when every image is already on the
            # machine is worse than running with what we have. A genuinely missing
            # image still fails loudly, at `up`.
            print(f"Could not refresh the images, using the local ones: {error}")
        setup.inspect()

        http_url = f"http://localhost:{setup.spec.find_service('kuvert').get_port_for_internal(80).published}/graphql"
        ws_url = f"ws://localhost:{setup.spec.find_service('kuvert').get_port_for_internal(80).published}/graphql"

        print(f"HTTP URL: {http_url}")
        print(f"WS URL: {ws_url}")

        y = KuvertRath(
            link=compose(
                TimeoutLink(timeout=12),
                ComposedAuthLink(
                    token_loader=token_loader, token_refresher=token_loader
                ),
                SplitLink(
                    left=AIOHttpLink(endpoint_url=http_url),
                    right=GraphQLWSLink(ws_endpoint_url=ws_url),
                    split=lambda o: o.node.operation != OperationType.SUBSCRIPTION,
                ),
            ),
        )

        kuvert = Kuvert(rath=y)

        setup.up()

        setup.check_health()

        with kuvert as kuvert:
            deployed = DeployedKuvert(
                deployment=setup,
                kuvert_watcher=watcher,
                kuvert=kuvert,
                mail_api_url=f"http://localhost:{integration_ports['mail_api']}",
                mail_smtp_port=integration_ports["mail_smtp"],
            )

            yield deployed


@pytest.fixture(scope="session")
def kuvert(deployed_app: DeployedKuvert) -> Kuvert:
    """The deployment's client: API calls are its methods, nothing is ambient."""
    return deployed_app.kuvert


class GreenMail:
    """The stack's mail server, driven from the host: users over its REST API, mail over SMTP."""

    #: Where kuvert (inside the stack) reaches it: TLS ports, self-signed certificate.
    IMAP: ClassVar[dict[str, object]] = {
        "host": "mail",
        "port": 3993,
        "security": "TLS",
    }
    SMTP: ClassVar[dict[str, object]] = {
        "host": "mail",
        "port": 3465,
        "security": "TLS",
    }

    def __init__(self, api_url: str, smtp_port: int) -> None:
        self.api_url = api_url
        self.smtp_port = smtp_port

    def wait_ready(self, timeout: float = 120) -> None:
        import time

        deadline = time.monotonic() + timeout
        while True:
            try:
                urllib.request.urlopen(
                    f"{self.api_url}/api/service/readiness", timeout=2
                ).read()
                return
            except Exception:
                if time.monotonic() > deadline:
                    raise
                time.sleep(1)

    def user(self, password: str = "secret") -> str:
        """A fresh mailbox on the server; its address is also its login."""
        address = f"u{uuid.uuid4().hex[:10]}@kuvert.test"
        request = urllib.request.Request(
            f"{self.api_url}/api/user",
            data=json.dumps(
                {"email": address, "login": address, "password": password}
            ).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        urllib.request.urlopen(request, timeout=10).read()
        return address

    def deliver(
        self,
        to: str,
        subject: str,
        body: str = "hello",
        sender: str = "someone@elsewhere.test",
    ) -> None:
        """Mail arriving from outside, straight into ``to``'s INBOX."""
        message = EmailMessage()
        message["From"] = sender
        message["To"] = to
        message["Subject"] = subject
        message["Message-ID"] = f"<{uuid.uuid4().hex}@elsewhere.test>"
        message.set_content(body)
        with smtplib.SMTP(
            "localhost", self.smtp_port, timeout=10, local_hostname="kuvert.test"
        ) as smtp:
            smtp.send_message(message)


@pytest.fixture(scope="session")
def greenmail(deployed_app: DeployedKuvert) -> GreenMail:
    """The mail server kuvert syncs from and sends through."""
    mail = GreenMail(deployed_app.mail_api_url, deployed_app.mail_smtp_port)
    mail.wait_ready()
    return mail
