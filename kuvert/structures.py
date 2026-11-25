"""The types kuvert sends by id, each expanded by the ``Kuvert`` client.

Imported by ``kuvert/__init__``: an app using ``Kuvert`` takes every one of them.
"""

from arkitekt_spec.declare.structures.declare import structure
from arkitekt_spec.declare.widgets import SearchWidget

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


def _search(query: object) -> SearchWidget:
    """The widget that picks one of these out of the deployment."""
    return SearchWidget(query=query.Meta.document, ward="kuvert")  # type: ignore[attr-defined]


# The three the server announces as signals (kuvert_server/service.py): their
# identifiers are a wire contract with it, spelled exactly as it spells them.


@structure("@kuvert/message", widget=_search(SearchMessagesQuery))
async def expand_message(id: str, kuvert: Kuvert) -> Message:
    """A message, by id."""
    return await kuvert.aget_message(id)


@structure("@kuvert/thread", widget=_search(SearchThreadsQuery))
async def expand_thread(id: str, kuvert: Kuvert) -> Thread:
    """A conversation, by id."""
    return await kuvert.aget_thread(id)


@structure("@kuvert/outgoingmessage")
async def expand_outgoing_message(id: str, kuvert: Kuvert) -> OutgoingMessage:
    """Mail sent (or being sent) from a mailbox, by id. The outbox has no search: no widget."""
    return await kuvert.aget_outgoing_message(id)


@structure("@kuvert/mailaccount", widget=_search(SearchMailAccountsQuery))
async def expand_mail_account(id: str, kuvert: Kuvert) -> DetailMailAccount:
    """A linked mailbox, by id."""
    return await kuvert.aget_mail_account(id)


@structure("@kuvert/task", widget=_search(SearchTasksQuery))
async def expand_task(id: str, kuvert: Kuvert) -> Task:
    """A task, by id."""
    return await kuvert.aget_task(id)


@structure("@kuvert/tasklist", widget=_search(SearchTaskListsQuery))
async def expand_task_list(id: str, kuvert: Kuvert) -> TaskList:
    """A task list, by id."""
    return await kuvert.aget_task_list(id)
