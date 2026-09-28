"""Tasks over conversations, against a real kuvert."""

import pytest

from kuvert.api.schema import (
    TaskFilter,
    TaskLinkSource,
    TaskStatus,
    ThreadFilter,
    ThreadLinkInput,
)
from kuvert.kuvert import Kuvert

from .conftest import GreenMail
from .test_mail import link, sync_all


@pytest.mark.integration
def test_task_lists_hold_tasks(kuvert: Kuvert) -> None:
    task_list = kuvert.create_task_list(name="Errands")
    task = kuvert.create_task(title="Renew passport", task_list=task_list.id)

    assert task.list is not None and task.list.id == task_list.id
    assert kuvert.get_task_list(id=task_list.id).open_count == 1
    assert [t.id for t in kuvert.list_tasks(filter=TaskFilter(list=task_list.id))] == [
        task.id
    ]
    assert task_list.id in {o.value for o in kuvert.search_task_lists(search="Errands")}


@pytest.mark.integration
def test_a_task_needs_only_a_title(kuvert: Kuvert) -> None:
    """Notes, pin and threads are the server's defaults when left out."""
    task = kuvert.create_task(title="Call the plumber")

    assert task.status == TaskStatus.OPEN
    assert task.notes == ""
    assert not task.pinned
    assert task.id in {o.value for o in kuvert.search_tasks(search="plumber")}


@pytest.mark.integration
def test_tasks_link_threads(kuvert: Kuvert, greenmail: GreenMail) -> None:
    account = link(kuvert, greenmail)
    greenmail.deliver(account.email_address, "Contract draft")
    sync_all(kuvert, account.id)
    (thread,) = kuvert.list_threads(filter=ThreadFilter(account=account.id))

    task = kuvert.create_task(title="Review the contract")
    (linked,) = kuvert.link_threads(
        task_id=task.id,
        threads=[thread.id],
        link=ThreadLinkInput(
            source=TaskLinkSource.APP, confidence=0.9, reason="mentions a contract"
        ),
    )
    assert linked.thread.id == thread.id
    assert linked.source == TaskLinkSource.APP

    fetched = kuvert.get_task(id=task.id)
    assert [t.id for t in fetched.threads] == [thread.id]
    assert [t.id for t in kuvert.list_threads(filter=ThreadFilter(task=task.id))] == [
        thread.id
    ]

    assert kuvert.unlink_threads(task_id=task.id, threads=[thread.id]).thread_count == 0


@pytest.mark.integration
def test_upsert_is_keyed_by_external_key(kuvert: Kuvert) -> None:
    """An app's own task id: the second upsert updates the first task."""
    first = kuvert.upsert_task(external_key="ticket-17", title="Ticket 17")
    second = kuvert.upsert_task(external_key="ticket-17", title="Ticket 17 (reopened)")

    assert second.id == first.id
    assert second.title == "Ticket 17 (reopened)"


@pytest.mark.integration
def test_finish_and_delete_tasks(kuvert: Kuvert) -> None:
    task = kuvert.create_task(title="Water the plants")

    (done,) = kuvert.set_task_status(tasks=[task.id], status=TaskStatus.DONE)
    assert done.status == TaskStatus.DONE
    assert done.completed_at is not None

    assert kuvert.delete_task(id=task.id) == task.id
    assert task.id not in {t.id for t in kuvert.list_tasks()}
