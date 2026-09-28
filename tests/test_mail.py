"""Mailboxes, their mail, and changes to it, against a real kuvert and a real mail server."""

import pytest

from kuvert.api.schema import (
    DetailMailAccount,
    FolderRole,
    MailAccountStatus,
    MessageFilter,
    OutgoingStatus,
    Protocol,
    RecipientInput,
    ServerInput,
    ThreadFilter,
)
from kuvert.kuvert import Kuvert

from .conftest import GreenMail


def link(
    kuvert: Kuvert, greenmail: GreenMail, address: str | None = None
) -> DetailMailAccount:
    """A GreenMail mailbox, linked with its password."""
    address = address or greenmail.user()
    return kuvert.create_mail_account(
        email_address=address,
        password="secret",
        protocol=Protocol.IMAP,
        incoming=ServerInput(**GreenMail.IMAP),
        smtp=ServerInput(**GreenMail.SMTP),
    )


def sync_all(kuvert: Kuvert, account_id: str) -> None:
    """Sync until the server says there is nothing more to fetch."""
    for _ in range(10):
        if not kuvert.sync_mail_account(id=account_id).more:
            return
    raise AssertionError("the mailbox never finished syncing")


@pytest.mark.integration
def test_link_a_mailbox(kuvert: Kuvert, greenmail: GreenMail) -> None:
    """A mailbox linked with its password is tested, stored and listed."""
    account = link(kuvert, greenmail)

    assert account.status == MailAccountStatus.ACTIVE
    assert account.is_owner
    assert account.id in {a.id for a in kuvert.list_mail_accounts()}
    assert kuvert.get_mail_account(id=account.id).email_address == account.email_address


@pytest.mark.integration
def test_a_wrong_password_links_nothing(kuvert: Kuvert, greenmail: GreenMail) -> None:
    address = greenmail.user()
    before = {a.id for a in kuvert.list_mail_accounts()}

    with pytest.raises(Exception, match="AUTH_FAILED"):
        kuvert.create_mail_account(
            email_address=address,
            password="wrong",
            incoming=ServerInput(**GreenMail.IMAP),
            smtp=ServerInput(**GreenMail.SMTP),
        )

    assert {a.id for a in kuvert.list_mail_accounts()} == before


@pytest.mark.integration
def test_sync_brings_in_mail_as_threads(kuvert: Kuvert, greenmail: GreenMail) -> None:
    account = link(kuvert, greenmail)
    greenmail.deliver(account.email_address, "Quarterly numbers")
    greenmail.deliver(account.email_address, "Lunch?")

    sync_all(kuvert, account.id)

    threads = kuvert.list_threads(
        filter=ThreadFilter(account=account.id, folder_role=FolderRole.INBOX)
    )
    # A thread's subject is normalised (lowercased, no Re:/Fwd:); its messages keep theirs.
    assert {t.latest_message.subject for t in threads if t.latest_message} == {
        "Quarterly numbers",
        "Lunch?",
    }
    assert (
        kuvert.count_threads(filter=ThreadFilter(account=account.id, unread=True)) == 2
    )

    thread = kuvert.get_thread(id=next(t.id for t in threads if t.subject == "lunch?"))
    assert [m.subject for m in thread.messages] == ["Lunch?"]

    message = kuvert.get_message(id=thread.messages[0].id)
    assert message.sender.address == "someone@elsewhere.test"
    assert "hello" in message.text_body


@pytest.mark.integration
def test_search_widgets_find_by_text_and_by_id(
    kuvert: Kuvert, greenmail: GreenMail
) -> None:
    """The Search* queries the structures' widgets run."""
    account = link(kuvert, greenmail)
    greenmail.deliver(account.email_address, "Invoice 4711")
    sync_all(kuvert, account.id)

    found = kuvert.search_threads(search="Invoice 4711")
    assert [o.label for o in found] == ["invoice 4711"]
    assert [o.value for o in kuvert.search_threads(values=[found[0].value])] == [
        found[0].value
    ]
    assert account.id in {
        o.value for o in kuvert.search_mail_accounts(search=account.email_address)
    }


@pytest.mark.integration
def test_flags_and_reads_apply_at_once_and_push(
    kuvert: Kuvert, greenmail: GreenMail
) -> None:
    """Local-first: a change shows immediately and reaches the server on push."""
    account = link(kuvert, greenmail)
    greenmail.deliver(account.email_address, "Flag me")
    sync_all(kuvert, account.id)
    (message,) = kuvert.list_messages(filter=MessageFilter(account=account.id))

    (read,) = kuvert.mark_messages_read(messages=[message.id])
    assert read.is_read
    (flagged,) = kuvert.set_message_flags(messages=[message.id], add=["\\Flagged"])
    assert flagged.is_flagged

    result = kuvert.push_mail_changes(account=account.id)
    assert result.failed == 0
    assert result.pending == 0
    assert kuvert.list_mail_changes(filter={"account": account.id}) == ()


@pytest.mark.integration
def test_categories_tag_messages(kuvert: Kuvert, greenmail: GreenMail) -> None:
    account = link(kuvert, greenmail)
    greenmail.deliver(account.email_address, "Tag me")
    sync_all(kuvert, account.id)
    (message,) = kuvert.list_messages(filter=MessageFilter(account=account.id))

    category = kuvert.create_category(account=account.id, name="Receipts")
    (tagged,) = kuvert.categorize_messages(messages=[message.id], add=[category.id])

    assert [c.name for c in tagged.categories] == ["Receipts"]
    assert kuvert.get_category(id=category.id).message_count == 1

    kuvert.delete_category(id=category.id)
    assert category.id not in {c.id for c in kuvert.list_categories()}


@pytest.mark.integration
def test_send_mail_to_another_mailbox(kuvert: Kuvert, greenmail: GreenMail) -> None:
    """Sent through the mailbox's own SMTP server, and arriving in the other one."""
    sender = link(kuvert, greenmail)
    recipient = link(kuvert, greenmail)

    # Only what is needed: every other input the server defaults.
    outgoing = kuvert.send_message(
        account=sender.id,
        to=[RecipientInput(address=recipient.email_address)],
        subject="Hi from kuvert",
        text="Sent by the client library.",
    )

    assert outgoing.status == OutgoingStatus.SENT
    assert kuvert.get_outgoing_message(id=outgoing.id).subject == "Hi from kuvert"

    sync_all(kuvert, recipient.id)
    subjects = {
        t.subject
        for t in kuvert.list_threads(filter=ThreadFilter(account=recipient.id))
    }
    assert "hi from kuvert" in subjects


@pytest.mark.integration
def test_unlink_a_mailbox(kuvert: Kuvert, greenmail: GreenMail) -> None:
    account = link(kuvert, greenmail)

    assert kuvert.delete_mail_account(id=account.id) == account.id
    assert account.id not in {a.id for a in kuvert.list_mail_accounts()}


@pytest.mark.integration
async def test_the_async_twins(kuvert: Kuvert, greenmail: GreenMail) -> None:
    """Every call has an ``a``-prefixed coroutine twin."""
    account = link(kuvert, greenmail)
    greenmail.deliver(account.email_address, "Async hello")
    await kuvert.async_mail_account(id=account.id)

    threads = await kuvert.alist_threads(filter=ThreadFilter(account=account.id))
    assert [t.subject for t in threads] == ["async hello"]
    assert (await kuvert.aget_thread(id=threads[0].id)).id == threads[0].id
