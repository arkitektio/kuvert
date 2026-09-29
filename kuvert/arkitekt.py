"""The kuvert service of an arkitekt app, and the types it sends by id.

Declared on one registry: the service first, then the structures whose expanders
ask for the client it returns. An app takes all of it in with
``App(services=[kuvert_service])``.
"""

import os
from typing import Annotated

from fakts import Alias, Require, TokenLoader
from fakts.contrib.rath.auth import FaktsAuthLink
from rath.links.aiohttp import AIOHttpLink
from rath.links.compose import compose
from rath.links.graphql_ws import GraphQLWSLink
from rath.links.split import SplitLink
from rekuest.app import AppRegistry
from rekuest.widgets import SearchWidget

from graphql import OperationType
from kuvert.api.schema import (
    DetailMailAccount,
    Message,
    OutgoingMessage,
    SearchMailAccountsQuery,
    SearchMessagesQuery,
    SearchTaskListsQuery,
    SearchTasksQuery,
    SearchThreadsQuery,
    Task,
    TaskList,
    Thread,
)
from kuvert.kuvert import Kuvert
from kuvert.rath import KuvertRath


def build_relative_path(*path: str) -> str:
    """Build a path relative to this file, for the files shipped beside it."""
    return os.path.join(os.path.dirname(__file__), *path)


registry = AppRegistry()
"""What kuvert brings to an app: its service, and the types it can send by id."""


@registry.service(
    schema=build_relative_path("api", "schema.graphql"),
    turms=build_relative_path("api", "project.json"),
)
def kuvert(
    kuvert: Annotated[
        Alias,
        Require(
            "live.arkitekt.kuvert",
            "Where the linked mailboxes and their mail are served",
        ),
    ],
    tokens: TokenLoader,
) -> Kuvert:
    """Kuvert: linked mailboxes, their conversations, tasks over them, and sending mail."""
    return Kuvert(
        rath=KuvertRath(
            link=compose(
                FaktsAuthLink(token_loader=tokens),
                SplitLink(
                    left=AIOHttpLink(
                        endpoint_url=kuvert.to_http_path("graphql"),
                        proxy=kuvert.proxy,
                    ),
                    right=GraphQLWSLink(
                        ws_endpoint_url=kuvert.to_ws_path("graphql"),
                        proxy=kuvert.proxy,
                    ),
                    split=lambda o: o.node.operation != OperationType.SUBSCRIPTION,
                ),
            ),
        ),
    )


def _search(query: object) -> SearchWidget:
    """The widget that picks one of these out of the deployment."""
    return SearchWidget(query=query.Meta.document, ward="kuvert")  # type: ignore[attr-defined]


# The three the server announces as signals (kuvert_server/service.py): their
# identifiers are a wire contract with it, spelled exactly as it spells them.


@registry.structure("@kuvert/message", widget=_search(SearchMessagesQuery))
async def expand_message(id: str, kuvert: Kuvert) -> Message:
    """A message, by id."""
    return await kuvert.aget_message(id)


@registry.structure("@kuvert/thread", widget=_search(SearchThreadsQuery))
async def expand_thread(id: str, kuvert: Kuvert) -> Thread:
    """A conversation, by id."""
    return await kuvert.aget_thread(id)


@registry.structure("@kuvert/outgoingmessage")
async def expand_outgoing_message(id: str, kuvert: Kuvert) -> OutgoingMessage:
    """Mail sent (or being sent) from a mailbox, by id. The outbox has no search: no widget."""
    return await kuvert.aget_outgoing_message(id)


@registry.structure("@kuvert/mailaccount", widget=_search(SearchMailAccountsQuery))
async def expand_mail_account(id: str, kuvert: Kuvert) -> DetailMailAccount:
    """A linked mailbox, by id."""
    return await kuvert.aget_mail_account(id)


@registry.structure("@kuvert/task", widget=_search(SearchTasksQuery))
async def expand_task(id: str, kuvert: Kuvert) -> Task:
    """A task, by id."""
    return await kuvert.aget_task(id)


@registry.structure("@kuvert/tasklist", widget=_search(SearchTaskListsQuery))
async def expand_task_list(id: str, kuvert: Kuvert) -> TaskList:
    """A task list, by id."""
    return await kuvert.aget_task_list(id)
