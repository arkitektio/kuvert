# kuvert

The python client for [kuvert](https://github.com/arkitektio/kuvert-server), the
[Arkitekt](https://arkitekt.live) mail service: the mailboxes you linked, their
folders and conversations, tasks over those conversations, and sending mail.

## Installation

```sh
pip install kuvert
```

## Usage

Every kuvert operation is a method of the `Kuvert` client, in a blocking and an
`a`-prefixed async flavour.

### In an arkitekt app

The client is injected by annotation. Add the service to your app and ask for
`kuvert: Kuvert`:

```python
from arkitekt import App, run
from kuvert import Kuvert, kuvert_service

app = App("mail-digest", "0.1.0", services=[kuvert_service])


@app.action
async def unread_subjects(kuvert: Kuvert) -> list[str]:
    """The subjects of the unread conversations in my inboxes."""
    threads = await kuvert.alist_threads(filter={"unread": True, "folderRole": "INBOX"})
    return [thread.subject for thread in threads]


if __name__ == "__main__":
    run(app)
```

Messages, threads, outgoing mail, mailboxes, tasks and task lists travel between
actions by id (`@kuvert/message`, `@kuvert/thread`, `@kuvert/outgoingmessage`,
`@kuvert/mailaccount`, `@kuvert/task`, `@kuvert/tasklist`), so an action can take
and return them directly, and a trigger on a kuvert signal hands them over.

### From a script

```python
from arkitekt import easy
from kuvert import kuvert_service

with easy("my-script", kuvert_service) as kuvert:
    for account in kuvert.list_mail_accounts():
        print(account.email_address, account.unread_count)
```

### Standalone

Without arkitekt, build the client over a rath link of your own:

```python
from kuvert import Kuvert
from kuvert.rath import KuvertRath

kuvert = Kuvert(rath=KuvertRath(link=...))

with kuvert:
    for account in kuvert.list_mail_accounts():
        print(account.email_address, account.unread_count)

    kuvert.send_message(
        account=account.id,
        to=[{"address": "someone@example.org"}],
        subject="Hello",
        text="From kuvert.",
    )
```

Arguments the server defaults (`cc`, `bcc`, `attachments` of `send_message`,
`notes`/`pinned` of `create_task`, …) are optional: **leave them out** rather
than passing `None`. An explicit `None` is sent as `null`, which the server
rejects for those fields.

Changes to mail (flags, moves, deletes, categories) are local-first: they apply
at once and reach the mail server when the mailbox next pushes.
`list_mail_changes` shows what is still pending and `undo_mail_changes` takes a
change back while it is.

## Development

The generated API (`kuvert/api/schema.py`) comes from the checked-in
`schema.graphql` and the documents in `graphql/`. The config comment in
`graphql.config.yaml` has the command that refreshes the schema from a
kuvert-server checkout. Then run turms to regenerate the API.

```sh
uv run pytest -m "not integration"   # no server needed
uv run pytest -m integration          # a real kuvert + mail server via dokker
```

See [RELEASING.md](RELEASING.md) for how versions are cut.
