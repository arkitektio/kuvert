"""A plain import declares the client and the types it sends by id."""

from arkitekt_spec.declare.client import client_of

from kuvert import Kuvert


def test_kuvert_declares_its_client_and_structures() -> None:
    declaration = client_of(Kuvert)
    assert declaration is not None and declaration.name == "kuvert"
    assert {s.identifier for s in declaration.structures} == {
        "@kuvert/message",
        "@kuvert/thread",
        "@kuvert/outgoingmessage",
        "@kuvert/mailaccount",
        "@kuvert/task",
        "@kuvert/tasklist",
    }
