"""Lightweight initialization tests that need no deployed stack.

These run on every OS in the CI matrix (they carry no ``integration`` marker),
exercising pure-Python construction of the client and the generated schema
models without touching the network or Docker.
"""

import inspect

from kuvert.api.schema import (
    FolderRole,
    MessageFilter,
    MessageOrderDate,
    OffsetPaginationInput,
    Ordering,
    RecipientInput,
    ThreadFilter,
)
from kuvert.kuvert import Kuvert


def test_kuvert_importable() -> None:
    """The top-level ``Kuvert`` composition imports and is a class."""
    assert isinstance(Kuvert, type)


def test_offset_pagination_input_constructs() -> None:
    pagination = OffsetPaginationInput(offset=0, limit=10)
    assert pagination.offset == 0
    assert pagination.limit == 10


def test_message_order_uses_enum() -> None:
    """``MessageOrderDate`` (a ``MessageOrder`` @oneOf variant) serialises via its alias."""
    order = MessageOrderDate(date=Ordering.DESC)
    assert order.model_dump(by_alias=True, exclude_none=True) == {"date": "DESC"}


def test_filters_speak_the_wire_names() -> None:
    """Python names in, GraphQL names out."""
    dumped = ThreadFilter(
        folder_role=FolderRole.INBOX, has_attachments=True
    ).model_dump(by_alias=True, exclude_none=True)
    assert dumped == {"folderRole": "INBOX", "hasAttachments": True}
    assert MessageFilter().model_dump(exclude_none=True) == {}


def test_recipient_needs_only_an_address() -> None:
    assert RecipientInput(address="a@example.org").model_dump(
        by_alias=True, exclude_none=True
    ) == {"address": "a@example.org"}


def test_defaulted_input_fields_are_optional_keywords() -> None:
    """What the server defaults, the caller may leave out.

    turms makes a non-null input field required even when the server defaults it,
    so these mutations spell their variables out (see graphql.config.yaml).
    """
    for method, required in {
        Kuvert.send_message: {"account"},
        Kuvert.create_task: {"title"},
        Kuvert.set_message_flags: {"messages"},
        Kuvert.categorize_messages: {"messages"},
        Kuvert.delete_messages: {"messages"},
        Kuvert.create_mail_account: {"email_address", "password"},
        Kuvert.create_category: {"account", "name"},
    }.items():
        parameters = inspect.signature(method).parameters.values()
        assert {p.name for p in parameters if p.default is inspect.Parameter.empty} - {
            "self"
        } == required, method


def test_no_operation_hides_the_task_kwarg() -> None:
    """``task=`` is the rekuest task a call is attributed to, on every method.

    A kuvert task travels as ``task_id``; nothing else may be called ``task``.
    """
    for name in ("link_threads", "unlink_threads"):
        parameters = inspect.signature(getattr(Kuvert, name)).parameters
        assert "task_id" in parameters
        assert str(parameters["task"].annotation).endswith("TaskLike | None")
