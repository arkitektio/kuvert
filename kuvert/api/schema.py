import builtins
from datetime import datetime
from enum import Enum
from pydantic import AliasChoices, BaseModel, ConfigDict, Field
from rath.scalars import ID, IDCoercible
from rath.task import TaskLike
from typing import Annotated, Any, AsyncIterator, ClassVar, Iterable, Iterator, Literal

class GraphQLDefault:
    """Records a GraphQL field schema default value. The client omits the field so the server applies its own default; this preserves the value for introspection."""

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return 'GraphQLDefault(' + repr(self.value) + ')'

class UnsetType:
    """Sentinel for arguments the caller did not provide. Such fields are omitted on serialization so the GraphQL server applies its own default."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self):
        return 'UNSET'

    def __bool__(self):
        return False
UNSET = UnsetType()

class AuthFinish(str, Enum):
    """How a started login finishes."""
    REDIRECT = 'REDIRECT'
    POLL = 'POLL'
    __str__ = str.__str__

class AuthMethod(str, Enum):
    """How the service logs in. PASSWORD: Username and (app) password; XOAUTH2: OAuth 2.0 access token (SASL XOAUTH2)."""
    PASSWORD = 'PASSWORD'
    XOAUTH2 = 'XOAUTH2'
    __str__ = str.__str__

class AuthStatus(str, Enum):
    """Where a login is."""
    PENDING = 'PENDING'
    DONE = 'DONE'
    FAILED = 'FAILED'
    EXPIRED = 'EXPIRED'
    CANCELLED = 'CANCELLED'
    __str__ = str.__str__

class CategorySync(str, Enum):
    """Where a category lives. LOCAL: Only here; the server never sees it; KEYWORD: As an IMAP keyword on the server, so other mail clients see it."""
    LOCAL = 'LOCAL'
    KEYWORD = 'KEYWORD'
    __str__ = str.__str__

class DescriptorOperator(str, Enum):
    """How a descriptor constraint compares the object's value with the stated one. The operators a rekuest port's `requires` and `provides` are written in, with the same meaning."""
    EQUALS = 'EQUALS'
    MATCHES = 'MATCHES'
    NOT_EQUALS = 'NOT_EQUALS'
    GTE = 'GTE'
    LTE = 'LTE'
    EXISTS = 'EXISTS'
    CONTAINS = 'CONTAINS'
    IN = 'IN'
    NOT_IN = 'NOT_IN'
    __str__ = str.__str__

class FolderRole(str, Enum):
    """What a folder is for (IMAP SPECIAL-USE, else guessed from its name). INBOX: Incoming mail; SENT: Sent mail; DRAFTS: Drafts; TRASH: Deleted mail; ARCHIVE: Archived mail; JUNK: Spam; ALL: Every message (Gmail's All Mail); FLAGGED: A virtual folder of flagged mail; OTHER: A user folder."""
    INBOX = 'INBOX'
    SENT = 'SENT'
    DRAFTS = 'DRAFTS'
    TRASH = 'TRASH'
    ARCHIVE = 'ARCHIVE'
    JUNK = 'JUNK'
    ALL = 'ALL'
    FLAGGED = 'FLAGGED'
    OTHER = 'OTHER'
    __str__ = str.__str__

class MailAccountStatus(str, Enum):
    """Lifecycle of a linked mailbox. ACTIVE: Linked; syncs and sends; NEEDS_REAUTH: The credentials stopped working; update the password or link again; DISABLED: Paused by a user; neither synced nor used to send."""
    ACTIVE = 'ACTIVE'
    NEEDS_REAUTH = 'NEEDS_REAUTH'
    DISABLED = 'DISABLED'
    __str__ = str.__str__

class MailChangeKind(str, Enum):
    """What a queued change does on the server. FLAGS: Add and remove flags and keywords (STORE); MOVE: Move the message to another folder; EXPUNGE: Delete the message for good; POP_DELE: Delete the message on a POP3 server."""
    FLAGS = 'FLAGS'
    MOVE = 'MOVE'
    EXPUNGE = 'EXPUNGE'
    POP_DELE = 'POP_DELE'
    __str__ = str.__str__

class MailChangeState(str, Enum):
    """Where a queued change is (a pushed one is gone). PENDING: Waiting to be pushed (from `pushAfter` on); FAILED: The server refused it or it ran out of attempts; the local state stays."""
    PENDING = 'PENDING'
    FAILED = 'FAILED'
    __str__ = str.__str__

class MailErrorCode(str, Enum):
    """What went wrong, for a client to offer a fix. Also stored as ``last_error_code``. NOT_CONFIGURED: The organization or the service is not set up for this (no usable provider, the datalayer); AUTH_FAILED: The server refused the username or password; CONSENT_EXPIRED: The OAuth grant was revoked or ran out; link the mailbox again; CONNECTION_FAILED: The server could not be reached, or the connection broke; TLS_FAILED: The TLS handshake failed (certificate or protocol); TLS_REQUIRED: The mailbox asks for a connection without TLS, which is not allowed; HOST_NOT_ALLOWED: The host resolves to a private or internal address; SYNC_IN_PROGRESS: Another sync holds this mailbox right now; RATE_LIMITED: Synced too recently; try again later; SERVER_ERROR: The server answered a command with an error; SEND_REJECTED: The SMTP server refused the message or a recipient; UNSUPPORTED_BY_PROTOCOL: POP3 cannot do this (folders, flags on the server); MAILBOX_INACTIVE: The mailbox is disabled or needs new credentials; INVALID_STATE: The link state is unknown, used or belongs to someone else; CODE_EXPIRED: The link was not completed in time; PROVIDER_ERROR: The OAuth provider answered with an error; UNSUPPORTED_BY_POLICY: The mailbox is set not to change this on the server (its push settings); KEYWORDS_NOT_PERMITTED: The folder does not keep keywords (no \\\\* in PERMANENTFLAGS), the category stays local; MESSAGE_GONE: The message is no longer where the change expected it on the server; UNSAFE_EXPUNGE: Without UIDPLUS an expunge would also remove other deleted messages of the folder."""
    NOT_CONFIGURED = 'NOT_CONFIGURED'
    AUTH_FAILED = 'AUTH_FAILED'
    CONSENT_EXPIRED = 'CONSENT_EXPIRED'
    CONNECTION_FAILED = 'CONNECTION_FAILED'
    TLS_FAILED = 'TLS_FAILED'
    TLS_REQUIRED = 'TLS_REQUIRED'
    HOST_NOT_ALLOWED = 'HOST_NOT_ALLOWED'
    SYNC_IN_PROGRESS = 'SYNC_IN_PROGRESS'
    RATE_LIMITED = 'RATE_LIMITED'
    SERVER_ERROR = 'SERVER_ERROR'
    SEND_REJECTED = 'SEND_REJECTED'
    UNSUPPORTED_BY_PROTOCOL = 'UNSUPPORTED_BY_PROTOCOL'
    MAILBOX_INACTIVE = 'MAILBOX_INACTIVE'
    INVALID_STATE = 'INVALID_STATE'
    CODE_EXPIRED = 'CODE_EXPIRED'
    PROVIDER_ERROR = 'PROVIDER_ERROR'
    UNSUPPORTED_BY_POLICY = 'UNSUPPORTED_BY_POLICY'
    KEYWORDS_NOT_PERMITTED = 'KEYWORDS_NOT_PERMITTED'
    MESSAGE_GONE = 'MESSAGE_GONE'
    UNSAFE_EXPUNGE = 'UNSAFE_EXPUNGE'
    __str__ = str.__str__

class Ordering(str, Enum):
    """No documentation"""
    ASC = 'ASC'
    ASC_NULLS_FIRST = 'ASC_NULLS_FIRST'
    ASC_NULLS_LAST = 'ASC_NULLS_LAST'
    DESC = 'DESC'
    DESC_NULLS_FIRST = 'DESC_NULLS_FIRST'
    DESC_NULLS_LAST = 'DESC_NULLS_LAST'
    __str__ = str.__str__

class OutgoingStatus(str, Enum):
    """Where a sent message is. SENDING: Being handed to the SMTP server; SENT: Accepted by the SMTP server; FAILED: Refused or not delivered to the SMTP server."""
    SENDING = 'SENDING'
    SENT = 'SENT'
    FAILED = 'FAILED'
    __str__ = str.__str__

class Protocol(str, Enum):
    """How incoming mail is read. IMAP: IMAP: folders, flags and moves live on the server; POP3: POP3: one inbox, downloaded; flags are local."""
    IMAP = 'IMAP'
    POP3 = 'POP3'
    __str__ = str.__str__

class Provider(str, Enum):
    """Who hosts a mailbox (decides OAuth, presets and Sent-copy behaviour); also the kind of a :class:`MailProvider`. GENERIC: Any IMAP/POP3 server; GMAIL: Gmail / Google Workspace; MICROSOFT: Outlook.com / Microsoft 365."""
    GENERIC = 'GENERIC'
    GMAIL = 'GMAIL'
    MICROSOFT = 'MICROSOFT'
    __str__ = str.__str__

class ProviderCapability(str, Enum):
    """What a provider may be used for, beyond reading mail (which every one does). SEND: Send mail through its mailboxes' SMTP servers; SCHEDULED_SYNC: Let the unattended sync_all_mailboxes action sync its mailboxes."""
    SEND = 'SEND'
    SCHEDULED_SYNC = 'SCHEDULED_SYNC'
    __str__ = str.__str__

class Security(str, Enum):
    """Transport security of a connection. TLS: Implicit TLS (IMAPS 993, POP3S 995, SMTPS 465); STARTTLS: Plain connection upgraded with STARTTLS (IMAP 143, POP3 110, SMTP 587); NONE: No encryption (only when the deployment allows it)."""
    TLS = 'TLS'
    STARTTLS = 'STARTTLS'
    NONE = 'NONE'
    __str__ = str.__str__

class SyncState(str, Enum):
    """How a message here relates to the server. SYNCED: As the server has it; PENDING: Changed here, the change is on its way to the server; LOCAL: Changed here only (the mailbox does not push it, or it was deleted here only); FAILED: A change did not reach the server (see `changes`)."""
    SYNCED = 'SYNCED'
    PENDING = 'PENDING'
    LOCAL = 'LOCAL'
    FAILED = 'FAILED'
    __str__ = str.__str__

class TaskLinkSource(str, Enum):
    """Who put a thread into a task. USER: A person, by hand; APP: An app that sorts mail."""
    USER = 'USER'
    APP = 'APP'
    __str__ = str.__str__

class TaskStatus(str, Enum):
    """Where a task is. OPEN: To do; DONE: Done; DISMISSED: Dropped without doing it."""
    OPEN = 'OPEN'
    DONE = 'DONE'
    DISMISSED = 'DISMISSED'
    __str__ = str.__str__

class Visibility(str, Enum):
    """Who in the organization sees a mailbox and its mail. PRIVATE: Only the member who linked it; SHARED: The member who linked it and the members it is shared with; ORGANIZATION: Every member of the organization (a team mailbox)."""
    PRIVATE = 'PRIVATE'
    SHARED = 'SHARED'
    ORGANIZATION = 'ORGANIZATION'
    __str__ = str.__str__

class CategoryFilter(BaseModel):
    """A category of a mailbox, shared by everyone who sees the mailbox.

A KEYWORD category *is* its keyword: a message is in it when the keyword is among its flags,
so the membership reaches other mail clients and survives moves made there. A LOCAL
category's members are its assignments, kept under the message key."""
    and_: 'CategoryFilter | None' = Field(validation_alias=AliasChoices('and_', 'AND'), serialization_alias='AND', default=None)
    or_: 'CategoryFilter | None' = Field(validation_alias=AliasChoices('or_', 'OR'), serialization_alias='OR', default=None)
    not_: 'CategoryFilter | None' = Field(validation_alias=AliasChoices('not_', 'NOT'), serialization_alias='NOT', default=None)
    distinct: bool | None = Field(validation_alias=AliasChoices('distinct', 'DISTINCT'), serialization_alias='DISTINCT', default=None)
    account: ID | None = None
    sync: CategorySync | None = None
    search: str | None = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class CompleteAuthInput(BaseModel):
    """Finish (REDIRECT) or advance (POLL) a started login."""
    state: str
    code: str | None = Field(default=None, description='REDIRECT: the `code` query parameter of the redirect. POLL: omitted.')
    error: str | None = Field(default=None, description="REDIRECT: the provider's `error` / `error_description`, when it refused.")
    error_description: str | None = Field(validation_alias=AliasChoices('error_description', 'errorDescription'), serialization_alias='errorDescription', default=None)
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class CreateOAuthProviderInput(BaseModel):
    """A new Gmail or Microsoft provider: one OAuth client (a Google Cloud OAuth client, an Entra app registration)."""
    kind: Provider = Field(description='GMAIL or MICROSOFT.')
    name: str = Field(description='What to call it, unique in the organization.')
    client_id: str = Field(validation_alias=AliasChoices('client_id', 'clientId'), serialization_alias='clientId', description='The OAuth client id.')
    client_secret: str | None = Field(validation_alias=AliasChoices('client_secret', 'clientSecret'), serialization_alias='clientSecret', default=None, description='The client secret (a public client with PKCE has none). Stored encrypted and never returned.')
    redirect_urls: tuple[str, ...] = Field(validation_alias=AliasChoices('redirect_urls', 'redirectUrls'), serialization_alias='redirectUrls', description='The redirect URLs registered for the client, the default first.')
    tenant: str | None = Field(default=None, description='Microsoft: the Entra tenant (id or domain); `common` (any account) by default.')
    capabilities: tuple[ProviderCapability, ...] | None = Field(default=None, description='What to switch on; everything the kind can do by default (see `providerKinds`).')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class DescriptorConstraintInput(BaseModel):
    """One constraint on an object's descriptors, in the shape a rekuest port states its `requires` in -- so a picker hands a port's constraints on unchanged. `key` is one of the keys the structure declares (e.g. `@kuvert/has_attachments`); a key it does not declare is refused."""
    key: str = Field(description='The descriptor key, e.g. `@kuvert/has_attachments`')
    operator: DescriptorOperator = Field(description="How the object's value is compared with `value`. MATCHES is equality, as EQUALS is")
    value: Any | None = Field(default=None, description='The value compared against: a number for GTE and LTE, a list for IN and NOT_IN, true or false for EXISTS, the member looked for with CONTAINS')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class MailAccountFilter(BaseModel):
    """One linked mailbox: where it lives, how to log in, and how far it is synced.

``secret`` holds the password (PASSWORD) or the refresh token (XOAUTH2), and
``access_token`` the current OAuth access token -- both Fernet-encrypted
(:mod:`mail.crypto`), never exposed and never written to history rows."""
    and_: 'MailAccountFilter | None' = Field(validation_alias=AliasChoices('and_', 'AND'), serialization_alias='AND', default=None)
    or_: 'MailAccountFilter | None' = Field(validation_alias=AliasChoices('or_', 'OR'), serialization_alias='OR', default=None)
    not_: 'MailAccountFilter | None' = Field(validation_alias=AliasChoices('not_', 'NOT'), serialization_alias='NOT', default=None)
    distinct: bool | None = Field(validation_alias=AliasChoices('distinct', 'DISTINCT'), serialization_alias='DISTINCT', default=None)
    ids: tuple[ID, ...] | None = None
    status: MailAccountStatus | None = None
    search: str | None = None
    provider: ID | None = None
    mine: bool | None = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class MailChangeFilter(BaseModel):
    """A change made here that still has to reach the server (see :mod:`mail.push`).

``origin_*`` is where a MOVE or EXPUNGE finds the message on the server: the row itself has
already left (moved rows wait with a null UID, deleted ones carry ``deleted_at``). A FLAGS
change finds it through its row, and through ``message_key`` once sync replaced the row."""
    and_: 'MailChangeFilter | None' = Field(validation_alias=AliasChoices('and_', 'AND'), serialization_alias='AND', default=None)
    or_: 'MailChangeFilter | None' = Field(validation_alias=AliasChoices('or_', 'OR'), serialization_alias='OR', default=None)
    not_: 'MailChangeFilter | None' = Field(validation_alias=AliasChoices('not_', 'NOT'), serialization_alias='NOT', default=None)
    distinct: bool | None = Field(validation_alias=AliasChoices('distinct', 'DISTINCT'), serialization_alias='DISTINCT', default=None)
    account: ID | None = None
    state: MailChangeState | None = None
    kind: MailChangeKind | None = None
    message: ID | None = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class MailFolderFilter(BaseModel):
    """A folder (IMAP mailbox) of a linked mailbox; a POP3 mailbox has exactly one, its INBOX."""
    and_: 'MailFolderFilter | None' = Field(validation_alias=AliasChoices('and_', 'AND'), serialization_alias='AND', default=None)
    or_: 'MailFolderFilter | None' = Field(validation_alias=AliasChoices('or_', 'OR'), serialization_alias='OR', default=None)
    not_: 'MailFolderFilter | None' = Field(validation_alias=AliasChoices('not_', 'NOT'), serialization_alias='NOT', default=None)
    distinct: bool | None = Field(validation_alias=AliasChoices('distinct', 'DISTINCT'), serialization_alias='DISTINCT', default=None)
    account: ID | None = None
    role: FolderRole | None = None
    sync_enabled: bool | None = Field(validation_alias=AliasChoices('sync_enabled', 'syncEnabled'), serialization_alias='syncEnabled', default=None)
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class MailProviderFilter(BaseModel):
    """A provider an organization's admin set up: one kind, its settings and credentials, and what is switched on.

Every mailbox is linked through one. A Gmail or Microsoft provider is one OAuth client (its
id and redirect URLs in ``settings``, its secret Fernet-encrypted in ``secret``); an IMAP
provider is a mail server (fixed in ``settings``), or any server its members name. What a
kind's ``settings`` hold is :mod:`mail.providers`'s to validate; a kind needing other
settings needs no migration."""
    and_: 'MailProviderFilter | None' = Field(validation_alias=AliasChoices('and_', 'AND'), serialization_alias='AND', default=None)
    or_: 'MailProviderFilter | None' = Field(validation_alias=AliasChoices('or_', 'OR'), serialization_alias='OR', default=None)
    not_: 'MailProviderFilter | None' = Field(validation_alias=AliasChoices('not_', 'NOT'), serialization_alias='NOT', default=None)
    distinct: bool | None = Field(validation_alias=AliasChoices('distinct', 'DISTINCT'), serialization_alias='DISTINCT', default=None)
    ids: tuple[ID, ...] | None = None
    kind: Provider | None = None
    enabled: bool | None = None
    requires: tuple[DescriptorConstraintInput, ...] | None = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class MessageFilter(BaseModel):
    """One message in one folder. A copy in another folder is another row with the same ``message_id``."""
    and_: 'MessageFilter | None' = Field(validation_alias=AliasChoices('and_', 'AND'), serialization_alias='AND', default=None)
    or_: 'MessageFilter | None' = Field(validation_alias=AliasChoices('or_', 'OR'), serialization_alias='OR', default=None)
    not_: 'MessageFilter | None' = Field(validation_alias=AliasChoices('not_', 'NOT'), serialization_alias='NOT', default=None)
    distinct: bool | None = Field(validation_alias=AliasChoices('distinct', 'DISTINCT'), serialization_alias='DISTINCT', default=None)
    ids: tuple[ID, ...] | None = None
    account: ID | None = None
    requires: tuple[DescriptorConstraintInput, ...] | None = None
    folder: ID | None = None
    folder_role: FolderRole | None = Field(validation_alias=AliasChoices('folder_role', 'folderRole'), serialization_alias='folderRole', default=None)
    thread: ID | None = None
    unread: bool | None = None
    flagged: bool | None = None
    has_flag: str | None = Field(validation_alias=AliasChoices('has_flag', 'hasFlag'), serialization_alias='hasFlag', default=None)
    has_attachments: bool | None = Field(validation_alias=AliasChoices('has_attachments', 'hasAttachments'), serialization_alias='hasAttachments', default=None)
    category: ID | None = None
    sync_state: SyncState | None = Field(validation_alias=AliasChoices('sync_state', 'syncState'), serialization_alias='syncState', default=None)
    sender: str | None = None
    recipient: str | None = None
    date_from: datetime | None = Field(validation_alias=AliasChoices('date_from', 'dateFrom'), serialization_alias='dateFrom', default=None)
    date_to: datetime | None = Field(validation_alias=AliasChoices('date_to', 'dateTo'), serialization_alias='dateTo', default=None)
    search: str | None = Field(default=None, description='Search by text: a case-insensitive substring of the subject, sender or text; or semantic similarity to them ("flight booking" finds the airline\'s confirmation). Substring matches rank first, then by similarity; an explicit `ordering` replaces that ranking.')
    similar_to: ID | None = Field(validation_alias=AliasChoices('similar_to', 'similarTo'), serialization_alias='similarTo', default=None, description='Order by similarity to the given message, nearest first (no cut-off; composes with other filters and pagination). Empty when the message is not visible or has no embedding yet.')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class MessageOrderDate(BaseModel):
    """'date' variant of the @oneOf input 'MessageOrder'"""
    date: Ordering
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class MessageOrderReceivedAt(BaseModel):
    """'receivedAt' variant of the @oneOf input 'MessageOrder'"""
    received_at: Ordering = Field(validation_alias=AliasChoices('received_at', 'receivedAt'), serialization_alias='receivedAt')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class MessageOrderSubject(BaseModel):
    """'subject' variant of the @oneOf input 'MessageOrder'"""
    subject: Ordering
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class MessageOrderSenderAddress(BaseModel):
    """'senderAddress' variant of the @oneOf input 'MessageOrder'"""
    sender_address: Ordering = Field(validation_alias=AliasChoices('sender_address', 'senderAddress'), serialization_alias='senderAddress')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class MessageOrderSize(BaseModel):
    """'size' variant of the @oneOf input 'MessageOrder'"""
    size: Ordering
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)
MessageOrder = MessageOrderDate | MessageOrderReceivedAt | MessageOrderSubject | MessageOrderSenderAddress | MessageOrderSize

class MoveMessagesInput(BaseModel):
    """Move messages to another folder of their mailbox."""
    messages: tuple[ID, ...]
    folder: ID
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class OffsetPaginationInput(BaseModel):
    """No documentation"""
    offset: Annotated[int | None, GraphQLDefault('0')] = None
    'Default: 0'
    limit: int | None = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class OutgoingMessageFilter(BaseModel):
    """A message sent through a mailbox's SMTP server: what was asked, and what happened."""
    and_: 'OutgoingMessageFilter | None' = Field(validation_alias=AliasChoices('and_', 'AND'), serialization_alias='AND', default=None)
    or_: 'OutgoingMessageFilter | None' = Field(validation_alias=AliasChoices('or_', 'OR'), serialization_alias='OR', default=None)
    not_: 'OutgoingMessageFilter | None' = Field(validation_alias=AliasChoices('not_', 'NOT'), serialization_alias='NOT', default=None)
    distinct: bool | None = Field(validation_alias=AliasChoices('distinct', 'DISTINCT'), serialization_alias='DISTINCT', default=None)
    account: ID | None = None
    status: OutgoingStatus | None = None
    requires: tuple[DescriptorConstraintInput, ...] | None = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class RecipientInput(BaseModel):
    """A recipient."""
    address: str
    name: str | None = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class RequestBigFileUploadInput(BaseModel):
    """No documentation"""
    original_file_name: str = Field(validation_alias=AliasChoices('original_file_name', 'originalFileName'), serialization_alias='originalFileName')
    file_size: int = Field(validation_alias=AliasChoices('file_size', 'fileSize'), serialization_alias='fileSize')
    content_type: str | None = Field(validation_alias=AliasChoices('content_type', 'contentType'), serialization_alias='contentType', default=None)
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class ServerInput(BaseModel):
    """Where a server is reached."""
    host: str
    port: int
    security: Annotated[Security | None, GraphQLDefault('TLS')] = None
    'Default: TLS'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class SetTaskStatusInput(BaseModel):
    """Set the status of tasks (DONE records when; OPEN clears it)."""
    tasks: tuple[ID, ...]
    status: TaskStatus
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class ShareMailAccountInput(BaseModel):
    """Who sees a mailbox."""
    id: ID
    visibility: Visibility
    users: tuple[ID, ...] | None = Field(default=None, description='The members a SHARED mailbox is shared with (replaces the list). Must be members of the organization.')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class SnoozeTasksInput(BaseModel):
    """Hide tasks from the active view until a time; null wakes them now."""
    tasks: tuple[ID, ...]
    until: datetime | None = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class TaskFilter(BaseModel):
    """Something to do, made of mail threads (from any mailbox its owner can see). Personal: only its owner sees it."""
    and_: 'TaskFilter | None' = Field(validation_alias=AliasChoices('and_', 'AND'), serialization_alias='AND', default=None)
    or_: 'TaskFilter | None' = Field(validation_alias=AliasChoices('or_', 'OR'), serialization_alias='OR', default=None)
    not_: 'TaskFilter | None' = Field(validation_alias=AliasChoices('not_', 'NOT'), serialization_alias='NOT', default=None)
    distinct: bool | None = Field(validation_alias=AliasChoices('distinct', 'DISTINCT'), serialization_alias='DISTINCT', default=None)
    ids: tuple[ID, ...] | None = None
    list: ID | None = None
    no_list: bool | None = Field(validation_alias=AliasChoices('no_list', 'noList'), serialization_alias='noList', default=None)
    status: TaskStatus | None = None
    pinned: bool | None = None
    snoozed: bool | None = None
    active: bool | None = None
    due_before: datetime | None = Field(validation_alias=AliasChoices('due_before', 'dueBefore'), serialization_alias='dueBefore', default=None)
    thread: ID | None = None
    external_key: str | None = Field(validation_alias=AliasChoices('external_key', 'externalKey'), serialization_alias='externalKey', default=None)
    search: str | None = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class TaskListFilter(BaseModel):
    """A member's list of tasks (an Inbox "bundle" or project). Personal: only its owner sees it."""
    and_: 'TaskListFilter | None' = Field(validation_alias=AliasChoices('and_', 'AND'), serialization_alias='AND', default=None)
    or_: 'TaskListFilter | None' = Field(validation_alias=AliasChoices('or_', 'OR'), serialization_alias='OR', default=None)
    not_: 'TaskListFilter | None' = Field(validation_alias=AliasChoices('not_', 'NOT'), serialization_alias='NOT', default=None)
    distinct: bool | None = Field(validation_alias=AliasChoices('distinct', 'DISTINCT'), serialization_alias='DISTINCT', default=None)
    ids: tuple[ID, ...] | None = None
    search: str | None = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class TaskOrderPosition(BaseModel):
    """'position' variant of the @oneOf input 'TaskOrder'"""
    position: Ordering
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class TaskOrderDueAt(BaseModel):
    """'dueAt' variant of the @oneOf input 'TaskOrder'"""
    due_at: Ordering = Field(validation_alias=AliasChoices('due_at', 'dueAt'), serialization_alias='dueAt')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class TaskOrderCreatedAt(BaseModel):
    """'createdAt' variant of the @oneOf input 'TaskOrder'"""
    created_at: Ordering = Field(validation_alias=AliasChoices('created_at', 'createdAt'), serialization_alias='createdAt')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class TaskOrderUpdatedAt(BaseModel):
    """'updatedAt' variant of the @oneOf input 'TaskOrder'"""
    updated_at: Ordering = Field(validation_alias=AliasChoices('updated_at', 'updatedAt'), serialization_alias='updatedAt')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class TaskOrderTitle(BaseModel):
    """'title' variant of the @oneOf input 'TaskOrder'"""
    title: Ordering
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)
TaskOrder = TaskOrderPosition | TaskOrderDueAt | TaskOrderCreatedAt | TaskOrderUpdatedAt | TaskOrderTitle

class ThreadFilter(BaseModel):
    """A conversation: messages linked by In-Reply-To/References, across the mailbox's folders."""
    and_: 'ThreadFilter | None' = Field(validation_alias=AliasChoices('and_', 'AND'), serialization_alias='AND', default=None)
    or_: 'ThreadFilter | None' = Field(validation_alias=AliasChoices('or_', 'OR'), serialization_alias='OR', default=None)
    not_: 'ThreadFilter | None' = Field(validation_alias=AliasChoices('not_', 'NOT'), serialization_alias='NOT', default=None)
    distinct: bool | None = Field(validation_alias=AliasChoices('distinct', 'DISTINCT'), serialization_alias='DISTINCT', default=None)
    account: ID | None = None
    requires: tuple[DescriptorConstraintInput, ...] | None = None
    folder: ID | None = None
    ids: tuple[ID, ...] | None = None
    folder_role: FolderRole | None = Field(validation_alias=AliasChoices('folder_role', 'folderRole'), serialization_alias='folderRole', default=None)
    unread: bool | None = None
    flagged: bool | None = None
    has_attachments: bool | None = Field(validation_alias=AliasChoices('has_attachments', 'hasAttachments'), serialization_alias='hasAttachments', default=None)
    category: ID | None = None
    task: ID | None = None
    has_task: bool | None = Field(validation_alias=AliasChoices('has_task', 'hasTask'), serialization_alias='hasTask', default=None)
    search: str | None = Field(default=None, description='Only conversations with a message matching the text: the same substring and meaning search as `messages(filters: {search})`.')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class ThreadLinkInput(BaseModel):
    """How a conversation is put into a task."""
    source: Annotated[TaskLinkSource | None, GraphQLDefault('USER')] = Field(default=None, description='APP when an app sorted it; USER when a person did.')
    'APP when an app sorted it; USER when a person did.\nDefault: USER'
    confidence: float | None = Field(default=None, description="An app's confidence, 0–1.")
    reason: Annotated[str | None, GraphQLDefault('')] = Field(default=None, description='Why the conversation belongs here.')
    'Why the conversation belongs here.\nDefault: '
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class ThreadOrderLastMessageAt(BaseModel):
    """'lastMessageAt' variant of the @oneOf input 'ThreadOrder'"""
    last_message_at: Ordering = Field(validation_alias=AliasChoices('last_message_at', 'lastMessageAt'), serialization_alias='lastMessageAt')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class ThreadOrderMessageCount(BaseModel):
    """'messageCount' variant of the @oneOf input 'ThreadOrder'"""
    message_count: Ordering = Field(validation_alias=AliasChoices('message_count', 'messageCount'), serialization_alias='messageCount')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)
ThreadOrder = ThreadOrderLastMessageAt | ThreadOrderMessageCount

class UndoMailChangesInput(BaseModel):
    """Take back changes that have not reached the server: by change, or every one of some messages."""
    changes: tuple[ID, ...] | None = None
    messages: tuple[ID, ...] | None = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class UpdateMailAccountInput(BaseModel):
    """Changes to a mailbox; omitted fields stay as they are. Changing servers or credentials tests the login first. A mailbox whose provider fixes the servers keeps them (an admin changes them on the provider)."""
    id: ID
    name: str | None = None
    display_name: str | None = Field(validation_alias=AliasChoices('display_name', 'displayName'), serialization_alias='displayName', default=None)
    password: str | None = None
    username: str | None = None
    incoming: ServerInput | None = None
    smtp: ServerInput | None = None
    smtp_username: str | None = Field(validation_alias=AliasChoices('smtp_username', 'smtpUsername'), serialization_alias='smtpUsername', default=None)
    smtp_password: str | None = Field(validation_alias=AliasChoices('smtp_password', 'smtpPassword'), serialization_alias='smtpPassword', default=None)
    save_sent_copy: bool | None = Field(validation_alias=AliasChoices('save_sent_copy', 'saveSentCopy'), serialization_alias='saveSentCopy', default=None)
    pop_leave_on_server: bool | None = Field(validation_alias=AliasChoices('pop_leave_on_server', 'popLeaveOnServer'), serialization_alias='popLeaveOnServer', default=None)
    enabled: bool | None = Field(default=None, description='False pauses the mailbox (DISABLED); true makes it ACTIVE again (after a successful login).')
    push_seen: bool | None = Field(validation_alias=AliasChoices('push_seen', 'pushSeen'), serialization_alias='pushSeen', default=None, description='Push read/unread to the server. Off keeps it here; turning it on pushes what was kept.')
    push_flagged: bool | None = Field(validation_alias=AliasChoices('push_flagged', 'pushFlagged'), serialization_alias='pushFlagged', default=None, description='Push flagging to the server. Off keeps it here.')
    push_keywords: bool | None = Field(validation_alias=AliasChoices('push_keywords', 'pushKeywords'), serialization_alias='pushKeywords', default=None, description='Push keywords (KEYWORD categories) to the server. Off keeps them here.')
    push_moves: bool | None = Field(validation_alias=AliasChoices('push_moves', 'pushMoves'), serialization_alias='pushMoves', default=None, description='Push moves and archiving. Off refuses moves (a folder only exists on the server).')
    push_deletes: bool | None = Field(validation_alias=AliasChoices('push_deletes', 'pushDeletes'), serialization_alias='pushDeletes', default=None, description='Push deletes. Off only hides deleted mail here.')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class UpdateMailFolderInput(BaseModel):
    """Changes to a folder."""
    id: ID
    sync_enabled: bool = Field(validation_alias=AliasChoices('sync_enabled', 'syncEnabled'), serialization_alias='syncEnabled', description='Whether syncs read the folder. Turning it off keeps what is stored.')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class UpdateOAuthProviderInput(BaseModel):
    """Changes to a Gmail or Microsoft provider; omitted fields stay as they are. Its client id stays while mailboxes go through it (their refresh tokens belong to that client)."""
    id: ID
    name: str | None = None
    enabled: bool | None = None
    client_id: str | None = Field(validation_alias=AliasChoices('client_id', 'clientId'), serialization_alias='clientId', default=None)
    client_secret: str | None = Field(validation_alias=AliasChoices('client_secret', 'clientSecret'), serialization_alias='clientSecret', default=None, description='A new client secret. Omitted or empty: the stored one is kept.')
    redirect_urls: tuple[str, ...] | None = Field(validation_alias=AliasChoices('redirect_urls', 'redirectUrls'), serialization_alias='redirectUrls', default=None)
    tenant: str | None = None
    capabilities: tuple[ProviderCapability, ...] | None = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class UpdateProviderInput(BaseModel):
    """Changes any provider takes, whatever its kind; omitted fields stay as they are."""
    id: ID
    name: str | None = None
    enabled: bool | None = None
    capabilities: tuple[ProviderCapability, ...] | None = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class UpdateServerProviderInput(BaseModel):
    """Changes to an IMAP provider; omitted fields stay as they are. Fixed servers may change and its mailboxes follow; while it has mailboxes, its protocol and whether its servers are fixed stay."""
    id: ID
    name: str | None = None
    enabled: bool | None = None
    protocol: Protocol | None = None
    incoming: ServerInput | None = None
    smtp: ServerInput | None = None
    save_sent_copy: bool | None = Field(validation_alias=AliasChoices('save_sent_copy', 'saveSentCopy'), serialization_alias='saveSentCopy', default=None)
    capabilities: tuple[ProviderCapability, ...] | None = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class UpdateTaskInput(BaseModel):
    """Changes to a task; omitted fields stay as they are."""
    id: ID
    title: str | None = None
    notes: str | None = None
    list: ID | None = Field(default=None, description='Another list; null takes it off its list.')
    due_at: datetime | None = Field(validation_alias=AliasChoices('due_at', 'dueAt'), serialization_alias='dueAt', default=None)
    pinned: bool | None = None
    position: float | None = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class UpdateTaskListInput(BaseModel):
    """Changes to a task list; omitted fields stay as they are."""
    id: ID
    name: str | None = None
    color: str | None = None
    position: float | None = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class ServerSettings(BaseModel):
    """Where a server is reached."""
    typename: Literal['ServerSettings'] = Field(alias='__typename', default='ServerSettings', exclude=True)
    host: str
    port: int
    security: Security
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for ServerSettings"""
        document = 'fragment ServerSettings on ServerSettings {\n  host\n  port\n  security\n  __typename\n}'
        name = 'ServerSettings'
        type = 'ServerSettings'

class AuthSessionResult(BaseModel):
    """A Structure: what the login linked, so the app can open its page."""
    typename: Literal['AuthResult'] = Field(alias='__typename', default='AuthResult', exclude=True)
    identifier: str
    id: ID
    label: str | None = Field(default=None)
    model_config = ConfigDict(frozen=True)

class AuthSession(BaseModel):
    """A login at an external provider, the same shape in every service. Open `openUrl` in the user's browser; then, by `finish`: REDIRECT — the provider redirects to `redirectUrl` with `code` and `state`, call `completeAuth` with both; POLL — call `completeAuth` with the `state` every `interval` seconds until `status` is not PENDING."""
    typename: Literal['AuthSession'] = Field(alias='__typename', default='AuthSession', exclude=True)
    state: str
    'Opaque, unguessable, single-use, stored server-side. THE handle of the login.'
    status: AuthStatus
    finish: AuthFinish
    open_url: str = Field(alias='openUrl')
    "https. What the app opens in the user's browser."
    expires_at: datetime = Field(alias='expiresAt')
    'Until when the first approval can happen.'
    redirect_url: str | None = Field(default=None, alias='redirectUrl')
    'REDIRECT: where the provider sends the browser back to (the relay URL).'
    interval: int | None = Field(default=None)
    'POLL: seconds between two completeAuth calls.'
    user_code: str | None = Field(default=None, alias='userCode')
    "POLL: the code the user confirms on the provider's page."
    step: str | None = Field(default=None)
    'Null until the first approval; then what is still awaited, e.g. MFA.'
    error_code: str | None = Field(default=None, alias='errorCode')
    "FAILED: machine-readable, the service's own error codes."
    error_message: str | None = Field(default=None, alias='errorMessage')
    'FAILED: one sentence for the user.'
    result: AuthSessionResult | None = Field(default=None)
    'DONE: what was linked. May be set earlier when it already exists (a relink).'
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for AuthSession"""
        document = 'fragment AuthSession on AuthSession {\n  state\n  status\n  finish\n  openUrl\n  expiresAt\n  redirectUrl\n  interval\n  userCode\n  step\n  errorCode\n  errorMessage\n  result {\n    identifier\n    id\n    label\n    __typename\n  }\n  __typename\n}'
        name = 'AuthSession'
        type = 'AuthSession'

class CategoryAccount(BaseModel):
    """A linked mailbox. Private to the member who linked it unless shared (`visibility`)."""
    typename: Literal['MailAccount'] = Field(alias='__typename', default='MailAccount', exclude=True)
    id: ID
    model_config = ConfigDict(frozen=True)

class Category(BaseModel):
    """A category of a mailbox, shared by everyone who sees the mailbox: LOCAL, or kept on the server as an IMAP keyword (KEYWORD)."""
    typename: Literal['Category'] = Field(alias='__typename', default='Category', exclude=True)
    id: ID
    name: str
    "The category's name."
    color: str
    'A display color (e.g. #4f86f7).'
    sync: CategorySync
    'Where the category lives.'
    keyword: str
    'The IMAP keyword a KEYWORD category is kept as.'
    created_at: datetime = Field(alias='createdAt')
    'When the category was created.'
    message_count: int = Field(alias='messageCount')
    'Messages in the category (every copy counts).'
    account: CategoryAccount
    'The mailbox.'
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Category"""
        document = 'fragment Category on Category {\n  id\n  name\n  color\n  sync\n  keyword\n  createdAt\n  messageCount\n  account {\n    id\n    __typename\n  }\n  __typename\n}'
        name = 'Category'
        type = 'Category'

class MailChangeAccount(BaseModel):
    """A linked mailbox. Private to the member who linked it unless shared (`visibility`)."""
    typename: Literal['MailAccount'] = Field(alias='__typename', default='MailAccount', exclude=True)
    id: ID
    model_config = ConfigDict(frozen=True)

class MailChangeOriginFolder(BaseModel):
    """A folder of a mailbox."""
    typename: Literal['MailFolder'] = Field(alias='__typename', default='MailFolder', exclude=True)
    id: ID
    model_config = ConfigDict(frozen=True)

class MailChangeTargetFolder(BaseModel):
    """A folder of a mailbox."""
    typename: Literal['MailFolder'] = Field(alias='__typename', default='MailFolder', exclude=True)
    id: ID
    model_config = ConfigDict(frozen=True)

class MailChangeMessage(BaseModel):
    """A message in a folder. A copy in another folder is another message with the same `messageId`."""
    typename: Literal['Message'] = Field(alias='__typename', default='Message', exclude=True)
    id: ID
    model_config = ConfigDict(frozen=True)

class MailChange(BaseModel):
    """A change made here that has not reached the server yet (a pushed one is gone)."""
    typename: Literal['MailChange'] = Field(alias='__typename', default='MailChange', exclude=True)
    id: ID
    kind: MailChangeKind
    'What the change does.'
    state: MailChangeState
    'Where the change is.'
    add: tuple[str, ...]
    'FLAGS: flags and keywords to add.'
    remove: tuple[str, ...]
    'FLAGS: flags and keywords to remove.'
    push_after: datetime = Field(alias='pushAfter')
    'Not pushed before then (the undo window, or the wait after a failure).'
    attempts: int
    'Failed attempts so far.'
    error: str | None = Field(default=None)
    'Why the last attempt failed.'
    error_code: MailErrorCode | None = Field(default=None, alias='errorCode')
    'The machine-readable kind of `error`.'
    created_at: datetime = Field(alias='createdAt')
    'When the change was made.'
    undoable: bool
    'Whether `undoMailChanges` can still take it back (in its undo window, or FAILED).'
    account: MailChangeAccount
    'The mailbox.'
    origin_folder: MailChangeOriginFolder | None = Field(default=None, alias='originFolder')
    'MOVE/EXPUNGE: the folder the server has the message in.'
    target_folder: MailChangeTargetFolder | None = Field(default=None, alias='targetFolder')
    'MOVE: the folder it goes to.'
    message: MailChangeMessage | None = Field(default=None)
    'The message (also one deleted here, while its delete is on its way).'
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for MailChange"""
        document = 'fragment MailChange on MailChange {\n  id\n  kind\n  state\n  add\n  remove\n  pushAfter\n  attempts\n  error\n  errorCode\n  createdAt\n  undoable\n  account {\n    id\n    __typename\n  }\n  originFolder {\n    id\n    __typename\n  }\n  targetFolder {\n    id\n    __typename\n  }\n  message {\n    id\n    __typename\n  }\n  __typename\n}'
        name = 'MailChange'
        type = 'MailChange'

class PushResultAccount(BaseModel):
    """A linked mailbox. Private to the member who linked it unless shared (`visibility`)."""
    typename: Literal['MailAccount'] = Field(alias='__typename', default='MailAccount', exclude=True)
    id: ID
    model_config = ConfigDict(frozen=True)

class PushResult(BaseModel):
    """What pushing a mailbox's changes did."""
    typename: Literal['PushResult'] = Field(alias='__typename', default='PushResult', exclude=True)
    pushed: int
    'Changes that reached the server.'
    pending: int
    'Changes still waiting (in their undo window, backing off, or a sync held the mailbox).'
    failed: int
    'Changes that did not reach the server.'
    account: PushResultAccount
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for PushResult"""
        document = 'fragment PushResult on PushResult {\n  pushed\n  pending\n  failed\n  account {\n    id\n    __typename\n  }\n  __typename\n}'
        name = 'PushResult'
        type = 'PushResult'

class BigFileStore(BaseModel):
    """A BigFileStore represents a large object stored behind the S3 datalayer."""
    typename: Literal['BigFileStore'] = Field(alias='__typename', default='BigFileStore', exclude=True)
    id: ID
    path: str
    'The object-store URI of the file'
    bucket: str
    'The datalayer bucket/service this store belongs to.'
    key: str
    'The object key/path within the datalayer bucket.'
    size_bytes: int | None = Field(default=None, alias='sizeBytes')
    'How many bytes this store actually holds, measured when its upload was finished. Null while unfinished, or for stores written before this was recorded'
    original_file_name: str | None = Field(default=None, alias='originalFileName')
    'The original client-provided file name.'
    content_type: str | None = Field(default=None, alias='contentType')
    'The client-provided content type for the uploaded file.'
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for BigFileStore"""
        document = 'fragment BigFileStore on BigFileStore {\n  id\n  path\n  bucket\n  key\n  sizeBytes\n  originalFileName\n  contentType\n  __typename\n}'
        name = 'BigFileStore'
        type = 'BigFileStore'

class BigFileUploadGrant(BaseModel):
    """Temporary S3 credentials for uploading a big file."""
    typename: Literal['BigFileUploadGrant'] = Field(alias='__typename', default='BigFileUploadGrant', exclude=True)
    status: str
    access_key: str = Field(alias='accessKey')
    secret_key: str = Field(alias='secretKey')
    session_token: str = Field(alias='sessionToken')
    region: str
    bucket: str
    key: str
    path: str
    expires_in: int = Field(alias='expiresIn')
    store: str
    max_bytes: int = Field(alias='maxBytes')
    original_file_name: str | None = Field(default=None, alias='originalFileName')
    upload_file_name: str = Field(alias='uploadFileName')
    upload_content_type: str | None = Field(default=None, alias='uploadContentType')
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for BigFileUploadGrant"""
        document = 'fragment BigFileUploadGrant on BigFileUploadGrant {\n  status\n  accessKey\n  secretKey\n  sessionToken\n  region\n  bucket\n  key\n  path\n  expiresIn\n  store\n  maxBytes\n  originalFileName\n  uploadFileName\n  uploadContentType\n  __typename\n}'
        name = 'BigFileUploadGrant'
        type = 'BigFileUploadGrant'

class MailFolderAccount(BaseModel):
    """A linked mailbox. Private to the member who linked it unless shared (`visibility`)."""
    typename: Literal['MailAccount'] = Field(alias='__typename', default='MailAccount', exclude=True)
    id: ID
    model_config = ConfigDict(frozen=True)

class MailFolder(BaseModel):
    """A folder of a mailbox."""
    typename: Literal['MailFolder'] = Field(alias='__typename', default='MailFolder', exclude=True)
    id: ID
    path: str
    "The folder's full name on the server, decoded (e.g. 'INBOX/Receipts')."
    name: str
    'The last segment of the path.'
    role: FolderRole
    'What the folder is for.'
    selectable: bool
    'Whether the folder can hold messages (\\Noselect folders only hold folders).'
    sync_enabled: bool = Field(alias='syncEnabled')
    'Whether syncs read this folder.'
    exists_on_server: bool = Field(alias='existsOnServer')
    'False once the server stopped listing the folder.'
    total_count: int = Field(alias='totalCount')
    'Messages in the folder, as the server counts them.'
    unread_count: int = Field(alias='unreadCount')
    'Unread messages in the folder, as they are here (local changes included).'
    server_unread_count: int = Field(alias='serverUnreadCount')
    'Unread messages in the folder, as the server counted them at the last sync.'
    keywords_allowed: bool = Field(alias='keywordsAllowed')
    'The folder keeps any keyword on the server (else KEYWORD categories stay local here).'
    backfill_done: bool = Field(alias='backfillDone')
    'The backfill reached the window (or the first message).'
    last_synced_at: datetime | None = Field(default=None, alias='lastSyncedAt')
    'When the folder was last synced.'
    account: MailFolderAccount
    'The mailbox this folder is in.'
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for MailFolder"""
        document = 'fragment MailFolder on MailFolder {\n  id\n  path\n  name\n  role\n  selectable\n  syncEnabled\n  existsOnServer\n  totalCount\n  unreadCount\n  serverUnreadCount\n  keywordsAllowed\n  backfillDone\n  lastSyncedAt\n  account {\n    id\n    __typename\n  }\n  __typename\n}'
        name = 'MailFolder'
        type = 'MailFolder'

class Address(BaseModel):
    """A mail address with its display name."""
    typename: Literal['Address'] = Field(alias='__typename', default='Address', exclude=True)
    name: str
    'The display name (may be empty).'
    address: str
    'The address.'
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Address"""
        document = 'fragment Address on Address {\n  name\n  address\n  __typename\n}'
        name = 'Address'
        type = 'Address'

class RefusedRecipient(BaseModel):
    """A recipient the SMTP server refused."""
    typename: Literal['RefusedRecipient'] = Field(alias='__typename', default='RefusedRecipient', exclude=True)
    address: str
    code: int
    message: str
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for RefusedRecipient"""
        document = 'fragment RefusedRecipient on RefusedRecipient {\n  address\n  code\n  message\n  __typename\n}'
        name = 'RefusedRecipient'
        type = 'RefusedRecipient'

class MailProviderRef(BaseModel):
    """A provider the organization's admins set up (an IMAP server, a Gmail or Microsoft OAuth client). Every mailbox is linked through one; credentials are never returned."""
    typename: Literal['MailProvider'] = Field(alias='__typename', default='MailProvider', exclude=True)
    id: ID
    name: str
    'What the organization calls it.'
    kind: Provider
    'Which kind of provider this is.'
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for MailProviderRef"""
        document = 'fragment MailProviderRef on MailProvider {\n  id\n  name\n  kind\n  __typename\n}'
        name = 'MailProviderRef'
        type = 'MailProvider'

class ProviderKindCapabilities(BaseModel):
    """A capability a provider can have switched on, as shown to whoever switches it."""
    typename: Literal['ProviderCapabilityInfo'] = Field(alias='__typename', default='ProviderCapabilityInfo', exclude=True)
    capability: ProviderCapability
    label: str
    description: str
    model_config = ConfigDict(frozen=True)

class ProviderKind(BaseModel):
    """A kind of provider this server can run. What a client needs to offer it, without knowing the kinds itself."""
    typename: Literal['ProviderKind'] = Field(alias='__typename', default='ProviderKind', exclude=True)
    kind: Provider
    label: str
    description: str
    auth_method: AuthMethod = Field(alias='authMethod')
    'How its mailboxes log in: PASSWORD — link one with `createMailAccount`; XOAUTH2 — with `startOAuthLink`.'
    capabilities: tuple[ProviderKindCapabilities, ...]
    'Everything the kind can do; a provider enables a subset.'
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for ProviderKind"""
        document = 'fragment ProviderKind on ProviderKind {\n  kind\n  label\n  description\n  authMethod\n  capabilities {\n    capability\n    label\n    description\n    __typename\n  }\n  __typename\n}'
        name = 'ProviderKind'
        type = 'ProviderKind'

class MailboxSyncEvent(BaseModel):
    """A mailbox finished syncing."""
    typename: Literal['MailboxSyncEvent'] = Field(alias='__typename', default='MailboxSyncEvent', exclude=True)
    account_id: ID = Field(alias='accountId')
    created: int
    updated: int
    deleted: int
    more: bool
    folders: tuple[ID, ...]
    'The folders whose messages changed, so a client refetches only those lists.'
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for MailboxSyncEvent"""
        document = 'fragment MailboxSyncEvent on MailboxSyncEvent {\n  accountId\n  created\n  updated\n  deleted\n  more\n  folders\n  __typename\n}'
        name = 'MailboxSyncEvent'
        type = 'MailboxSyncEvent'

class TaskList(BaseModel):
    """A member's list of tasks (an Inbox bundle or project). Only its owner sees it."""
    typename: Literal['TaskList'] = Field(alias='__typename', default='TaskList', exclude=True)
    id: ID
    name: str
    "The list's name."
    color: str
    'A display color (e.g. #4f86f7).'
    position: float
    "Where the list sorts among the owner's lists."
    created_at: datetime = Field(alias='createdAt')
    'When the list was created.'
    open_count: int = Field(alias='openCount')
    'How many tasks on the list are OPEN.'
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for TaskList"""
        document = 'fragment TaskList on TaskList {\n  id\n  name\n  color\n  position\n  createdAt\n  openCount\n  __typename\n}'
        name = 'TaskList'
        type = 'TaskList'

class ListTaskList(BaseModel):
    """A member's list of tasks (an Inbox bundle or project). Only its owner sees it."""
    typename: Literal['TaskList'] = Field(alias='__typename', default='TaskList', exclude=True)
    id: ID
    name: str
    "The list's name."
    model_config = ConfigDict(frozen=True)

class ListTask(BaseModel):
    """Something to do, made of mail conversations from any mailbox its owner can see. Only its owner sees it. Its status is independent of the mail: finishing a task changes no message."""
    typename: Literal['Task'] = Field(alias='__typename', default='Task', exclude=True)
    id: ID
    title: str
    'What to do.'
    notes: str
    'Free notes.'
    status: TaskStatus
    'Where the task is.'
    pinned: bool
    'Pinned to the top.'
    due_at: datetime | None = Field(default=None, alias='dueAt')
    'When it is due.'
    snoozed_until: datetime | None = Field(default=None, alias='snoozedUntil')
    'Hidden from the active view until then.'
    snoozed: bool
    'Whether the task is snoozed right now.'
    position: float
    'Where the task sorts in its list.'
    external_key: str | None = Field(default=None, alias='externalKey')
    "An app's own key for the task: `upsertTask` finds the task by it, so sorting again updates instead of duplicating."
    completed_at: datetime | None = Field(default=None, alias='completedAt')
    'When it was marked DONE.'
    created_at: datetime = Field(alias='createdAt')
    'When the task was created.'
    updated_at: datetime = Field(alias='updatedAt')
    'When the task last changed.'
    thread_count: int = Field(alias='threadCount')
    'How many conversations the task has (visible ones).'
    unread_count: int = Field(alias='unreadCount')
    "Unread messages over the task's conversations."
    list: ListTaskList | None = Field(default=None)
    'The list it is on, if any.'
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for ListTask"""
        document = 'fragment ListTask on Task {\n  id\n  title\n  notes\n  status\n  pinned\n  dueAt\n  snoozedUntil\n  snoozed\n  position\n  externalKey\n  completedAt\n  createdAt\n  updatedAt\n  threadCount\n  unreadCount\n  list {\n    id\n    name\n    __typename\n  }\n  __typename\n}'
        name = 'ListTask'
        type = 'Task'

class TaskThreadTask(BaseModel):
    """Something to do, made of mail conversations from any mailbox its owner can see. Only its owner sees it. Its status is independent of the mail: finishing a task changes no message."""
    typename: Literal['Task'] = Field(alias='__typename', default='Task', exclude=True)
    id: ID
    model_config = ConfigDict(frozen=True)

class TaskThreadThread(BaseModel):
    """A conversation: messages linked by In-Reply-To/References, across the mailbox's folders."""
    typename: Literal['Thread'] = Field(alias='__typename', default='Thread', exclude=True)
    id: ID
    subject: str
    'The subject without Re:/Fwd: prefixes.'
    model_config = ConfigDict(frozen=True)

class TaskThread(BaseModel):
    """A conversation in a task: who put it there, and (for an app) how sure it was and why."""
    typename: Literal['TaskThread'] = Field(alias='__typename', default='TaskThread', exclude=True)
    id: ID
    source: TaskLinkSource
    'Who put the thread into the task.'
    confidence: float | None = Field(default=None)
    "An app's confidence (0–1) that the thread belongs here."
    reason: str
    'Why the thread belongs here, in words.'
    position: float
    'Where the thread sorts within the task.'
    created_at: datetime = Field(alias='createdAt')
    'When the thread was put into the task.'
    task: TaskThreadTask
    'The task.'
    thread: TaskThreadThread
    'The conversation.'
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for TaskThread"""
        document = 'fragment TaskThread on TaskThread {\n  id\n  source\n  confidence\n  reason\n  position\n  createdAt\n  task {\n    id\n    __typename\n  }\n  thread {\n    id\n    subject\n    __typename\n  }\n  __typename\n}'
        name = 'TaskThread'
        type = 'TaskThread'

class MailPreset(BaseModel):
    """Server settings of a well-known mail provider, to fill in a new mailbox."""
    typename: Literal['MailPreset'] = Field(alias='__typename', default='MailPreset', exclude=True)
    key: str
    name: str
    domains: tuple[str, ...]
    provider: Provider
    imap: ServerSettings | None = Field(default=None)
    pop3: ServerSettings | None = Field(default=None)
    smtp: ServerSettings | None = Field(default=None)
    save_sent_copy: bool = Field(alias='saveSentCopy')
    oauth: bool
    'The provider is linked through OAuth (`startOAuthLink`).'
    oauth_configured: bool = Field(alias='oauthConfigured')
    'The organization has an enabled provider for it (`mailProviders`).'
    note: str
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for MailPreset"""
        document = 'fragment ServerSettings on ServerSettings {\n  host\n  port\n  security\n  __typename\n}\n\nfragment MailPreset on MailPreset {\n  key\n  name\n  domains\n  provider\n  imap {\n    ...ServerSettings\n    __typename\n  }\n  pop3 {\n    ...ServerSettings\n    __typename\n  }\n  smtp {\n    ...ServerSettings\n    __typename\n  }\n  saveSentCopy\n  oauth\n  oauthConfigured\n  note\n  __typename\n}'
        name = 'MailPreset'
        type = 'MailPreset'

class Attachment(BaseModel):
    """A file attached to a message."""
    typename: Literal['Attachment'] = Field(alias='__typename', default='Attachment', exclude=True)
    id: ID
    position: int
    "The part's position among the message's attachments."
    filename: str
    'The file name, as the sender gave it.'
    content_type: str = Field(alias='contentType')
    'The MIME type.'
    size: int
    'The decoded size in bytes.'
    content_id: str | None = Field(default=None, alias='contentId')
    'The Content-ID an HTML body references (cid:), without angle brackets.'
    inline: bool
    'Shown inside the HTML body (an inline image), not as a download.'
    store: BigFileStore | None = Field(default=None)
    'The bytes in the datalayer (request a read grant from it); null without a datalayer.'
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Attachment"""
        document = 'fragment BigFileStore on BigFileStore {\n  id\n  path\n  bucket\n  key\n  sizeBytes\n  originalFileName\n  contentType\n  __typename\n}\n\nfragment Attachment on Attachment {\n  id\n  position\n  filename\n  contentType\n  size\n  contentId\n  inline\n  store {\n    ...BigFileStore\n    __typename\n  }\n  __typename\n}'
        name = 'Attachment'
        type = 'Attachment'

class ListMessageAccount(BaseModel):
    """A linked mailbox. Private to the member who linked it unless shared (`visibility`)."""
    typename: Literal['MailAccount'] = Field(alias='__typename', default='MailAccount', exclude=True)
    id: ID
    model_config = ConfigDict(frozen=True)

class ListMessageFolder(BaseModel):
    """A folder of a mailbox."""
    typename: Literal['MailFolder'] = Field(alias='__typename', default='MailFolder', exclude=True)
    id: ID
    role: FolderRole
    'What the folder is for.'
    model_config = ConfigDict(frozen=True)

class ListMessageThread(BaseModel):
    """A conversation: messages linked by In-Reply-To/References, across the mailbox's folders."""
    typename: Literal['Thread'] = Field(alias='__typename', default='Thread', exclude=True)
    id: ID
    model_config = ConfigDict(frozen=True)

class ListMessageCategories(BaseModel):
    """A category of a mailbox, shared by everyone who sees the mailbox: LOCAL, or kept on the server as an IMAP keyword (KEYWORD)."""
    typename: Literal['Category'] = Field(alias='__typename', default='Category', exclude=True)
    id: ID
    name: str
    "The category's name."
    color: str
    'A display color (e.g. #4f86f7).'
    model_config = ConfigDict(frozen=True)

class ListMessage(BaseModel):
    """A message in a folder. A copy in another folder is another message with the same `messageId`."""
    typename: Literal['Message'] = Field(alias='__typename', default='Message', exclude=True)
    id: ID
    subject: str
    'The decoded subject.'
    sender: Address
    'The sender.'
    date: datetime | None = Field(default=None)
    'The Date header (else when the server received it).'
    received_at: datetime | None = Field(default=None, alias='receivedAt')
    'When the server received the message (IMAP INTERNALDATE).'
    snippet: str
    'The start of the text, for list views.'
    flags: tuple[str, ...]
    "The flags and keywords as they are here: the server's with local changes applied."
    is_read: bool = Field(alias='isRead')
    'Whether the message is read (\\Seen).'
    is_flagged: bool = Field(alias='isFlagged')
    'Whether the message is flagged (\\Flagged).'
    is_answered: bool = Field(alias='isAnswered')
    'Whether the message was answered (\\Answered).'
    has_attachments: bool = Field(alias='hasAttachments')
    'The message has attachments (not counting inline images).'
    sync_state: SyncState = Field(alias='syncState')
    'How the message here relates to the server.'
    account: ListMessageAccount
    'The mailbox.'
    folder: ListMessageFolder
    'The folder the message is in.'
    thread: ListMessageThread | None = Field(default=None)
    'The conversation.'
    categories: tuple[ListMessageCategories, ...]
    'The categories the message is in.'
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for ListMessage"""
        document = 'fragment Address on Address {\n  name\n  address\n  __typename\n}\n\nfragment ListMessage on Message {\n  id\n  subject\n  sender {\n    ...Address\n    __typename\n  }\n  date\n  receivedAt\n  snippet\n  flags\n  isRead\n  isFlagged\n  isAnswered\n  hasAttachments\n  syncState\n  account {\n    id\n    __typename\n  }\n  folder {\n    id\n    role\n    __typename\n  }\n  thread {\n    id\n    __typename\n  }\n  categories {\n    id\n    name\n    color\n    __typename\n  }\n  __typename\n}'
        name = 'ListMessage'
        type = 'Message'

class OutgoingMessageAccount(BaseModel):
    """A linked mailbox. Private to the member who linked it unless shared (`visibility`)."""
    typename: Literal['MailAccount'] = Field(alias='__typename', default='MailAccount', exclude=True)
    id: ID
    model_config = ConfigDict(frozen=True)

class OutgoingMessageInReplyTo(BaseModel):
    """A message in a folder. A copy in another folder is another message with the same `messageId`."""
    typename: Literal['Message'] = Field(alias='__typename', default='Message', exclude=True)
    id: ID
    model_config = ConfigDict(frozen=True)

class OutgoingMessage(BaseModel):
    """A message sent through a mailbox's SMTP server."""
    typename: Literal['OutgoingMessage'] = Field(alias='__typename', default='OutgoingMessage', exclude=True)
    id: ID
    status: OutgoingStatus
    'Where the message is.'
    subject: str
    'The subject.'
    text_body: str = Field(alias='textBody')
    'The plain-text body.'
    html_body: str = Field(alias='htmlBody')
    'The HTML body, as given.'
    message_id: str = Field(alias='messageId')
    'The Message-ID given to the message.'
    saved_to_sent: bool = Field(alias='savedToSent')
    'A copy was appended to the Sent folder.'
    error: str | None = Field(default=None)
    'Why sending failed.'
    error_code: MailErrorCode | None = Field(default=None, alias='errorCode')
    'The machine-readable kind of `error`.'
    created_at: datetime = Field(alias='createdAt')
    'When sending was asked for.'
    sent_at: datetime | None = Field(default=None, alias='sentAt')
    'When the SMTP server accepted it.'
    account: OutgoingMessageAccount
    'The mailbox it is sent from.'
    in_reply_to: OutgoingMessageInReplyTo | None = Field(default=None, alias='inReplyTo')
    'The message this answers (sets In-Reply-To/References).'
    to: tuple[Address, ...]
    'To addresses.'
    cc: tuple[Address, ...]
    'Cc addresses.'
    bcc: tuple[Address, ...]
    'Bcc addresses.'
    refused: tuple[RefusedRecipient, ...]
    'Recipients the SMTP server refused while accepting the rest.'
    attachments: tuple[BigFileStore, ...]
    'The files attached.'
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for OutgoingMessage"""
        document = 'fragment Address on Address {\n  name\n  address\n  __typename\n}\n\nfragment BigFileStore on BigFileStore {\n  id\n  path\n  bucket\n  key\n  sizeBytes\n  originalFileName\n  contentType\n  __typename\n}\n\nfragment RefusedRecipient on RefusedRecipient {\n  address\n  code\n  message\n  __typename\n}\n\nfragment OutgoingMessage on OutgoingMessage {\n  id\n  status\n  subject\n  textBody\n  htmlBody\n  messageId\n  savedToSent\n  error\n  errorCode\n  createdAt\n  sentAt\n  account {\n    id\n    __typename\n  }\n  inReplyTo {\n    id\n    __typename\n  }\n  to {\n    ...Address\n    __typename\n  }\n  cc {\n    ...Address\n    __typename\n  }\n  bcc {\n    ...Address\n    __typename\n  }\n  refused {\n    ...RefusedRecipient\n    __typename\n  }\n  attachments {\n    ...BigFileStore\n    __typename\n  }\n  __typename\n}'
        name = 'OutgoingMessage'
        type = 'OutgoingMessage'

class MailAccount(BaseModel):
    """A linked mailbox. Private to the member who linked it unless shared (`visibility`)."""
    typename: Literal['MailAccount'] = Field(alias='__typename', default='MailAccount', exclude=True)
    id: ID
    name: str
    "A display name for the mailbox (e.g. 'Work')."
    email_address: str = Field(alias='emailAddress')
    "The mailbox's address; the From of sent mail."
    display_name: str = Field(alias='displayName')
    'The sender name of sent mail.'
    provider: Provider
    'Who hosts the mailbox.'
    status: MailAccountStatus
    'Where the mailbox is in its lifecycle.'
    visibility: Visibility
    'Who in the organization sees the mailbox and its mail.'
    protocol: Protocol
    'How incoming mail is read.'
    auth_method: AuthMethod = Field(alias='authMethod')
    'How the service logs in.'
    capabilities: tuple[str, ...]
    'What the incoming server announced (IMAP CAPABILITY, POP3 CAPA).'
    last_synced_at: datetime | None = Field(default=None, alias='lastSyncedAt')
    'When the last successful sync finished.'
    last_error: str | None = Field(default=None, alias='lastError')
    'Why the last sync or connection failed, if it did.'
    last_error_code: MailErrorCode | None = Field(default=None, alias='lastErrorCode')
    'The machine-readable kind of `last_error`.'
    backfill_done: bool = Field(alias='backfillDone')
    'Every synced folder has reached the backfill window.'
    created_at: datetime = Field(alias='createdAt')
    'When the mailbox was linked.'
    is_owner: bool = Field(alias='isOwner')
    'Whether the caller linked the mailbox (and so may change its credentials, sharing, or delete it).'
    can_send: bool = Field(alias='canSend')
    'Whether the mailbox can send: it has an SMTP server, and its provider is enabled with SEND switched on.'
    syncing: bool
    'Whether a sync holds the mailbox right now.'
    unread_count: int = Field(alias='unreadCount')
    'Unread messages over the synced folders, as they are here.'
    pending_changes: int = Field(alias='pendingChanges')
    'Changes made here that have not reached the server yet.'
    failed_changes: int = Field(alias='failedChanges')
    'Changes made here that did not reach the server (see `mailChanges`).'
    mail_provider: MailProviderRef | None = Field(default=None, alias='mailProvider')
    "The organization's provider the mailbox was linked through (null: none any more; an admin has to set one up)."
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for MailAccount"""
        document = 'fragment MailProviderRef on MailProvider {\n  id\n  name\n  kind\n  __typename\n}\n\nfragment MailAccount on MailAccount {\n  id\n  name\n  emailAddress\n  displayName\n  provider\n  status\n  visibility\n  protocol\n  authMethod\n  capabilities\n  lastSyncedAt\n  lastError\n  lastErrorCode\n  backfillDone\n  createdAt\n  isOwner\n  canSend\n  syncing\n  unreadCount\n  pendingChanges\n  failedChanges\n  mailProvider {\n    ...MailProviderRef\n    __typename\n  }\n  __typename\n}'
        name = 'MailAccount'
        type = 'MailAccount'

class MailProviderOauth(BaseModel):
    """The OAuth client of a Gmail or Microsoft provider. Its secret is never returned."""
    typename: Literal['OAuthClientSettings'] = Field(alias='__typename', default='OAuthClientSettings', exclude=True)
    client_id: str = Field(alias='clientId')
    'The OAuth client id.'
    redirect_urls: tuple[str, ...] = Field(alias='redirectUrls')
    'The redirect URLs a login may use; the first is the default.'
    tenant: str
    'Microsoft: the Entra tenant logins go through (`common`: any account).'
    has_secret: bool = Field(alias='hasSecret')
    'Whether a client secret is stored (a public client with PKCE has none).'
    model_config = ConfigDict(frozen=True)

class MailProviderServer(BaseModel):
    """The servers of an IMAP provider: fixed by the admin, or left to each member (`fixed` false)."""
    typename: Literal['MailServerSettings'] = Field(alias='__typename', default='MailServerSettings', exclude=True)
    fixed: bool
    'True: its mailboxes use these servers, members only give their login. False: members name the servers.'
    protocol: Protocol | None = Field(default=None)
    'With fixed servers: how incoming mail is read.'
    incoming: ServerSettings | None = Field(default=None)
    'With fixed servers: the IMAP or POP3 server.'
    smtp: ServerSettings | None = Field(default=None)
    'With fixed servers: the SMTP server (null: its mailboxes cannot send).'
    save_sent_copy: bool = Field(alias='saveSentCopy')
    'Whether its mailboxes append sent mail to Sent.'
    model_config = ConfigDict(frozen=True)

class MailProvider(MailProviderRef, BaseModel):
    """A provider the organization's admins set up (an IMAP server, a Gmail or Microsoft OAuth client). Every mailbox is linked through one; credentials are never returned."""
    typename: Literal['MailProvider'] = Field(alias='__typename', default='MailProvider', exclude=True)
    enabled: bool
    'A disabled provider links no mailbox, and its mailboxes neither sync, push nor send.'
    capabilities: tuple[ProviderCapability, ...]
    'The capabilities switched on for this provider.'
    mailbox_count: int = Field(alias='mailboxCount')
    'How many mailboxes of the organization are linked through it (all of them, whoever sees them).'
    created_at: datetime = Field(alias='createdAt')
    'When the provider was set up.'
    updated_at: datetime = Field(alias='updatedAt')
    'When it was last changed.'
    kind_info: ProviderKind = Field(alias='kindInfo')
    'What its kind is and can do.'
    oauth: MailProviderOauth | None = Field(default=None)
    'Its OAuth client when it is a Gmail or Microsoft provider, else null.'
    server: MailProviderServer | None = Field(default=None)
    'Its servers when it is an IMAP provider, else null.'
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for MailProvider"""
        document = 'fragment MailProviderRef on MailProvider {\n  id\n  name\n  kind\n  __typename\n}\n\nfragment ProviderKind on ProviderKind {\n  kind\n  label\n  description\n  authMethod\n  capabilities {\n    capability\n    label\n    description\n    __typename\n  }\n  __typename\n}\n\nfragment ServerSettings on ServerSettings {\n  host\n  port\n  security\n  __typename\n}\n\nfragment MailProvider on MailProvider {\n  ...MailProviderRef\n  enabled\n  capabilities\n  mailboxCount\n  createdAt\n  updatedAt\n  kindInfo {\n    ...ProviderKind\n    __typename\n  }\n  oauth {\n    clientId\n    redirectUrls\n    tenant\n    hasSecret\n    __typename\n  }\n  server {\n    fixed\n    protocol\n    incoming {\n      ...ServerSettings\n      __typename\n    }\n    smtp {\n      ...ServerSettings\n      __typename\n    }\n    saveSentCopy\n    __typename\n  }\n  __typename\n}'
        name = 'MailProvider'
        type = 'MailProvider'

class Message(ListMessage, BaseModel):
    """A message in a folder. A copy in another folder is another message with the same `messageId`."""
    typename: Literal['Message'] = Field(alias='__typename', default='Message', exclude=True)
    message_id: str | None = Field(default=None, alias='messageId')
    'The Message-ID header, without angle brackets.'
    in_reply_to: str | None = Field(default=None, alias='inReplyTo')
    'The In-Reply-To header, without angle brackets.'
    references: tuple[str, ...]
    'The References header, oldest first.'
    text_body: str = Field(alias='textBody')
    'The plain-text body (converted from HTML when there is none).'
    has_remote_images: bool = Field(alias='hasRemoteImages')
    'The HTML loads images from the internet.'
    size: int
    'The message size in bytes.'
    server_flags: tuple[str, ...] = Field(alias='serverFlags')
    'The flags and keywords as the server last had them.'
    truncated: bool
    'The message was larger than the sync limit; only its headers are stored.'
    created_at: datetime = Field(alias='createdAt')
    'When the message was first stored.'
    reply_to: tuple[Address, ...] = Field(alias='replyTo')
    'Reply-To addresses.'
    to: tuple[Address, ...]
    'To addresses.'
    cc: tuple[Address, ...]
    'Cc addresses.'
    bcc: tuple[Address, ...]
    'Bcc addresses (only known on sent mail).'
    attachments: tuple[Attachment, ...]
    'Attached files, inline images included (`inline`).'
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Message"""
        document = 'fragment BigFileStore on BigFileStore {\n  id\n  path\n  bucket\n  key\n  sizeBytes\n  originalFileName\n  contentType\n  __typename\n}\n\nfragment Address on Address {\n  name\n  address\n  __typename\n}\n\nfragment Attachment on Attachment {\n  id\n  position\n  filename\n  contentType\n  size\n  contentId\n  inline\n  store {\n    ...BigFileStore\n    __typename\n  }\n  __typename\n}\n\nfragment ListMessage on Message {\n  id\n  subject\n  sender {\n    ...Address\n    __typename\n  }\n  date\n  receivedAt\n  snippet\n  flags\n  isRead\n  isFlagged\n  isAnswered\n  hasAttachments\n  syncState\n  account {\n    id\n    __typename\n  }\n  folder {\n    id\n    role\n    __typename\n  }\n  thread {\n    id\n    __typename\n  }\n  categories {\n    id\n    name\n    color\n    __typename\n  }\n  __typename\n}\n\nfragment Message on Message {\n  ...ListMessage\n  messageId\n  inReplyTo\n  references\n  textBody\n  hasRemoteImages\n  size\n  serverFlags\n  truncated\n  createdAt\n  replyTo {\n    ...Address\n    __typename\n  }\n  to {\n    ...Address\n    __typename\n  }\n  cc {\n    ...Address\n    __typename\n  }\n  bcc {\n    ...Address\n    __typename\n  }\n  attachments {\n    ...Attachment\n    __typename\n  }\n  __typename\n}'
        name = 'Message'
        type = 'Message'

class ListThreadAccount(BaseModel):
    """A linked mailbox. Private to the member who linked it unless shared (`visibility`)."""
    typename: Literal['MailAccount'] = Field(alias='__typename', default='MailAccount', exclude=True)
    id: ID
    model_config = ConfigDict(frozen=True)

class ListThread(BaseModel):
    """A conversation: messages linked by In-Reply-To/References, across the mailbox's folders."""
    typename: Literal['Thread'] = Field(alias='__typename', default='Thread', exclude=True)
    id: ID
    subject: str
    'The subject without Re:/Fwd: prefixes.'
    last_message_at: datetime | None = Field(default=None, alias='lastMessageAt')
    'The date of the newest message.'
    message_count: int = Field(alias='messageCount')
    'How many messages are in the conversation.'
    unread: bool
    'Whether a message of the conversation is unread.'
    flagged: bool
    'Whether any message of the conversation is flagged.'
    has_attachments: bool = Field(alias='hasAttachments')
    'Whether any message of the conversation has attachments.'
    participants: tuple[Address, ...]
    'Distinct senders, oldest first ("Anna, Ben & 2 more").'
    account: ListThreadAccount
    'The mailbox the conversation is in.'
    latest_message: ListMessage | None = Field(default=None, alias='latestMessage')
    'The newest message, optionally only within a folder or a folder role: what a list row shows. Null when the conversation has no message there.'
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for ListThread"""
        document = 'fragment Address on Address {\n  name\n  address\n  __typename\n}\n\nfragment ListMessage on Message {\n  id\n  subject\n  sender {\n    ...Address\n    __typename\n  }\n  date\n  receivedAt\n  snippet\n  flags\n  isRead\n  isFlagged\n  isAnswered\n  hasAttachments\n  syncState\n  account {\n    id\n    __typename\n  }\n  folder {\n    id\n    role\n    __typename\n  }\n  thread {\n    id\n    __typename\n  }\n  categories {\n    id\n    name\n    color\n    __typename\n  }\n  __typename\n}\n\nfragment ListThread on Thread {\n  id\n  subject\n  lastMessageAt\n  messageCount\n  unread\n  flagged\n  hasAttachments\n  participants {\n    ...Address\n    __typename\n  }\n  account {\n    id\n    __typename\n  }\n  latestMessage {\n    ...ListMessage\n    __typename\n  }\n  __typename\n}'
        name = 'ListThread'
        type = 'Thread'

class DetailMailAccountSharedWith(BaseModel):
    """A user account; sub is the stable subject identifier from the identity provider."""
    typename: Literal['User'] = Field(alias='__typename', default='User', exclude=True)
    id: ID
    sub: str
    preferred_username: str = Field(alias='preferredUsername')
    model_config = ConfigDict(frozen=True)

class DetailMailAccount(MailAccount, BaseModel):
    """A linked mailbox. Private to the member who linked it unless shared (`visibility`)."""
    typename: Literal['MailAccount'] = Field(alias='__typename', default='MailAccount', exclude=True)
    incoming_host: str = Field(alias='incomingHost')
    'The IMAP or POP3 server.'
    incoming_port: int = Field(alias='incomingPort')
    'The IMAP or POP3 port.'
    incoming_security: Security = Field(alias='incomingSecurity')
    'Transport security of the incoming connection.'
    smtp_host: str | None = Field(default=None, alias='smtpHost')
    'The SMTP server; without one the mailbox cannot send.'
    smtp_port: int | None = Field(default=None, alias='smtpPort')
    'The SMTP port.'
    smtp_security: Security = Field(alias='smtpSecurity')
    'Transport security of the SMTP connection.'
    username: str
    'The login name (usually the address).'
    save_sent_copy: bool = Field(alias='saveSentCopy')
    'Append sent mail to the Sent folder (off for Gmail and Microsoft, which keep a copy themselves).'
    pop_leave_on_server: bool = Field(alias='popLeaveOnServer')
    'POP3: keep downloaded mail on the server. Off deletes it there once stored.'
    push_seen: bool = Field(alias='pushSeen')
    'Read/unread is pushed to the server (else kept here).'
    push_flagged: bool = Field(alias='pushFlagged')
    'Flagging is pushed to the server (else kept here).'
    push_keywords: bool = Field(alias='pushKeywords')
    'Keywords (KEYWORD categories) are pushed to the server (else kept here).'
    push_moves: bool = Field(alias='pushMoves')
    'Moves are pushed to the server (else refused).'
    push_deletes: bool = Field(alias='pushDeletes')
    'Deletes are pushed to the server (else only hidden here).'
    server_side_folders: bool = Field(alias='serverSideFolders')
    'Whether folders, moves and flags live on the server (IMAP). On POP3 flags are local and moves are refused.'
    shared_with: tuple[DetailMailAccountSharedWith, ...] = Field(alias='sharedWith')
    'Members who see the mailbox when it is SHARED.'
    folders: tuple[MailFolder, ...]
    "The mailbox's folders (a POP3 mailbox has one, its INBOX)."
    pending_auth: AuthSession | None = Field(default=None, alias='pendingAuth')
    'The re-link of this mailbox still to be finished, when you started it and it is PENDING: continue it with `resumeAuth(state)`. Null otherwise.'
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for DetailMailAccount"""
        document = 'fragment MailProviderRef on MailProvider {\n  id\n  name\n  kind\n  __typename\n}\n\nfragment AuthSession on AuthSession {\n  state\n  status\n  finish\n  openUrl\n  expiresAt\n  redirectUrl\n  interval\n  userCode\n  step\n  errorCode\n  errorMessage\n  result {\n    identifier\n    id\n    label\n    __typename\n  }\n  __typename\n}\n\nfragment MailAccount on MailAccount {\n  id\n  name\n  emailAddress\n  displayName\n  provider\n  status\n  visibility\n  protocol\n  authMethod\n  capabilities\n  lastSyncedAt\n  lastError\n  lastErrorCode\n  backfillDone\n  createdAt\n  isOwner\n  canSend\n  syncing\n  unreadCount\n  pendingChanges\n  failedChanges\n  mailProvider {\n    ...MailProviderRef\n    __typename\n  }\n  __typename\n}\n\nfragment MailFolder on MailFolder {\n  id\n  path\n  name\n  role\n  selectable\n  syncEnabled\n  existsOnServer\n  totalCount\n  unreadCount\n  serverUnreadCount\n  keywordsAllowed\n  backfillDone\n  lastSyncedAt\n  account {\n    id\n    __typename\n  }\n  __typename\n}\n\nfragment DetailMailAccount on MailAccount {\n  ...MailAccount\n  incomingHost\n  incomingPort\n  incomingSecurity\n  smtpHost\n  smtpPort\n  smtpSecurity\n  username\n  saveSentCopy\n  popLeaveOnServer\n  pushSeen\n  pushFlagged\n  pushKeywords\n  pushMoves\n  pushDeletes\n  serverSideFolders\n  sharedWith {\n    id\n    sub\n    preferredUsername\n    __typename\n  }\n  folders {\n    ...MailFolder\n    __typename\n  }\n  pendingAuth {\n    ...AuthSession\n    __typename\n  }\n  __typename\n}'
        name = 'DetailMailAccount'
        type = 'MailAccount'

class SyncResult(BaseModel):
    """What one mailbox sync did."""
    typename: Literal['SyncResult'] = Field(alias='__typename', default='SyncResult', exclude=True)
    created: int
    'New messages.'
    updated: int
    'Messages whose flags changed.'
    deleted: int
    'Messages gone from the server.'
    folders: int
    'Folders synced.'
    more: bool
    'More mail is waiting (the backfill or a burst of new mail continues on the next sync).'
    account: MailAccount
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for SyncResult"""
        document = 'fragment MailProviderRef on MailProvider {\n  id\n  name\n  kind\n  __typename\n}\n\nfragment MailAccount on MailAccount {\n  id\n  name\n  emailAddress\n  displayName\n  provider\n  status\n  visibility\n  protocol\n  authMethod\n  capabilities\n  lastSyncedAt\n  lastError\n  lastErrorCode\n  backfillDone\n  createdAt\n  isOwner\n  canSend\n  syncing\n  unreadCount\n  pendingChanges\n  failedChanges\n  mailProvider {\n    ...MailProviderRef\n    __typename\n  }\n  __typename\n}\n\nfragment SyncResult on SyncResult {\n  created\n  updated\n  deleted\n  folders\n  more\n  account {\n    ...MailAccount\n    __typename\n  }\n  __typename\n}'
        name = 'SyncResult'
        type = 'SyncResult'

class Task(ListTask, BaseModel):
    """Something to do, made of mail conversations from any mailbox its owner can see. Only its owner sees it. Its status is independent of the mail: finishing a task changes no message."""
    typename: Literal['Task'] = Field(alias='__typename', default='Task', exclude=True)
    links: tuple[TaskThread, ...]
    "The task's conversations with who put them there; only those in mailboxes the caller can still see."
    threads: tuple[ListThread, ...]
    "The task's conversations, newest first; only those in mailboxes the caller can still see."
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Task"""
        document = 'fragment Address on Address {\n  name\n  address\n  __typename\n}\n\nfragment ListMessage on Message {\n  id\n  subject\n  sender {\n    ...Address\n    __typename\n  }\n  date\n  receivedAt\n  snippet\n  flags\n  isRead\n  isFlagged\n  isAnswered\n  hasAttachments\n  syncState\n  account {\n    id\n    __typename\n  }\n  folder {\n    id\n    role\n    __typename\n  }\n  thread {\n    id\n    __typename\n  }\n  categories {\n    id\n    name\n    color\n    __typename\n  }\n  __typename\n}\n\nfragment ListTask on Task {\n  id\n  title\n  notes\n  status\n  pinned\n  dueAt\n  snoozedUntil\n  snoozed\n  position\n  externalKey\n  completedAt\n  createdAt\n  updatedAt\n  threadCount\n  unreadCount\n  list {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment ListThread on Thread {\n  id\n  subject\n  lastMessageAt\n  messageCount\n  unread\n  flagged\n  hasAttachments\n  participants {\n    ...Address\n    __typename\n  }\n  account {\n    id\n    __typename\n  }\n  latestMessage {\n    ...ListMessage\n    __typename\n  }\n  __typename\n}\n\nfragment TaskThread on TaskThread {\n  id\n  source\n  confidence\n  reason\n  position\n  createdAt\n  task {\n    id\n    __typename\n  }\n  thread {\n    id\n    subject\n    __typename\n  }\n  __typename\n}\n\nfragment Task on Task {\n  ...ListTask\n  links {\n    ...TaskThread\n    __typename\n  }\n  threads {\n    ...ListThread\n    __typename\n  }\n  __typename\n}'
        name = 'Task'
        type = 'Task'

class Thread(ListThread, BaseModel):
    """A conversation: messages linked by In-Reply-To/References, across the mailbox's folders."""
    typename: Literal['Thread'] = Field(alias='__typename', default='Thread', exclude=True)
    messages: tuple[ListMessage, ...]
    "The conversation's messages, oldest first."
    tasks: tuple[ListTask, ...]
    "The caller's tasks this conversation is in."
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Thread"""
        document = 'fragment Address on Address {\n  name\n  address\n  __typename\n}\n\nfragment ListMessage on Message {\n  id\n  subject\n  sender {\n    ...Address\n    __typename\n  }\n  date\n  receivedAt\n  snippet\n  flags\n  isRead\n  isFlagged\n  isAnswered\n  hasAttachments\n  syncState\n  account {\n    id\n    __typename\n  }\n  folder {\n    id\n    role\n    __typename\n  }\n  thread {\n    id\n    __typename\n  }\n  categories {\n    id\n    name\n    color\n    __typename\n  }\n  __typename\n}\n\nfragment ListTask on Task {\n  id\n  title\n  notes\n  status\n  pinned\n  dueAt\n  snoozedUntil\n  snoozed\n  position\n  externalKey\n  completedAt\n  createdAt\n  updatedAt\n  threadCount\n  unreadCount\n  list {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment ListThread on Thread {\n  id\n  subject\n  lastMessageAt\n  messageCount\n  unread\n  flagged\n  hasAttachments\n  participants {\n    ...Address\n    __typename\n  }\n  account {\n    id\n    __typename\n  }\n  latestMessage {\n    ...ListMessage\n    __typename\n  }\n  __typename\n}\n\nfragment Thread on Thread {\n  ...ListThread\n  messages {\n    ...ListMessage\n    __typename\n  }\n  tasks {\n    ...ListTask\n    __typename\n  }\n  __typename\n}'
        name = 'Thread'
        type = 'Thread'

class CreateMailAccountMutation(BaseModel):
    """No documentation found for this operation."""
    create_mail_account: DetailMailAccount = Field(alias='createMailAccount')
    'Link a mailbox with a username and (app) password through an IMAP provider; the login is tested first.'

    class Arguments(BaseModel):
        """Arguments for CreateMailAccount """
        provider: ID
        email_address: str = Field(validation_alias=AliasChoices('email_address', 'emailAddress'), serialization_alias='emailAddress')
        password: str
        name: str | None = Field(default=None)
        display_name: str | None = Field(validation_alias=AliasChoices('display_name', 'displayName'), serialization_alias='displayName', default=None)
        protocol: Protocol | None = Field(default=None)
        incoming: ServerInput | None = Field(default=None)
        smtp: ServerInput | None = Field(default=None)
        username: str | None = Field(default=None)
        smtp_username: str | None = Field(validation_alias=AliasChoices('smtp_username', 'smtpUsername'), serialization_alias='smtpUsername', default=None)
        smtp_password: str | None = Field(validation_alias=AliasChoices('smtp_password', 'smtpPassword'), serialization_alias='smtpPassword', default=None)
        save_sent_copy: bool | None = Field(validation_alias=AliasChoices('save_sent_copy', 'saveSentCopy'), serialization_alias='saveSentCopy', default=None)
        pop_leave_on_server: bool | None = Field(validation_alias=AliasChoices('pop_leave_on_server', 'popLeaveOnServer'), serialization_alias='popLeaveOnServer', default=None)
        visibility: Visibility | None = Field(default=None)

    class Meta:
        """Meta class for CreateMailAccount """
        document = 'fragment MailProviderRef on MailProvider {\n  id\n  name\n  kind\n  __typename\n}\n\nfragment AuthSession on AuthSession {\n  state\n  status\n  finish\n  openUrl\n  expiresAt\n  redirectUrl\n  interval\n  userCode\n  step\n  errorCode\n  errorMessage\n  result {\n    identifier\n    id\n    label\n    __typename\n  }\n  __typename\n}\n\nfragment MailAccount on MailAccount {\n  id\n  name\n  emailAddress\n  displayName\n  provider\n  status\n  visibility\n  protocol\n  authMethod\n  capabilities\n  lastSyncedAt\n  lastError\n  lastErrorCode\n  backfillDone\n  createdAt\n  isOwner\n  canSend\n  syncing\n  unreadCount\n  pendingChanges\n  failedChanges\n  mailProvider {\n    ...MailProviderRef\n    __typename\n  }\n  __typename\n}\n\nfragment MailFolder on MailFolder {\n  id\n  path\n  name\n  role\n  selectable\n  syncEnabled\n  existsOnServer\n  totalCount\n  unreadCount\n  serverUnreadCount\n  keywordsAllowed\n  backfillDone\n  lastSyncedAt\n  account {\n    id\n    __typename\n  }\n  __typename\n}\n\nfragment DetailMailAccount on MailAccount {\n  ...MailAccount\n  incomingHost\n  incomingPort\n  incomingSecurity\n  smtpHost\n  smtpPort\n  smtpSecurity\n  username\n  saveSentCopy\n  popLeaveOnServer\n  pushSeen\n  pushFlagged\n  pushKeywords\n  pushMoves\n  pushDeletes\n  serverSideFolders\n  sharedWith {\n    id\n    sub\n    preferredUsername\n    __typename\n  }\n  folders {\n    ...MailFolder\n    __typename\n  }\n  pendingAuth {\n    ...AuthSession\n    __typename\n  }\n  __typename\n}\n\nmutation CreateMailAccount($provider: ID!, $emailAddress: String!, $password: String!, $name: String, $displayName: String, $protocol: Protocol, $incoming: ServerInput, $smtp: ServerInput, $username: String, $smtpUsername: String, $smtpPassword: String, $saveSentCopy: Boolean, $popLeaveOnServer: Boolean, $visibility: Visibility) {\n  createMailAccount(\n    input: {\n      provider: $provider\n      emailAddress: $emailAddress\n      password: $password\n      name: $name\n      displayName: $displayName\n      protocol: $protocol\n      incoming: $incoming\n      smtp: $smtp\n      username: $username\n      smtpUsername: $smtpUsername\n      smtpPassword: $smtpPassword\n      saveSentCopy: $saveSentCopy\n      popLeaveOnServer: $popLeaveOnServer\n      visibility: $visibility\n    }\n  ) {\n    ...DetailMailAccount\n    __typename\n  }\n}'

class UpdateMailAccountMutation(BaseModel):
    """No documentation found for this operation."""
    update_mail_account: DetailMailAccount = Field(alias='updateMailAccount')
    'Change a mailbox (owner only); new servers or credentials are tested first.'

    class Arguments(BaseModel):
        """Arguments for UpdateMailAccount """
        input: UpdateMailAccountInput

    class Meta:
        """Meta class for UpdateMailAccount """
        document = 'fragment MailProviderRef on MailProvider {\n  id\n  name\n  kind\n  __typename\n}\n\nfragment AuthSession on AuthSession {\n  state\n  status\n  finish\n  openUrl\n  expiresAt\n  redirectUrl\n  interval\n  userCode\n  step\n  errorCode\n  errorMessage\n  result {\n    identifier\n    id\n    label\n    __typename\n  }\n  __typename\n}\n\nfragment MailAccount on MailAccount {\n  id\n  name\n  emailAddress\n  displayName\n  provider\n  status\n  visibility\n  protocol\n  authMethod\n  capabilities\n  lastSyncedAt\n  lastError\n  lastErrorCode\n  backfillDone\n  createdAt\n  isOwner\n  canSend\n  syncing\n  unreadCount\n  pendingChanges\n  failedChanges\n  mailProvider {\n    ...MailProviderRef\n    __typename\n  }\n  __typename\n}\n\nfragment MailFolder on MailFolder {\n  id\n  path\n  name\n  role\n  selectable\n  syncEnabled\n  existsOnServer\n  totalCount\n  unreadCount\n  serverUnreadCount\n  keywordsAllowed\n  backfillDone\n  lastSyncedAt\n  account {\n    id\n    __typename\n  }\n  __typename\n}\n\nfragment DetailMailAccount on MailAccount {\n  ...MailAccount\n  incomingHost\n  incomingPort\n  incomingSecurity\n  smtpHost\n  smtpPort\n  smtpSecurity\n  username\n  saveSentCopy\n  popLeaveOnServer\n  pushSeen\n  pushFlagged\n  pushKeywords\n  pushMoves\n  pushDeletes\n  serverSideFolders\n  sharedWith {\n    id\n    sub\n    preferredUsername\n    __typename\n  }\n  folders {\n    ...MailFolder\n    __typename\n  }\n  pendingAuth {\n    ...AuthSession\n    __typename\n  }\n  __typename\n}\n\nmutation UpdateMailAccount($input: UpdateMailAccountInput!) {\n  updateMailAccount(input: $input) {\n    ...DetailMailAccount\n    __typename\n  }\n}'

class ShareMailAccountMutation(BaseModel):
    """No documentation found for this operation."""
    share_mail_account: DetailMailAccount = Field(alias='shareMailAccount')
    'Set who sees a mailbox (owner only).'

    class Arguments(BaseModel):
        """Arguments for ShareMailAccount """
        input: ShareMailAccountInput

    class Meta:
        """Meta class for ShareMailAccount """
        document = 'fragment MailProviderRef on MailProvider {\n  id\n  name\n  kind\n  __typename\n}\n\nfragment AuthSession on AuthSession {\n  state\n  status\n  finish\n  openUrl\n  expiresAt\n  redirectUrl\n  interval\n  userCode\n  step\n  errorCode\n  errorMessage\n  result {\n    identifier\n    id\n    label\n    __typename\n  }\n  __typename\n}\n\nfragment MailAccount on MailAccount {\n  id\n  name\n  emailAddress\n  displayName\n  provider\n  status\n  visibility\n  protocol\n  authMethod\n  capabilities\n  lastSyncedAt\n  lastError\n  lastErrorCode\n  backfillDone\n  createdAt\n  isOwner\n  canSend\n  syncing\n  unreadCount\n  pendingChanges\n  failedChanges\n  mailProvider {\n    ...MailProviderRef\n    __typename\n  }\n  __typename\n}\n\nfragment MailFolder on MailFolder {\n  id\n  path\n  name\n  role\n  selectable\n  syncEnabled\n  existsOnServer\n  totalCount\n  unreadCount\n  serverUnreadCount\n  keywordsAllowed\n  backfillDone\n  lastSyncedAt\n  account {\n    id\n    __typename\n  }\n  __typename\n}\n\nfragment DetailMailAccount on MailAccount {\n  ...MailAccount\n  incomingHost\n  incomingPort\n  incomingSecurity\n  smtpHost\n  smtpPort\n  smtpSecurity\n  username\n  saveSentCopy\n  popLeaveOnServer\n  pushSeen\n  pushFlagged\n  pushKeywords\n  pushMoves\n  pushDeletes\n  serverSideFolders\n  sharedWith {\n    id\n    sub\n    preferredUsername\n    __typename\n  }\n  folders {\n    ...MailFolder\n    __typename\n  }\n  pendingAuth {\n    ...AuthSession\n    __typename\n  }\n  __typename\n}\n\nmutation ShareMailAccount($input: ShareMailAccountInput!) {\n  shareMailAccount(input: $input) {\n    ...DetailMailAccount\n    __typename\n  }\n}'

class TestMailAccountMutation(BaseModel):
    """No documentation found for this operation."""
    test_mail_account: MailAccount = Field(alias='testMailAccount')
    "Log in to a mailbox's servers now."

    class Arguments(BaseModel):
        """Arguments for TestMailAccount """
        id: ID

    class Meta:
        """Meta class for TestMailAccount """
        document = 'fragment MailProviderRef on MailProvider {\n  id\n  name\n  kind\n  __typename\n}\n\nfragment MailAccount on MailAccount {\n  id\n  name\n  emailAddress\n  displayName\n  provider\n  status\n  visibility\n  protocol\n  authMethod\n  capabilities\n  lastSyncedAt\n  lastError\n  lastErrorCode\n  backfillDone\n  createdAt\n  isOwner\n  canSend\n  syncing\n  unreadCount\n  pendingChanges\n  failedChanges\n  mailProvider {\n    ...MailProviderRef\n    __typename\n  }\n  __typename\n}\n\nmutation TestMailAccount($id: ID!) {\n  testMailAccount(id: $id) {\n    ...MailAccount\n    __typename\n  }\n}'

class DeleteMailAccountMutation(BaseModel):
    """No documentation found for this operation."""
    delete_mail_account: ID = Field(alias='deleteMailAccount')
    'Unlink a mailbox (owner only). Mail on the server is untouched.'

    class Arguments(BaseModel):
        """Arguments for DeleteMailAccount """
        id: ID

    class Meta:
        """Meta class for DeleteMailAccount """
        document = 'mutation DeleteMailAccount($id: ID!) {\n  deleteMailAccount(id: $id)\n}'

class SyncMailAccountMutation(BaseModel):
    """No documentation found for this operation."""
    sync_mail_account: SyncResult = Field(alias='syncMailAccount')
    'Sync a mailbox now.'

    class Arguments(BaseModel):
        """Arguments for SyncMailAccount """
        id: ID
        folders: list[ID] | None = Field(default=None)

    class Meta:
        """Meta class for SyncMailAccount """
        document = 'fragment MailProviderRef on MailProvider {\n  id\n  name\n  kind\n  __typename\n}\n\nfragment MailAccount on MailAccount {\n  id\n  name\n  emailAddress\n  displayName\n  provider\n  status\n  visibility\n  protocol\n  authMethod\n  capabilities\n  lastSyncedAt\n  lastError\n  lastErrorCode\n  backfillDone\n  createdAt\n  isOwner\n  canSend\n  syncing\n  unreadCount\n  pendingChanges\n  failedChanges\n  mailProvider {\n    ...MailProviderRef\n    __typename\n  }\n  __typename\n}\n\nfragment SyncResult on SyncResult {\n  created\n  updated\n  deleted\n  folders\n  more\n  account {\n    ...MailAccount\n    __typename\n  }\n  __typename\n}\n\nmutation SyncMailAccount($id: ID!, $folders: [ID!]) {\n  syncMailAccount(id: $id, folders: $folders) {\n    ...SyncResult\n    __typename\n  }\n}'

class PushMailChangesMutation(BaseModel):
    """No documentation found for this operation."""
    push_mail_changes: PushResult = Field(alias='pushMailChanges')
    "Push a mailbox's due changes now."

    class Arguments(BaseModel):
        """Arguments for PushMailChanges """
        account: ID

    class Meta:
        """Meta class for PushMailChanges """
        document = 'fragment PushResult on PushResult {\n  pushed\n  pending\n  failed\n  account {\n    id\n    __typename\n  }\n  __typename\n}\n\nmutation PushMailChanges($account: ID!) {\n  pushMailChanges(account: $account) {\n    ...PushResult\n    __typename\n  }\n}'

class CreateCategoryMutation(BaseModel):
    """No documentation found for this operation."""
    create_category: Category = Field(alias='createCategory')
    'Create a category of a mailbox.'

    class Arguments(BaseModel):
        """Arguments for CreateCategory """
        account: ID
        name: str
        color: str | None = Field(default=None)
        sync: CategorySync | None = Field(default=None)
        keyword: str | None = Field(default=None)

    class Meta:
        """Meta class for CreateCategory """
        document = 'fragment Category on Category {\n  id\n  name\n  color\n  sync\n  keyword\n  createdAt\n  messageCount\n  account {\n    id\n    __typename\n  }\n  __typename\n}\n\nmutation CreateCategory($account: ID!, $name: String!, $color: String, $sync: CategorySync, $keyword: String) {\n  createCategory(\n    input: {\n      account: $account\n      name: $name\n      color: $color\n      sync: $sync\n      keyword: $keyword\n    }\n  ) {\n    ...Category\n    __typename\n  }\n}'

class UpdateCategoryMutation(BaseModel):
    """No documentation found for this operation."""
    update_category: Category = Field(alias='updateCategory')
    'Change a category.'

    class Arguments(BaseModel):
        """Arguments for UpdateCategory """
        id: ID
        name: str | None = Field(default=None)
        color: str | None = Field(default=None)
        sync: CategorySync | None = Field(default=None)
        keyword: str | None = Field(default=None)
        remove_keywords: bool | None = Field(validation_alias=AliasChoices('remove_keywords', 'removeKeywords'), serialization_alias='removeKeywords', default=None)

    class Meta:
        """Meta class for UpdateCategory """
        document = 'fragment Category on Category {\n  id\n  name\n  color\n  sync\n  keyword\n  createdAt\n  messageCount\n  account {\n    id\n    __typename\n  }\n  __typename\n}\n\nmutation UpdateCategory($id: ID!, $name: String, $color: String, $sync: CategorySync, $keyword: String, $removeKeywords: Boolean) {\n  updateCategory(\n    input: {\n      id: $id\n      name: $name\n      color: $color\n      sync: $sync\n      keyword: $keyword\n      removeKeywords: $removeKeywords\n    }\n  ) {\n    ...Category\n    __typename\n  }\n}'

class DeleteCategoryMutation(BaseModel):
    """No documentation found for this operation."""
    delete_category: ID = Field(alias='deleteCategory')
    'Delete a category.'

    class Arguments(BaseModel):
        """Arguments for DeleteCategory """
        id: ID
        remove_keywords: Annotated[bool | None, GraphQLDefault('False')] = Field(validation_alias=AliasChoices('remove_keywords', 'removeKeywords'), serialization_alias='removeKeywords', default=None)

    class Meta:
        """Meta class for DeleteCategory """
        document = 'mutation DeleteCategory($id: ID!, $removeKeywords: Boolean! = false) {\n  deleteCategory(id: $id, removeKeywords: $removeKeywords)\n}'

class UpdateMailFolderMutation(BaseModel):
    """No documentation found for this operation."""
    update_mail_folder: MailFolder = Field(alias='updateMailFolder')
    'Turn syncing a folder on or off.'

    class Arguments(BaseModel):
        """Arguments for UpdateMailFolder """
        input: UpdateMailFolderInput

    class Meta:
        """Meta class for UpdateMailFolder """
        document = 'fragment MailFolder on MailFolder {\n  id\n  path\n  name\n  role\n  selectable\n  syncEnabled\n  existsOnServer\n  totalCount\n  unreadCount\n  serverUnreadCount\n  keywordsAllowed\n  backfillDone\n  lastSyncedAt\n  account {\n    id\n    __typename\n  }\n  __typename\n}\n\nmutation UpdateMailFolder($input: UpdateMailFolderInput!) {\n  updateMailFolder(input: $input) {\n    ...MailFolder\n    __typename\n  }\n}'

class SetMessageFlagsMutation(BaseModel):
    """No documentation found for this operation."""
    set_message_flags: tuple[ListMessage, ...] = Field(alias='setMessageFlags')
    'Add and remove flags of messages.'

    class Arguments(BaseModel):
        """Arguments for SetMessageFlags """
        messages: list[ID]
        add: list[str] | None = Field(default=None)
        remove: list[str] | None = Field(default=None)

    class Meta:
        """Meta class for SetMessageFlags """
        document = 'fragment Address on Address {\n  name\n  address\n  __typename\n}\n\nfragment ListMessage on Message {\n  id\n  subject\n  sender {\n    ...Address\n    __typename\n  }\n  date\n  receivedAt\n  snippet\n  flags\n  isRead\n  isFlagged\n  isAnswered\n  hasAttachments\n  syncState\n  account {\n    id\n    __typename\n  }\n  folder {\n    id\n    role\n    __typename\n  }\n  thread {\n    id\n    __typename\n  }\n  categories {\n    id\n    name\n    color\n    __typename\n  }\n  __typename\n}\n\nmutation SetMessageFlags($messages: [ID!]!, $add: [String!], $remove: [String!]) {\n  setMessageFlags(input: { messages: $messages, add: $add, remove: $remove }) {\n    ...ListMessage\n    __typename\n  }\n}'

class MarkMessagesReadMutation(BaseModel):
    """No documentation found for this operation."""
    mark_messages_read: tuple[ListMessage, ...] = Field(alias='markMessagesRead')
    'Mark messages read or unread.'

    class Arguments(BaseModel):
        """Arguments for MarkMessagesRead """
        messages: list[ID]
        read: bool | None = Field(default=None)

    class Meta:
        """Meta class for MarkMessagesRead """
        document = 'fragment Address on Address {\n  name\n  address\n  __typename\n}\n\nfragment ListMessage on Message {\n  id\n  subject\n  sender {\n    ...Address\n    __typename\n  }\n  date\n  receivedAt\n  snippet\n  flags\n  isRead\n  isFlagged\n  isAnswered\n  hasAttachments\n  syncState\n  account {\n    id\n    __typename\n  }\n  folder {\n    id\n    role\n    __typename\n  }\n  thread {\n    id\n    __typename\n  }\n  categories {\n    id\n    name\n    color\n    __typename\n  }\n  __typename\n}\n\nmutation MarkMessagesRead($messages: [ID!]!, $read: Boolean) {\n  markMessagesRead(input: { messages: $messages, read: $read }) {\n    ...ListMessage\n    __typename\n  }\n}'

class MoveMessagesMutation(BaseModel):
    """No documentation found for this operation."""
    move_messages: tuple[ListMessage, ...] = Field(alias='moveMessages')
    'Move messages to another folder of their mailbox.'

    class Arguments(BaseModel):
        """Arguments for MoveMessages """
        input: MoveMessagesInput

    class Meta:
        """Meta class for MoveMessages """
        document = 'fragment Address on Address {\n  name\n  address\n  __typename\n}\n\nfragment ListMessage on Message {\n  id\n  subject\n  sender {\n    ...Address\n    __typename\n  }\n  date\n  receivedAt\n  snippet\n  flags\n  isRead\n  isFlagged\n  isAnswered\n  hasAttachments\n  syncState\n  account {\n    id\n    __typename\n  }\n  folder {\n    id\n    role\n    __typename\n  }\n  thread {\n    id\n    __typename\n  }\n  categories {\n    id\n    name\n    color\n    __typename\n  }\n  __typename\n}\n\nmutation MoveMessages($input: MoveMessagesInput!) {\n  moveMessages(input: $input) {\n    ...ListMessage\n    __typename\n  }\n}'

class CategorizeMessagesMutation(BaseModel):
    """No documentation found for this operation."""
    categorize_messages: tuple[ListMessage, ...] = Field(alias='categorizeMessages')
    'Put messages into categories and take them out.'

    class Arguments(BaseModel):
        """Arguments for CategorizeMessages """
        messages: list[ID]
        add: list[ID] | None = Field(default=None)
        remove: list[ID] | None = Field(default=None)

    class Meta:
        """Meta class for CategorizeMessages """
        document = 'fragment Address on Address {\n  name\n  address\n  __typename\n}\n\nfragment ListMessage on Message {\n  id\n  subject\n  sender {\n    ...Address\n    __typename\n  }\n  date\n  receivedAt\n  snippet\n  flags\n  isRead\n  isFlagged\n  isAnswered\n  hasAttachments\n  syncState\n  account {\n    id\n    __typename\n  }\n  folder {\n    id\n    role\n    __typename\n  }\n  thread {\n    id\n    __typename\n  }\n  categories {\n    id\n    name\n    color\n    __typename\n  }\n  __typename\n}\n\nmutation CategorizeMessages($messages: [ID!]!, $add: [ID!], $remove: [ID!]) {\n  categorizeMessages(input: { messages: $messages, add: $add, remove: $remove }) {\n    ...ListMessage\n    __typename\n  }\n}'

class UndoMailChangesMutation(BaseModel):
    """No documentation found for this operation."""
    undo_mail_changes: tuple[ListMessage, ...] = Field(alias='undoMailChanges')
    'Take back changes that have not reached the server.'

    class Arguments(BaseModel):
        """Arguments for UndoMailChanges """
        input: UndoMailChangesInput

    class Meta:
        """Meta class for UndoMailChanges """
        document = 'fragment Address on Address {\n  name\n  address\n  __typename\n}\n\nfragment ListMessage on Message {\n  id\n  subject\n  sender {\n    ...Address\n    __typename\n  }\n  date\n  receivedAt\n  snippet\n  flags\n  isRead\n  isFlagged\n  isAnswered\n  hasAttachments\n  syncState\n  account {\n    id\n    __typename\n  }\n  folder {\n    id\n    role\n    __typename\n  }\n  thread {\n    id\n    __typename\n  }\n  categories {\n    id\n    name\n    color\n    __typename\n  }\n  __typename\n}\n\nmutation UndoMailChanges($input: UndoMailChangesInput!) {\n  undoMailChanges(input: $input) {\n    ...ListMessage\n    __typename\n  }\n}'

class DeleteMessagesMutationDeleteMessages(BaseModel):
    """What a delete did."""
    typename: Literal['DeleteResult'] = Field(alias='__typename', default='DeleteResult', exclude=True)
    deleted: int
    'Messages deleted or moved to Trash (here at once; on the server after the undo window).'
    model_config = ConfigDict(frozen=True)

class DeleteMessagesMutation(BaseModel):
    """No documentation found for this operation."""
    delete_messages: DeleteMessagesMutationDeleteMessages = Field(alias='deleteMessages')
    'Delete messages (into Trash, or for good).'

    class Arguments(BaseModel):
        """Arguments for DeleteMessages """
        messages: list[ID]
        permanent: bool | None = Field(default=None)

    class Meta:
        """Meta class for DeleteMessages """
        document = 'mutation DeleteMessages($messages: [ID!]!, $permanent: Boolean) {\n  deleteMessages(input: { messages: $messages, permanent: $permanent }) {\n    deleted\n    __typename\n  }\n}'

class RevertMessagesToServerMutation(BaseModel):
    """No documentation found for this operation."""
    revert_messages_to_server: tuple[ListMessage, ...] = Field(alias='revertMessagesToServer')
    'Drop local-only and queued flag changes of messages: back to what the server has.'

    class Arguments(BaseModel):
        """Arguments for RevertMessagesToServer """
        messages: list[ID]

    class Meta:
        """Meta class for RevertMessagesToServer """
        document = 'fragment Address on Address {\n  name\n  address\n  __typename\n}\n\nfragment ListMessage on Message {\n  id\n  subject\n  sender {\n    ...Address\n    __typename\n  }\n  date\n  receivedAt\n  snippet\n  flags\n  isRead\n  isFlagged\n  isAnswered\n  hasAttachments\n  syncState\n  account {\n    id\n    __typename\n  }\n  folder {\n    id\n    role\n    __typename\n  }\n  thread {\n    id\n    __typename\n  }\n  categories {\n    id\n    name\n    color\n    __typename\n  }\n  __typename\n}\n\nmutation RevertMessagesToServer($messages: [ID!]!) {\n  revertMessagesToServer(messages: $messages) {\n    ...ListMessage\n    __typename\n  }\n}'

class RetryMailChangesMutation(BaseModel):
    """No documentation found for this operation."""
    retry_mail_changes: tuple[MailChange, ...] = Field(alias='retryMailChanges')
    'Queue failed changes again.'

    class Arguments(BaseModel):
        """Arguments for RetryMailChanges """
        changes: list[ID]

    class Meta:
        """Meta class for RetryMailChanges """
        document = 'fragment MailChange on MailChange {\n  id\n  kind\n  state\n  add\n  remove\n  pushAfter\n  attempts\n  error\n  errorCode\n  createdAt\n  undoable\n  account {\n    id\n    __typename\n  }\n  originFolder {\n    id\n    __typename\n  }\n  targetFolder {\n    id\n    __typename\n  }\n  message {\n    id\n    __typename\n  }\n  __typename\n}\n\nmutation RetryMailChanges($changes: [ID!]!) {\n  retryMailChanges(changes: $changes) {\n    ...MailChange\n    __typename\n  }\n}'

class StartOAuthLinkMutation(BaseModel):
    """No documentation found for this operation."""
    start_o_auth_link: AuthSession = Field(alias='startOAuthLink')
    'Start linking (or re-linking) a mailbox through a Gmail or Microsoft provider.'

    class Arguments(BaseModel):
        """Arguments for StartOAuthLink """
        provider: ID | None = Field(default=None)
        protocol: Protocol | None = Field(default=None)
        redirect_url: str | None = Field(validation_alias=AliasChoices('redirect_url', 'redirectUrl'), serialization_alias='redirectUrl', default=None)
        name: str | None = Field(default=None)
        account: ID | None = Field(default=None)
        login_hint: str | None = Field(validation_alias=AliasChoices('login_hint', 'loginHint'), serialization_alias='loginHint', default=None)

    class Meta:
        """Meta class for StartOAuthLink """
        document = 'fragment AuthSession on AuthSession {\n  state\n  status\n  finish\n  openUrl\n  expiresAt\n  redirectUrl\n  interval\n  userCode\n  step\n  errorCode\n  errorMessage\n  result {\n    identifier\n    id\n    label\n    __typename\n  }\n  __typename\n}\n\nmutation StartOAuthLink($provider: ID, $protocol: Protocol, $redirectUrl: String, $name: String, $account: ID, $loginHint: String) {\n  startOAuthLink(\n    input: {\n      provider: $provider\n      protocol: $protocol\n      redirectUrl: $redirectUrl\n      name: $name\n      account: $account\n      loginHint: $loginHint\n    }\n  ) {\n    ...AuthSession\n    __typename\n  }\n}'

class CompleteAuthMutation(BaseModel):
    """No documentation found for this operation."""
    complete_auth: AuthSession = Field(alias='completeAuth')
    'REDIRECT: finish with the code. POLL: advance one step; call until not PENDING.'

    class Arguments(BaseModel):
        """Arguments for CompleteAuth """
        input: CompleteAuthInput

    class Meta:
        """Meta class for CompleteAuth """
        document = 'fragment AuthSession on AuthSession {\n  state\n  status\n  finish\n  openUrl\n  expiresAt\n  redirectUrl\n  interval\n  userCode\n  step\n  errorCode\n  errorMessage\n  result {\n    identifier\n    id\n    label\n    __typename\n  }\n  __typename\n}\n\nmutation CompleteAuth($input: CompleteAuthInput!) {\n  completeAuth(input: $input) {\n    ...AuthSession\n    __typename\n  }\n}'

class ResumeAuthMutation(BaseModel):
    """No documentation found for this operation."""
    resume_auth: AuthSession = Field(alias='resumeAuth')
    'The same login again (a fresh openUrl if the old one cannot be reused).'

    class Arguments(BaseModel):
        """Arguments for ResumeAuth """
        state: str

    class Meta:
        """Meta class for ResumeAuth """
        document = 'fragment AuthSession on AuthSession {\n  state\n  status\n  finish\n  openUrl\n  expiresAt\n  redirectUrl\n  interval\n  userCode\n  step\n  errorCode\n  errorMessage\n  result {\n    identifier\n    id\n    label\n    __typename\n  }\n  __typename\n}\n\nmutation ResumeAuth($state: String!) {\n  resumeAuth(state: $state) {\n    ...AuthSession\n    __typename\n  }\n}'

class CancelAuthMutation(BaseModel):
    """No documentation found for this operation."""
    cancel_auth: AuthSession = Field(alias='cancelAuth')
    'Drop a login that will not be finished. Idempotent.'

    class Arguments(BaseModel):
        """Arguments for CancelAuth """
        state: str

    class Meta:
        """Meta class for CancelAuth """
        document = 'fragment AuthSession on AuthSession {\n  state\n  status\n  finish\n  openUrl\n  expiresAt\n  redirectUrl\n  interval\n  userCode\n  step\n  errorCode\n  errorMessage\n  result {\n    identifier\n    id\n    label\n    __typename\n  }\n  __typename\n}\n\nmutation CancelAuth($state: String!) {\n  cancelAuth(state: $state) {\n    ...AuthSession\n    __typename\n  }\n}'

class SendMessageMutation(BaseModel):
    """No documentation found for this operation."""
    send_message: OutgoingMessage = Field(alias='sendMessage')
    "Send a message through a mailbox's SMTP server."

    class Arguments(BaseModel):
        """Arguments for SendMessage """
        account: ID
        to: list[RecipientInput] | None = Field(default=None)
        cc: list[RecipientInput] | None = Field(default=None)
        bcc: list[RecipientInput] | None = Field(default=None)
        subject: str | None = Field(default=None)
        text: str | None = Field(default=None)
        html: str | None = Field(default=None)
        in_reply_to: ID | None = Field(validation_alias=AliasChoices('in_reply_to', 'inReplyTo'), serialization_alias='inReplyTo', default=None)
        attachments: list[str] | None = Field(default=None)

    class Meta:
        """Meta class for SendMessage """
        document = 'fragment Address on Address {\n  name\n  address\n  __typename\n}\n\nfragment BigFileStore on BigFileStore {\n  id\n  path\n  bucket\n  key\n  sizeBytes\n  originalFileName\n  contentType\n  __typename\n}\n\nfragment RefusedRecipient on RefusedRecipient {\n  address\n  code\n  message\n  __typename\n}\n\nfragment OutgoingMessage on OutgoingMessage {\n  id\n  status\n  subject\n  textBody\n  htmlBody\n  messageId\n  savedToSent\n  error\n  errorCode\n  createdAt\n  sentAt\n  account {\n    id\n    __typename\n  }\n  inReplyTo {\n    id\n    __typename\n  }\n  to {\n    ...Address\n    __typename\n  }\n  cc {\n    ...Address\n    __typename\n  }\n  bcc {\n    ...Address\n    __typename\n  }\n  refused {\n    ...RefusedRecipient\n    __typename\n  }\n  attachments {\n    ...BigFileStore\n    __typename\n  }\n  __typename\n}\n\nmutation SendMessage($account: ID!, $to: [RecipientInput!], $cc: [RecipientInput!], $bcc: [RecipientInput!], $subject: String, $text: String, $html: String, $inReplyTo: ID, $attachments: [String!]) {\n  sendMessage(\n    input: {\n      account: $account\n      to: $to\n      cc: $cc\n      bcc: $bcc\n      subject: $subject\n      text: $text\n      html: $html\n      inReplyTo: $inReplyTo\n      attachments: $attachments\n    }\n  ) {\n    ...OutgoingMessage\n    __typename\n  }\n}'

class CreateServerProviderMutation(BaseModel):
    """ A provider an admin sets up for the organization, through which its mailboxes are
 linked: a server provider (IMAP/POP3 + SMTP, the servers fixed or left to each link)
 or an OAuth client (Gmail, Microsoft)."""
    create_server_provider: MailProvider = Field(alias='createServerProvider')
    'Admins: set up an IMAP provider, with fixed servers or open to any.'

    class Arguments(BaseModel):
        """Arguments for CreateServerProvider """
        name: str
        protocol: Protocol | None = Field(default=None)
        incoming: ServerInput | None = Field(default=None)
        smtp: ServerInput | None = Field(default=None)
        save_sent_copy: bool | None = Field(validation_alias=AliasChoices('save_sent_copy', 'saveSentCopy'), serialization_alias='saveSentCopy', default=None)
        capabilities: list[ProviderCapability] | None = Field(default=None)

    class Meta:
        """Meta class for CreateServerProvider """
        document = 'fragment MailProviderRef on MailProvider {\n  id\n  name\n  kind\n  __typename\n}\n\nfragment ProviderKind on ProviderKind {\n  kind\n  label\n  description\n  authMethod\n  capabilities {\n    capability\n    label\n    description\n    __typename\n  }\n  __typename\n}\n\nfragment ServerSettings on ServerSettings {\n  host\n  port\n  security\n  __typename\n}\n\nfragment MailProvider on MailProvider {\n  ...MailProviderRef\n  enabled\n  capabilities\n  mailboxCount\n  createdAt\n  updatedAt\n  kindInfo {\n    ...ProviderKind\n    __typename\n  }\n  oauth {\n    clientId\n    redirectUrls\n    tenant\n    hasSecret\n    __typename\n  }\n  server {\n    fixed\n    protocol\n    incoming {\n      ...ServerSettings\n      __typename\n    }\n    smtp {\n      ...ServerSettings\n      __typename\n    }\n    saveSentCopy\n    __typename\n  }\n  __typename\n}\n\nmutation CreateServerProvider($name: String!, $protocol: Protocol, $incoming: ServerInput, $smtp: ServerInput, $saveSentCopy: Boolean, $capabilities: [ProviderCapability!]) {\n  createServerProvider(\n    input: {\n      name: $name\n      protocol: $protocol\n      incoming: $incoming\n      smtp: $smtp\n      saveSentCopy: $saveSentCopy\n      capabilities: $capabilities\n    }\n  ) {\n    ...MailProvider\n    __typename\n  }\n}'

class CreateOAuthProviderMutation(BaseModel):
    """No documentation found for this operation."""
    create_o_auth_provider: MailProvider = Field(alias='createOAuthProvider')
    'Admins: set up a Gmail or Microsoft OAuth client as a provider.'

    class Arguments(BaseModel):
        """Arguments for CreateOAuthProvider """
        input: CreateOAuthProviderInput

    class Meta:
        """Meta class for CreateOAuthProvider """
        document = 'fragment MailProviderRef on MailProvider {\n  id\n  name\n  kind\n  __typename\n}\n\nfragment ProviderKind on ProviderKind {\n  kind\n  label\n  description\n  authMethod\n  capabilities {\n    capability\n    label\n    description\n    __typename\n  }\n  __typename\n}\n\nfragment ServerSettings on ServerSettings {\n  host\n  port\n  security\n  __typename\n}\n\nfragment MailProvider on MailProvider {\n  ...MailProviderRef\n  enabled\n  capabilities\n  mailboxCount\n  createdAt\n  updatedAt\n  kindInfo {\n    ...ProviderKind\n    __typename\n  }\n  oauth {\n    clientId\n    redirectUrls\n    tenant\n    hasSecret\n    __typename\n  }\n  server {\n    fixed\n    protocol\n    incoming {\n      ...ServerSettings\n      __typename\n    }\n    smtp {\n      ...ServerSettings\n      __typename\n    }\n    saveSentCopy\n    __typename\n  }\n  __typename\n}\n\nmutation CreateOAuthProvider($input: CreateOAuthProviderInput!) {\n  createOAuthProvider(input: $input) {\n    ...MailProvider\n    __typename\n  }\n}'

class UpdateServerProviderMutation(BaseModel):
    """No documentation found for this operation."""
    update_server_provider: MailProvider = Field(alias='updateServerProvider')
    'Admins: change an IMAP provider; its mailboxes follow new fixed servers.'

    class Arguments(BaseModel):
        """Arguments for UpdateServerProvider """
        input: UpdateServerProviderInput

    class Meta:
        """Meta class for UpdateServerProvider """
        document = 'fragment MailProviderRef on MailProvider {\n  id\n  name\n  kind\n  __typename\n}\n\nfragment ProviderKind on ProviderKind {\n  kind\n  label\n  description\n  authMethod\n  capabilities {\n    capability\n    label\n    description\n    __typename\n  }\n  __typename\n}\n\nfragment ServerSettings on ServerSettings {\n  host\n  port\n  security\n  __typename\n}\n\nfragment MailProvider on MailProvider {\n  ...MailProviderRef\n  enabled\n  capabilities\n  mailboxCount\n  createdAt\n  updatedAt\n  kindInfo {\n    ...ProviderKind\n    __typename\n  }\n  oauth {\n    clientId\n    redirectUrls\n    tenant\n    hasSecret\n    __typename\n  }\n  server {\n    fixed\n    protocol\n    incoming {\n      ...ServerSettings\n      __typename\n    }\n    smtp {\n      ...ServerSettings\n      __typename\n    }\n    saveSentCopy\n    __typename\n  }\n  __typename\n}\n\nmutation UpdateServerProvider($input: UpdateServerProviderInput!) {\n  updateServerProvider(input: $input) {\n    ...MailProvider\n    __typename\n  }\n}'

class UpdateOAuthProviderMutation(BaseModel):
    """No documentation found for this operation."""
    update_o_auth_provider: MailProvider = Field(alias='updateOAuthProvider')
    'Admins: change a Gmail or Microsoft provider; an empty secret keeps the stored one.'

    class Arguments(BaseModel):
        """Arguments for UpdateOAuthProvider """
        input: UpdateOAuthProviderInput

    class Meta:
        """Meta class for UpdateOAuthProvider """
        document = 'fragment MailProviderRef on MailProvider {\n  id\n  name\n  kind\n  __typename\n}\n\nfragment ProviderKind on ProviderKind {\n  kind\n  label\n  description\n  authMethod\n  capabilities {\n    capability\n    label\n    description\n    __typename\n  }\n  __typename\n}\n\nfragment ServerSettings on ServerSettings {\n  host\n  port\n  security\n  __typename\n}\n\nfragment MailProvider on MailProvider {\n  ...MailProviderRef\n  enabled\n  capabilities\n  mailboxCount\n  createdAt\n  updatedAt\n  kindInfo {\n    ...ProviderKind\n    __typename\n  }\n  oauth {\n    clientId\n    redirectUrls\n    tenant\n    hasSecret\n    __typename\n  }\n  server {\n    fixed\n    protocol\n    incoming {\n      ...ServerSettings\n      __typename\n    }\n    smtp {\n      ...ServerSettings\n      __typename\n    }\n    saveSentCopy\n    __typename\n  }\n  __typename\n}\n\nmutation UpdateOAuthProvider($input: UpdateOAuthProviderInput!) {\n  updateOAuthProvider(input: $input) {\n    ...MailProvider\n    __typename\n  }\n}'

class UpdateProviderMutation(BaseModel):
    """No documentation found for this operation."""
    update_provider: MailProvider = Field(alias='updateProvider')
    'Admins: rename, enable or disable any provider, or change its capabilities.'

    class Arguments(BaseModel):
        """Arguments for UpdateProvider """
        input: UpdateProviderInput

    class Meta:
        """Meta class for UpdateProvider """
        document = 'fragment MailProviderRef on MailProvider {\n  id\n  name\n  kind\n  __typename\n}\n\nfragment ProviderKind on ProviderKind {\n  kind\n  label\n  description\n  authMethod\n  capabilities {\n    capability\n    label\n    description\n    __typename\n  }\n  __typename\n}\n\nfragment ServerSettings on ServerSettings {\n  host\n  port\n  security\n  __typename\n}\n\nfragment MailProvider on MailProvider {\n  ...MailProviderRef\n  enabled\n  capabilities\n  mailboxCount\n  createdAt\n  updatedAt\n  kindInfo {\n    ...ProviderKind\n    __typename\n  }\n  oauth {\n    clientId\n    redirectUrls\n    tenant\n    hasSecret\n    __typename\n  }\n  server {\n    fixed\n    protocol\n    incoming {\n      ...ServerSettings\n      __typename\n    }\n    smtp {\n      ...ServerSettings\n      __typename\n    }\n    saveSentCopy\n    __typename\n  }\n  __typename\n}\n\nmutation UpdateProvider($input: UpdateProviderInput!) {\n  updateProvider(input: $input) {\n    ...MailProvider\n    __typename\n  }\n}'

class DeleteProviderMutation(BaseModel):
    """No documentation found for this operation."""
    delete_provider: ID = Field(alias='deleteProvider')
    'Admins: remove a provider no mailbox goes through.'

    class Arguments(BaseModel):
        """Arguments for DeleteProvider """
        id: ID

    class Meta:
        """Meta class for DeleteProvider """
        document = 'mutation DeleteProvider($id: ID!) {\n  deleteProvider(id: $id)\n}'

class CreateTaskListMutation(BaseModel):
    """No documentation found for this operation."""
    create_task_list: TaskList = Field(alias='createTaskList')
    'Create a task list.'

    class Arguments(BaseModel):
        """Arguments for CreateTaskList """
        name: str
        color: str | None = Field(default=None)
        position: float | None = Field(default=None)

    class Meta:
        """Meta class for CreateTaskList """
        document = 'fragment TaskList on TaskList {\n  id\n  name\n  color\n  position\n  createdAt\n  openCount\n  __typename\n}\n\nmutation CreateTaskList($name: String!, $color: String, $position: Float) {\n  createTaskList(input: { name: $name, color: $color, position: $position }) {\n    ...TaskList\n    __typename\n  }\n}'

class UpdateTaskListMutation(BaseModel):
    """No documentation found for this operation."""
    update_task_list: TaskList = Field(alias='updateTaskList')
    'Rename, recolor or move a task list.'

    class Arguments(BaseModel):
        """Arguments for UpdateTaskList """
        input: UpdateTaskListInput

    class Meta:
        """Meta class for UpdateTaskList """
        document = 'fragment TaskList on TaskList {\n  id\n  name\n  color\n  position\n  createdAt\n  openCount\n  __typename\n}\n\nmutation UpdateTaskList($input: UpdateTaskListInput!) {\n  updateTaskList(input: $input) {\n    ...TaskList\n    __typename\n  }\n}'

class DeleteTaskListMutation(BaseModel):
    """No documentation found for this operation."""
    delete_task_list: ID = Field(alias='deleteTaskList')
    'Delete a task list; its tasks stay, on no list.'

    class Arguments(BaseModel):
        """Arguments for DeleteTaskList """
        id: ID

    class Meta:
        """Meta class for DeleteTaskList """
        document = 'mutation DeleteTaskList($id: ID!) {\n  deleteTaskList(id: $id)\n}'

class CreateTaskMutation(BaseModel):
    """No documentation found for this operation."""
    create_task: Task = Field(alias='createTask')
    'Create a task, optionally with conversations.'

    class Arguments(BaseModel):
        """Arguments for CreateTask """
        title: str
        notes: str | None = Field(default=None)
        task_list: ID | None = Field(validation_alias=AliasChoices('task_list', 'taskList'), serialization_alias='taskList', default=None)
        due_at: datetime | None = Field(validation_alias=AliasChoices('due_at', 'dueAt'), serialization_alias='dueAt', default=None)
        pinned: bool | None = Field(default=None)
        position: float | None = Field(default=None)
        external_key: str | None = Field(validation_alias=AliasChoices('external_key', 'externalKey'), serialization_alias='externalKey', default=None)
        threads: list[ID] | None = Field(default=None)
        link: ThreadLinkInput | None = Field(default=None)

    class Meta:
        """Meta class for CreateTask """
        document = 'fragment Address on Address {\n  name\n  address\n  __typename\n}\n\nfragment ListMessage on Message {\n  id\n  subject\n  sender {\n    ...Address\n    __typename\n  }\n  date\n  receivedAt\n  snippet\n  flags\n  isRead\n  isFlagged\n  isAnswered\n  hasAttachments\n  syncState\n  account {\n    id\n    __typename\n  }\n  folder {\n    id\n    role\n    __typename\n  }\n  thread {\n    id\n    __typename\n  }\n  categories {\n    id\n    name\n    color\n    __typename\n  }\n  __typename\n}\n\nfragment ListTask on Task {\n  id\n  title\n  notes\n  status\n  pinned\n  dueAt\n  snoozedUntil\n  snoozed\n  position\n  externalKey\n  completedAt\n  createdAt\n  updatedAt\n  threadCount\n  unreadCount\n  list {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment ListThread on Thread {\n  id\n  subject\n  lastMessageAt\n  messageCount\n  unread\n  flagged\n  hasAttachments\n  participants {\n    ...Address\n    __typename\n  }\n  account {\n    id\n    __typename\n  }\n  latestMessage {\n    ...ListMessage\n    __typename\n  }\n  __typename\n}\n\nfragment TaskThread on TaskThread {\n  id\n  source\n  confidence\n  reason\n  position\n  createdAt\n  task {\n    id\n    __typename\n  }\n  thread {\n    id\n    subject\n    __typename\n  }\n  __typename\n}\n\nfragment Task on Task {\n  ...ListTask\n  links {\n    ...TaskThread\n    __typename\n  }\n  threads {\n    ...ListThread\n    __typename\n  }\n  __typename\n}\n\nmutation CreateTask($title: String!, $notes: String, $taskList: ID, $dueAt: DateTime, $pinned: Boolean, $position: Float, $externalKey: String, $threads: [ID!], $link: ThreadLinkInput) {\n  createTask(\n    input: {\n      title: $title\n      notes: $notes\n      list: $taskList\n      dueAt: $dueAt\n      pinned: $pinned\n      position: $position\n      externalKey: $externalKey\n      threads: $threads\n      link: $link\n    }\n  ) {\n    ...Task\n    __typename\n  }\n}'

class UpsertTaskMutation(BaseModel):
    """No documentation found for this operation."""
    upsert_task: Task = Field(alias='upsertTask')
    "Create or update the caller's task with this externalKey, and add conversations to it."

    class Arguments(BaseModel):
        """Arguments for UpsertTask """
        external_key: str = Field(validation_alias=AliasChoices('external_key', 'externalKey'), serialization_alias='externalKey')
        title: str
        notes: str | None = Field(default=None)
        task_list: ID | None = Field(validation_alias=AliasChoices('task_list', 'taskList'), serialization_alias='taskList', default=None)
        due_at: datetime | None = Field(validation_alias=AliasChoices('due_at', 'dueAt'), serialization_alias='dueAt', default=None)
        pinned: bool | None = Field(default=None)
        threads: list[ID] | None = Field(default=None)
        link: ThreadLinkInput | None = Field(default=None)

    class Meta:
        """Meta class for UpsertTask """
        document = 'fragment Address on Address {\n  name\n  address\n  __typename\n}\n\nfragment ListMessage on Message {\n  id\n  subject\n  sender {\n    ...Address\n    __typename\n  }\n  date\n  receivedAt\n  snippet\n  flags\n  isRead\n  isFlagged\n  isAnswered\n  hasAttachments\n  syncState\n  account {\n    id\n    __typename\n  }\n  folder {\n    id\n    role\n    __typename\n  }\n  thread {\n    id\n    __typename\n  }\n  categories {\n    id\n    name\n    color\n    __typename\n  }\n  __typename\n}\n\nfragment ListTask on Task {\n  id\n  title\n  notes\n  status\n  pinned\n  dueAt\n  snoozedUntil\n  snoozed\n  position\n  externalKey\n  completedAt\n  createdAt\n  updatedAt\n  threadCount\n  unreadCount\n  list {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment ListThread on Thread {\n  id\n  subject\n  lastMessageAt\n  messageCount\n  unread\n  flagged\n  hasAttachments\n  participants {\n    ...Address\n    __typename\n  }\n  account {\n    id\n    __typename\n  }\n  latestMessage {\n    ...ListMessage\n    __typename\n  }\n  __typename\n}\n\nfragment TaskThread on TaskThread {\n  id\n  source\n  confidence\n  reason\n  position\n  createdAt\n  task {\n    id\n    __typename\n  }\n  thread {\n    id\n    subject\n    __typename\n  }\n  __typename\n}\n\nfragment Task on Task {\n  ...ListTask\n  links {\n    ...TaskThread\n    __typename\n  }\n  threads {\n    ...ListThread\n    __typename\n  }\n  __typename\n}\n\nmutation UpsertTask($externalKey: String!, $title: String!, $notes: String, $taskList: ID, $dueAt: DateTime, $pinned: Boolean, $threads: [ID!], $link: ThreadLinkInput) {\n  upsertTask(\n    input: {\n      externalKey: $externalKey\n      title: $title\n      notes: $notes\n      list: $taskList\n      dueAt: $dueAt\n      pinned: $pinned\n      threads: $threads\n      link: $link\n    }\n  ) {\n    ...Task\n    __typename\n  }\n}'

class UpdateTaskMutation(BaseModel):
    """No documentation found for this operation."""
    update_task: Task = Field(alias='updateTask')
    'Change a task.'

    class Arguments(BaseModel):
        """Arguments for UpdateTask """
        input: UpdateTaskInput

    class Meta:
        """Meta class for UpdateTask """
        document = 'fragment Address on Address {\n  name\n  address\n  __typename\n}\n\nfragment ListMessage on Message {\n  id\n  subject\n  sender {\n    ...Address\n    __typename\n  }\n  date\n  receivedAt\n  snippet\n  flags\n  isRead\n  isFlagged\n  isAnswered\n  hasAttachments\n  syncState\n  account {\n    id\n    __typename\n  }\n  folder {\n    id\n    role\n    __typename\n  }\n  thread {\n    id\n    __typename\n  }\n  categories {\n    id\n    name\n    color\n    __typename\n  }\n  __typename\n}\n\nfragment ListTask on Task {\n  id\n  title\n  notes\n  status\n  pinned\n  dueAt\n  snoozedUntil\n  snoozed\n  position\n  externalKey\n  completedAt\n  createdAt\n  updatedAt\n  threadCount\n  unreadCount\n  list {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment ListThread on Thread {\n  id\n  subject\n  lastMessageAt\n  messageCount\n  unread\n  flagged\n  hasAttachments\n  participants {\n    ...Address\n    __typename\n  }\n  account {\n    id\n    __typename\n  }\n  latestMessage {\n    ...ListMessage\n    __typename\n  }\n  __typename\n}\n\nfragment TaskThread on TaskThread {\n  id\n  source\n  confidence\n  reason\n  position\n  createdAt\n  task {\n    id\n    __typename\n  }\n  thread {\n    id\n    subject\n    __typename\n  }\n  __typename\n}\n\nfragment Task on Task {\n  ...ListTask\n  links {\n    ...TaskThread\n    __typename\n  }\n  threads {\n    ...ListThread\n    __typename\n  }\n  __typename\n}\n\nmutation UpdateTask($input: UpdateTaskInput!) {\n  updateTask(input: $input) {\n    ...Task\n    __typename\n  }\n}'

class SetTaskStatusMutation(BaseModel):
    """No documentation found for this operation."""
    set_task_status: tuple[ListTask, ...] = Field(alias='setTaskStatus')
    'Mark tasks OPEN, DONE or DISMISSED.'

    class Arguments(BaseModel):
        """Arguments for SetTaskStatus """
        input: SetTaskStatusInput

    class Meta:
        """Meta class for SetTaskStatus """
        document = 'fragment ListTask on Task {\n  id\n  title\n  notes\n  status\n  pinned\n  dueAt\n  snoozedUntil\n  snoozed\n  position\n  externalKey\n  completedAt\n  createdAt\n  updatedAt\n  threadCount\n  unreadCount\n  list {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nmutation SetTaskStatus($input: SetTaskStatusInput!) {\n  setTaskStatus(input: $input) {\n    ...ListTask\n    __typename\n  }\n}'

class SnoozeTasksMutation(BaseModel):
    """No documentation found for this operation."""
    snooze_tasks: tuple[ListTask, ...] = Field(alias='snoozeTasks')
    'Snooze tasks until a time (null wakes them).'

    class Arguments(BaseModel):
        """Arguments for SnoozeTasks """
        input: SnoozeTasksInput

    class Meta:
        """Meta class for SnoozeTasks """
        document = 'fragment ListTask on Task {\n  id\n  title\n  notes\n  status\n  pinned\n  dueAt\n  snoozedUntil\n  snoozed\n  position\n  externalKey\n  completedAt\n  createdAt\n  updatedAt\n  threadCount\n  unreadCount\n  list {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nmutation SnoozeTasks($input: SnoozeTasksInput!) {\n  snoozeTasks(input: $input) {\n    ...ListTask\n    __typename\n  }\n}'

class DeleteTaskMutation(BaseModel):
    """No documentation found for this operation."""
    delete_task: ID = Field(alias='deleteTask')
    'Delete a task.'

    class Arguments(BaseModel):
        """Arguments for DeleteTask """
        id: ID

    class Meta:
        """Meta class for DeleteTask """
        document = 'mutation DeleteTask($id: ID!) {\n  deleteTask(id: $id)\n}'

class LinkThreadsMutation(BaseModel):
    """ Link conversations to the task `task_id`."""
    link_threads: tuple[TaskThread, ...] = Field(alias='linkThreads')
    'Put conversations into a task.'

    class Arguments(BaseModel):
        """Arguments for LinkThreads """
        task_id: ID = Field(validation_alias=AliasChoices('task_id', 'taskId'), serialization_alias='taskId')
        threads: list[ID]
        link: ThreadLinkInput | None = Field(default=None)

    class Meta:
        """Meta class for LinkThreads """
        document = 'fragment TaskThread on TaskThread {\n  id\n  source\n  confidence\n  reason\n  position\n  createdAt\n  task {\n    id\n    __typename\n  }\n  thread {\n    id\n    subject\n    __typename\n  }\n  __typename\n}\n\nmutation LinkThreads($taskId: ID!, $threads: [ID!]!, $link: ThreadLinkInput) {\n  linkThreads(input: { task: $taskId, threads: $threads, link: $link }) {\n    ...TaskThread\n    __typename\n  }\n}'

class UnlinkThreadsMutation(BaseModel):
    """No documentation found for this operation."""
    unlink_threads: Task = Field(alias='unlinkThreads')
    'Take conversations out of a task.'

    class Arguments(BaseModel):
        """Arguments for UnlinkThreads """
        task_id: ID = Field(validation_alias=AliasChoices('task_id', 'taskId'), serialization_alias='taskId')
        threads: list[ID]

    class Meta:
        """Meta class for UnlinkThreads """
        document = 'fragment Address on Address {\n  name\n  address\n  __typename\n}\n\nfragment ListMessage on Message {\n  id\n  subject\n  sender {\n    ...Address\n    __typename\n  }\n  date\n  receivedAt\n  snippet\n  flags\n  isRead\n  isFlagged\n  isAnswered\n  hasAttachments\n  syncState\n  account {\n    id\n    __typename\n  }\n  folder {\n    id\n    role\n    __typename\n  }\n  thread {\n    id\n    __typename\n  }\n  categories {\n    id\n    name\n    color\n    __typename\n  }\n  __typename\n}\n\nfragment ListTask on Task {\n  id\n  title\n  notes\n  status\n  pinned\n  dueAt\n  snoozedUntil\n  snoozed\n  position\n  externalKey\n  completedAt\n  createdAt\n  updatedAt\n  threadCount\n  unreadCount\n  list {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment ListThread on Thread {\n  id\n  subject\n  lastMessageAt\n  messageCount\n  unread\n  flagged\n  hasAttachments\n  participants {\n    ...Address\n    __typename\n  }\n  account {\n    id\n    __typename\n  }\n  latestMessage {\n    ...ListMessage\n    __typename\n  }\n  __typename\n}\n\nfragment TaskThread on TaskThread {\n  id\n  source\n  confidence\n  reason\n  position\n  createdAt\n  task {\n    id\n    __typename\n  }\n  thread {\n    id\n    subject\n    __typename\n  }\n  __typename\n}\n\nfragment Task on Task {\n  ...ListTask\n  links {\n    ...TaskThread\n    __typename\n  }\n  threads {\n    ...ListThread\n    __typename\n  }\n  __typename\n}\n\nmutation UnlinkThreads($taskId: ID!, $threads: [ID!]!) {\n  unlinkThreads(input: { task: $taskId, threads: $threads }) {\n    ...Task\n    __typename\n  }\n}'

class RequestBigfileUploadMutation(BaseModel):
    """No documentation found for this operation."""
    request_bigfile_upload: BigFileUploadGrant = Field(alias='requestBigfileUpload')
    'Request temporary S3 credentials to upload one file (an attachment to send).'

    class Arguments(BaseModel):
        """Arguments for RequestBigfileUpload """
        input: RequestBigFileUploadInput

    class Meta:
        """Meta class for RequestBigfileUpload """
        document = 'fragment BigFileUploadGrant on BigFileUploadGrant {\n  status\n  accessKey\n  secretKey\n  sessionToken\n  region\n  bucket\n  key\n  path\n  expiresIn\n  store\n  maxBytes\n  originalFileName\n  uploadFileName\n  uploadContentType\n  __typename\n}\n\nmutation RequestBigfileUpload($input: RequestBigFileUploadInput!) {\n  requestBigfileUpload(input: $input) {\n    ...BigFileUploadGrant\n    __typename\n  }\n}'

class FinishBigfileUploadMutation(BaseModel):
    """No documentation found for this operation."""
    finish_bigfile_upload: BigFileStore = Field(alias='finishBigfileUpload')
    "Finalize the caller's file upload after the client has written the object."

    class Arguments(BaseModel):
        """Arguments for FinishBigfileUpload """
        store_id: str = Field(validation_alias=AliasChoices('store_id', 'storeId'), serialization_alias='storeId')
        valid: bool | None = Field(default=None)

    class Meta:
        """Meta class for FinishBigfileUpload """
        document = 'fragment BigFileStore on BigFileStore {\n  id\n  path\n  bucket\n  key\n  sizeBytes\n  originalFileName\n  contentType\n  __typename\n}\n\nmutation FinishBigfileUpload($storeId: String!, $valid: Boolean) {\n  finishBigfileUpload(input: { storeId: $storeId, valid: $valid }) {\n    ...BigFileStore\n    __typename\n  }\n}'

class RefreshBigfileUploadMutation(BaseModel):
    """ Reissues credentials for an upload still in flight, to the same key: a write that outlives its
 credentials asks for this before they expire and carries on. Only the uploader may."""
    refresh_bigfile_upload: BigFileUploadGrant = Field(alias='refreshBigfileUpload')
    "Reissue upload credentials for a bigfile upload still in flight, to the same key, so a write that outlives its credentials carries on. Only the uploader may, never for a finished store, and never past the upload's time limit"

    class Arguments(BaseModel):
        """Arguments for RefreshBigfileUpload """
        store_id: str = Field(validation_alias=AliasChoices('store_id', 'storeId'), serialization_alias='storeId')

    class Meta:
        """Meta class for RefreshBigfileUpload """
        document = 'fragment BigFileUploadGrant on BigFileUploadGrant {\n  status\n  accessKey\n  secretKey\n  sessionToken\n  region\n  bucket\n  key\n  path\n  expiresIn\n  store\n  maxBytes\n  originalFileName\n  uploadFileName\n  uploadContentType\n  __typename\n}\n\nmutation RefreshBigfileUpload($storeId: String!) {\n  refreshBigfileUpload(input: { storeId: $storeId }) {\n    ...BigFileUploadGrant\n    __typename\n  }\n}'

class GetMailAccountQuery(BaseModel):
    """No documentation found for this operation."""
    mail_account: DetailMailAccount = Field(alias='mailAccount')
    'A mailbox by id.'

    class Arguments(BaseModel):
        """Arguments for GetMailAccount """
        id: ID

    class Meta:
        """Meta class for GetMailAccount """
        document = 'fragment MailProviderRef on MailProvider {\n  id\n  name\n  kind\n  __typename\n}\n\nfragment AuthSession on AuthSession {\n  state\n  status\n  finish\n  openUrl\n  expiresAt\n  redirectUrl\n  interval\n  userCode\n  step\n  errorCode\n  errorMessage\n  result {\n    identifier\n    id\n    label\n    __typename\n  }\n  __typename\n}\n\nfragment MailAccount on MailAccount {\n  id\n  name\n  emailAddress\n  displayName\n  provider\n  status\n  visibility\n  protocol\n  authMethod\n  capabilities\n  lastSyncedAt\n  lastError\n  lastErrorCode\n  backfillDone\n  createdAt\n  isOwner\n  canSend\n  syncing\n  unreadCount\n  pendingChanges\n  failedChanges\n  mailProvider {\n    ...MailProviderRef\n    __typename\n  }\n  __typename\n}\n\nfragment MailFolder on MailFolder {\n  id\n  path\n  name\n  role\n  selectable\n  syncEnabled\n  existsOnServer\n  totalCount\n  unreadCount\n  serverUnreadCount\n  keywordsAllowed\n  backfillDone\n  lastSyncedAt\n  account {\n    id\n    __typename\n  }\n  __typename\n}\n\nfragment DetailMailAccount on MailAccount {\n  ...MailAccount\n  incomingHost\n  incomingPort\n  incomingSecurity\n  smtpHost\n  smtpPort\n  smtpSecurity\n  username\n  saveSentCopy\n  popLeaveOnServer\n  pushSeen\n  pushFlagged\n  pushKeywords\n  pushMoves\n  pushDeletes\n  serverSideFolders\n  sharedWith {\n    id\n    sub\n    preferredUsername\n    __typename\n  }\n  folders {\n    ...MailFolder\n    __typename\n  }\n  pendingAuth {\n    ...AuthSession\n    __typename\n  }\n  __typename\n}\n\nquery GetMailAccount($id: ID!) {\n  mailAccount(id: $id) {\n    ...DetailMailAccount\n    __typename\n  }\n}'

class ListMailAccountsQuery(BaseModel):
    """No documentation found for this operation."""
    mail_accounts: tuple[MailAccount, ...] = Field(alias='mailAccounts')
    "The mailboxes the caller sees: their own, shared with them, and the organization's."

    class Arguments(BaseModel):
        """Arguments for ListMailAccounts """
        filter: MailAccountFilter | None = Field(default=None)
        pagination: OffsetPaginationInput | None = Field(default=None)

    class Meta:
        """Meta class for ListMailAccounts """
        document = 'fragment MailProviderRef on MailProvider {\n  id\n  name\n  kind\n  __typename\n}\n\nfragment MailAccount on MailAccount {\n  id\n  name\n  emailAddress\n  displayName\n  provider\n  status\n  visibility\n  protocol\n  authMethod\n  capabilities\n  lastSyncedAt\n  lastError\n  lastErrorCode\n  backfillDone\n  createdAt\n  isOwner\n  canSend\n  syncing\n  unreadCount\n  pendingChanges\n  failedChanges\n  mailProvider {\n    ...MailProviderRef\n    __typename\n  }\n  __typename\n}\n\nquery ListMailAccounts($filter: MailAccountFilter, $pagination: OffsetPaginationInput) {\n  mailAccounts(filters: $filter, pagination: $pagination) {\n    ...MailAccount\n    __typename\n  }\n}'

class MailPresetsQuery(BaseModel):
    """No documentation found for this operation."""
    mail_presets: tuple[MailPreset, ...] = Field(alias='mailPresets')
    'Server settings of well-known providers (the one for `address`, when given).'

    class Arguments(BaseModel):
        """Arguments for MailPresets """
        address: str | None = Field(default=None)

    class Meta:
        """Meta class for MailPresets """
        document = 'fragment ServerSettings on ServerSettings {\n  host\n  port\n  security\n  __typename\n}\n\nfragment MailPreset on MailPreset {\n  key\n  name\n  domains\n  provider\n  imap {\n    ...ServerSettings\n    __typename\n  }\n  pop3 {\n    ...ServerSettings\n    __typename\n  }\n  smtp {\n    ...ServerSettings\n    __typename\n  }\n  saveSentCopy\n  oauth\n  oauthConfigured\n  note\n  __typename\n}\n\nquery MailPresets($address: String) {\n  mailPresets(address: $address) {\n    ...MailPreset\n    __typename\n  }\n}'

class GetAuthSessionQuery(BaseModel):
    """No documentation found for this operation."""
    auth_session: AuthSession = Field(alias='authSession')
    'Where a login is. No side effect.'

    class Arguments(BaseModel):
        """Arguments for GetAuthSession """
        state: str

    class Meta:
        """Meta class for GetAuthSession """
        document = 'fragment AuthSession on AuthSession {\n  state\n  status\n  finish\n  openUrl\n  expiresAt\n  redirectUrl\n  interval\n  userCode\n  step\n  errorCode\n  errorMessage\n  result {\n    identifier\n    id\n    label\n    __typename\n  }\n  __typename\n}\n\nquery GetAuthSession($state: String!) {\n  authSession(state: $state) {\n    ...AuthSession\n    __typename\n  }\n}'

class SearchMailAccountsQueryOptions(BaseModel):
    """A linked mailbox. Private to the member who linked it unless shared (`visibility`)."""
    typename: Literal['MailAccount'] = Field(alias='__typename', default='MailAccount', exclude=True)
    value: ID
    label: str
    "The mailbox's address; the From of sent mail."
    model_config = ConfigDict(frozen=True)

class SearchMailAccountsQuery(BaseModel):
    """No documentation found for this operation."""
    options: tuple[SearchMailAccountsQueryOptions, ...]
    "The mailboxes the caller sees: their own, shared with them, and the organization's."

    class Arguments(BaseModel):
        """Arguments for SearchMailAccounts """
        search: str | None = Field(default=None)
        values: list[ID] | None = Field(default=None)
        limit: Annotated[int | None, GraphQLDefault('10')] = Field(default=None)
        offset: Annotated[int | None, GraphQLDefault('0')] = Field(default=None)

    class Meta:
        """Meta class for SearchMailAccounts """
        document = 'query SearchMailAccounts($search: String, $values: [ID!], $limit: Int = 10, $offset: Int = 0) {\n  options: mailAccounts(\n    filters: { search: $search, ids: $values }\n    pagination: { limit: $limit, offset: $offset }\n  ) {\n    value: id\n    label: emailAddress\n    __typename\n  }\n}'

class GetCategoryQuery(BaseModel):
    """No documentation found for this operation."""
    category: Category
    'A category by id.'

    class Arguments(BaseModel):
        """Arguments for GetCategory """
        id: ID

    class Meta:
        """Meta class for GetCategory """
        document = 'fragment Category on Category {\n  id\n  name\n  color\n  sync\n  keyword\n  createdAt\n  messageCount\n  account {\n    id\n    __typename\n  }\n  __typename\n}\n\nquery GetCategory($id: ID!) {\n  category(id: $id) {\n    ...Category\n    __typename\n  }\n}'

class ListCategoriesQuery(BaseModel):
    """No documentation found for this operation."""
    categories: tuple[Category, ...]
    'Categories of the visible mailboxes (filter by `account`).'

    class Arguments(BaseModel):
        """Arguments for ListCategories """
        filter: CategoryFilter | None = Field(default=None)
        pagination: OffsetPaginationInput | None = Field(default=None)

    class Meta:
        """Meta class for ListCategories """
        document = 'fragment Category on Category {\n  id\n  name\n  color\n  sync\n  keyword\n  createdAt\n  messageCount\n  account {\n    id\n    __typename\n  }\n  __typename\n}\n\nquery ListCategories($filter: CategoryFilter, $pagination: OffsetPaginationInput) {\n  categories(filters: $filter, pagination: $pagination) {\n    ...Category\n    __typename\n  }\n}'

class ListMailChangesQuery(BaseModel):
    """No documentation found for this operation."""
    mail_changes: tuple[MailChange, ...] = Field(alias='mailChanges')
    'Changes made here that have not reached the server yet (pending or failed), oldest first.'

    class Arguments(BaseModel):
        """Arguments for ListMailChanges """
        filter: MailChangeFilter | None = Field(default=None)
        pagination: OffsetPaginationInput | None = Field(default=None)

    class Meta:
        """Meta class for ListMailChanges """
        document = 'fragment MailChange on MailChange {\n  id\n  kind\n  state\n  add\n  remove\n  pushAfter\n  attempts\n  error\n  errorCode\n  createdAt\n  undoable\n  account {\n    id\n    __typename\n  }\n  originFolder {\n    id\n    __typename\n  }\n  targetFolder {\n    id\n    __typename\n  }\n  message {\n    id\n    __typename\n  }\n  __typename\n}\n\nquery ListMailChanges($filter: MailChangeFilter, $pagination: OffsetPaginationInput) {\n  mailChanges(filters: $filter, pagination: $pagination) {\n    ...MailChange\n    __typename\n  }\n}'

class GetMailFolderQuery(BaseModel):
    """No documentation found for this operation."""
    mail_folder: MailFolder = Field(alias='mailFolder')
    'A folder by id.'

    class Arguments(BaseModel):
        """Arguments for GetMailFolder """
        id: ID

    class Meta:
        """Meta class for GetMailFolder """
        document = 'fragment MailFolder on MailFolder {\n  id\n  path\n  name\n  role\n  selectable\n  syncEnabled\n  existsOnServer\n  totalCount\n  unreadCount\n  serverUnreadCount\n  keywordsAllowed\n  backfillDone\n  lastSyncedAt\n  account {\n    id\n    __typename\n  }\n  __typename\n}\n\nquery GetMailFolder($id: ID!) {\n  mailFolder(id: $id) {\n    ...MailFolder\n    __typename\n  }\n}'

class ListMailFoldersQuery(BaseModel):
    """No documentation found for this operation."""
    mail_folders: tuple[MailFolder, ...] = Field(alias='mailFolders')
    'Folders of the visible mailboxes (filter by `account`).'

    class Arguments(BaseModel):
        """Arguments for ListMailFolders """
        filter: MailFolderFilter | None = Field(default=None)
        pagination: OffsetPaginationInput | None = Field(default=None)

    class Meta:
        """Meta class for ListMailFolders """
        document = 'fragment MailFolder on MailFolder {\n  id\n  path\n  name\n  role\n  selectable\n  syncEnabled\n  existsOnServer\n  totalCount\n  unreadCount\n  serverUnreadCount\n  keywordsAllowed\n  backfillDone\n  lastSyncedAt\n  account {\n    id\n    __typename\n  }\n  __typename\n}\n\nquery ListMailFolders($filter: MailFolderFilter, $pagination: OffsetPaginationInput) {\n  mailFolders(filters: $filter, pagination: $pagination) {\n    ...MailFolder\n    __typename\n  }\n}'

class GetMessageQuery(BaseModel):
    """No documentation found for this operation."""
    message: Message
    'A message by id.'

    class Arguments(BaseModel):
        """Arguments for GetMessage """
        id: ID

    class Meta:
        """Meta class for GetMessage """
        document = 'fragment BigFileStore on BigFileStore {\n  id\n  path\n  bucket\n  key\n  sizeBytes\n  originalFileName\n  contentType\n  __typename\n}\n\nfragment Address on Address {\n  name\n  address\n  __typename\n}\n\nfragment Attachment on Attachment {\n  id\n  position\n  filename\n  contentType\n  size\n  contentId\n  inline\n  store {\n    ...BigFileStore\n    __typename\n  }\n  __typename\n}\n\nfragment ListMessage on Message {\n  id\n  subject\n  sender {\n    ...Address\n    __typename\n  }\n  date\n  receivedAt\n  snippet\n  flags\n  isRead\n  isFlagged\n  isAnswered\n  hasAttachments\n  syncState\n  account {\n    id\n    __typename\n  }\n  folder {\n    id\n    role\n    __typename\n  }\n  thread {\n    id\n    __typename\n  }\n  categories {\n    id\n    name\n    color\n    __typename\n  }\n  __typename\n}\n\nfragment Message on Message {\n  ...ListMessage\n  messageId\n  inReplyTo\n  references\n  textBody\n  hasRemoteImages\n  size\n  serverFlags\n  truncated\n  createdAt\n  replyTo {\n    ...Address\n    __typename\n  }\n  to {\n    ...Address\n    __typename\n  }\n  cc {\n    ...Address\n    __typename\n  }\n  bcc {\n    ...Address\n    __typename\n  }\n  attachments {\n    ...Attachment\n    __typename\n  }\n  __typename\n}\n\nquery GetMessage($id: ID!) {\n  message(id: $id) {\n    ...Message\n    __typename\n  }\n}'

class GetMessageHtmlQueryMessage(BaseModel):
    """A message in a folder. A copy in another folder is another message with the same `messageId`."""
    typename: Literal['Message'] = Field(alias='__typename', default='Message', exclude=True)
    id: ID
    html: str | None = Field(default=None)
    'The HTML body, sanitized: no scripts, styles, event handlers or forms. Remote images are removed unless `allowRemote` (loading one tells the sender the mail was read); inline images keep their `cid:` references (see `attachments.contentId`). Null for a plain-text message.'
    model_config = ConfigDict(frozen=True)

class GetMessageHtmlQuery(BaseModel):
    """No documentation found for this operation."""
    message: GetMessageHtmlQueryMessage
    'A message by id.'

    class Arguments(BaseModel):
        """Arguments for GetMessageHtml """
        id: ID
        allow_remote: Annotated[bool | None, GraphQLDefault('False')] = Field(validation_alias=AliasChoices('allow_remote', 'allowRemote'), serialization_alias='allowRemote', default=None)

    class Meta:
        """Meta class for GetMessageHtml """
        document = 'query GetMessageHtml($id: ID!, $allowRemote: Boolean! = false) {\n  message(id: $id) {\n    id\n    html(allowRemote: $allowRemote)\n    __typename\n  }\n}'

class ListMessagesQuery(BaseModel):
    """No documentation found for this operation."""
    messages: tuple[ListMessage, ...]
    'Messages of the visible mailboxes (paginated, filterable — `search` also matches by meaning — and orderable).'

    class Arguments(BaseModel):
        """Arguments for ListMessages """
        filter: MessageFilter | None = Field(default=None)
        order: list[MessageOrder] | None = Field(default=None)
        pagination: OffsetPaginationInput | None = Field(default=None)

    class Meta:
        """Meta class for ListMessages """
        document = 'fragment Address on Address {\n  name\n  address\n  __typename\n}\n\nfragment ListMessage on Message {\n  id\n  subject\n  sender {\n    ...Address\n    __typename\n  }\n  date\n  receivedAt\n  snippet\n  flags\n  isRead\n  isFlagged\n  isAnswered\n  hasAttachments\n  syncState\n  account {\n    id\n    __typename\n  }\n  folder {\n    id\n    role\n    __typename\n  }\n  thread {\n    id\n    __typename\n  }\n  categories {\n    id\n    name\n    color\n    __typename\n  }\n  __typename\n}\n\nquery ListMessages($filter: MessageFilter, $order: [MessageOrder!], $pagination: OffsetPaginationInput) {\n  messages(filters: $filter, ordering: $order, pagination: $pagination) {\n    ...ListMessage\n    __typename\n  }\n}'

class CountMessagesQuery(BaseModel):
    """No documentation found for this operation."""
    messages_count: int = Field(alias='messagesCount')
    'How many messages match the filters.'

    class Arguments(BaseModel):
        """Arguments for CountMessages """
        filter: MessageFilter | None = Field(default=None)

    class Meta:
        """Meta class for CountMessages """
        document = 'query CountMessages($filter: MessageFilter) {\n  messagesCount(filters: $filter)\n}'

class SearchMessagesQueryOptions(BaseModel):
    """A message in a folder. A copy in another folder is another message with the same `messageId`."""
    typename: Literal['Message'] = Field(alias='__typename', default='Message', exclude=True)
    value: ID
    label: str
    'The decoded subject.'
    model_config = ConfigDict(frozen=True)

class SearchMessagesQuery(BaseModel):
    """No documentation found for this operation."""
    options: tuple[SearchMessagesQueryOptions, ...]
    'Messages of the visible mailboxes (paginated, filterable — `search` also matches by meaning — and orderable).'

    class Arguments(BaseModel):
        """Arguments for SearchMessages """
        search: str | None = Field(default=None)
        values: list[ID] | None = Field(default=None)
        limit: Annotated[int | None, GraphQLDefault('10')] = Field(default=None)
        offset: Annotated[int | None, GraphQLDefault('0')] = Field(default=None)

    class Meta:
        """Meta class for SearchMessages """
        document = 'query SearchMessages($search: String, $values: [ID!], $limit: Int = 10, $offset: Int = 0) {\n  options: messages(\n    filters: { search: $search, ids: $values }\n    pagination: { limit: $limit, offset: $offset }\n  ) {\n    value: id\n    label: subject\n    __typename\n  }\n}'

class GetOutgoingMessageQuery(BaseModel):
    """No documentation found for this operation."""
    outgoing_message: OutgoingMessage = Field(alias='outgoingMessage')
    'A sent message by id.'

    class Arguments(BaseModel):
        """Arguments for GetOutgoingMessage """
        id: ID

    class Meta:
        """Meta class for GetOutgoingMessage """
        document = 'fragment Address on Address {\n  name\n  address\n  __typename\n}\n\nfragment BigFileStore on BigFileStore {\n  id\n  path\n  bucket\n  key\n  sizeBytes\n  originalFileName\n  contentType\n  __typename\n}\n\nfragment RefusedRecipient on RefusedRecipient {\n  address\n  code\n  message\n  __typename\n}\n\nfragment OutgoingMessage on OutgoingMessage {\n  id\n  status\n  subject\n  textBody\n  htmlBody\n  messageId\n  savedToSent\n  error\n  errorCode\n  createdAt\n  sentAt\n  account {\n    id\n    __typename\n  }\n  inReplyTo {\n    id\n    __typename\n  }\n  to {\n    ...Address\n    __typename\n  }\n  cc {\n    ...Address\n    __typename\n  }\n  bcc {\n    ...Address\n    __typename\n  }\n  refused {\n    ...RefusedRecipient\n    __typename\n  }\n  attachments {\n    ...BigFileStore\n    __typename\n  }\n  __typename\n}\n\nquery GetOutgoingMessage($id: ID!) {\n  outgoingMessage(id: $id) {\n    ...OutgoingMessage\n    __typename\n  }\n}'

class ListOutboxQuery(BaseModel):
    """No documentation found for this operation."""
    outbox: tuple[OutgoingMessage, ...]
    'Mail sent through the visible mailboxes, newest first.'

    class Arguments(BaseModel):
        """Arguments for ListOutbox """
        filter: OutgoingMessageFilter | None = Field(default=None)
        pagination: OffsetPaginationInput | None = Field(default=None)

    class Meta:
        """Meta class for ListOutbox """
        document = 'fragment Address on Address {\n  name\n  address\n  __typename\n}\n\nfragment BigFileStore on BigFileStore {\n  id\n  path\n  bucket\n  key\n  sizeBytes\n  originalFileName\n  contentType\n  __typename\n}\n\nfragment RefusedRecipient on RefusedRecipient {\n  address\n  code\n  message\n  __typename\n}\n\nfragment OutgoingMessage on OutgoingMessage {\n  id\n  status\n  subject\n  textBody\n  htmlBody\n  messageId\n  savedToSent\n  error\n  errorCode\n  createdAt\n  sentAt\n  account {\n    id\n    __typename\n  }\n  inReplyTo {\n    id\n    __typename\n  }\n  to {\n    ...Address\n    __typename\n  }\n  cc {\n    ...Address\n    __typename\n  }\n  bcc {\n    ...Address\n    __typename\n  }\n  refused {\n    ...RefusedRecipient\n    __typename\n  }\n  attachments {\n    ...BigFileStore\n    __typename\n  }\n  __typename\n}\n\nquery ListOutbox($filter: OutgoingMessageFilter, $pagination: OffsetPaginationInput) {\n  outbox(filters: $filter, pagination: $pagination) {\n    ...OutgoingMessage\n    __typename\n  }\n}'

class GetMailProviderQuery(BaseModel):
    """No documentation found for this operation."""
    mail_provider: MailProvider = Field(alias='mailProvider')
    'A provider by id.'

    class Arguments(BaseModel):
        """Arguments for GetMailProvider """
        id: ID

    class Meta:
        """Meta class for GetMailProvider """
        document = 'fragment MailProviderRef on MailProvider {\n  id\n  name\n  kind\n  __typename\n}\n\nfragment ProviderKind on ProviderKind {\n  kind\n  label\n  description\n  authMethod\n  capabilities {\n    capability\n    label\n    description\n    __typename\n  }\n  __typename\n}\n\nfragment ServerSettings on ServerSettings {\n  host\n  port\n  security\n  __typename\n}\n\nfragment MailProvider on MailProvider {\n  ...MailProviderRef\n  enabled\n  capabilities\n  mailboxCount\n  createdAt\n  updatedAt\n  kindInfo {\n    ...ProviderKind\n    __typename\n  }\n  oauth {\n    clientId\n    redirectUrls\n    tenant\n    hasSecret\n    __typename\n  }\n  server {\n    fixed\n    protocol\n    incoming {\n      ...ServerSettings\n      __typename\n    }\n    smtp {\n      ...ServerSettings\n      __typename\n    }\n    saveSentCopy\n    __typename\n  }\n  __typename\n}\n\nquery GetMailProvider($id: ID!) {\n  mailProvider(id: $id) {\n    ...MailProvider\n    __typename\n  }\n}'

class ListMailProvidersQuery(BaseModel):
    """No documentation found for this operation."""
    mail_providers: tuple[MailProvider, ...] = Field(alias='mailProviders')
    'The providers the organization set up; every mailbox is linked through one.'

    class Arguments(BaseModel):
        """Arguments for ListMailProviders """
        filter: MailProviderFilter | None = Field(default=None)
        pagination: OffsetPaginationInput | None = Field(default=None)

    class Meta:
        """Meta class for ListMailProviders """
        document = 'fragment MailProviderRef on MailProvider {\n  id\n  name\n  kind\n  __typename\n}\n\nfragment ProviderKind on ProviderKind {\n  kind\n  label\n  description\n  authMethod\n  capabilities {\n    capability\n    label\n    description\n    __typename\n  }\n  __typename\n}\n\nfragment ServerSettings on ServerSettings {\n  host\n  port\n  security\n  __typename\n}\n\nfragment MailProvider on MailProvider {\n  ...MailProviderRef\n  enabled\n  capabilities\n  mailboxCount\n  createdAt\n  updatedAt\n  kindInfo {\n    ...ProviderKind\n    __typename\n  }\n  oauth {\n    clientId\n    redirectUrls\n    tenant\n    hasSecret\n    __typename\n  }\n  server {\n    fixed\n    protocol\n    incoming {\n      ...ServerSettings\n      __typename\n    }\n    smtp {\n      ...ServerSettings\n      __typename\n    }\n    saveSentCopy\n    __typename\n  }\n  __typename\n}\n\nquery ListMailProviders($filter: MailProviderFilter, $pagination: OffsetPaginationInput) {\n  mailProviders(filters: $filter, pagination: $pagination) {\n    ...MailProvider\n    __typename\n  }\n}'

class ProviderKindsQuery(BaseModel):
    """No documentation found for this operation."""
    provider_kinds: tuple[ProviderKind, ...] = Field(alias='providerKinds')
    'The kinds of provider this server can run, each with its capabilities.'

    class Arguments(BaseModel):
        """Arguments for ProviderKinds """
        pass

    class Meta:
        """Meta class for ProviderKinds """
        document = 'fragment ProviderKind on ProviderKind {\n  kind\n  label\n  description\n  authMethod\n  capabilities {\n    capability\n    label\n    description\n    __typename\n  }\n  __typename\n}\n\nquery ProviderKinds {\n  providerKinds {\n    ...ProviderKind\n    __typename\n  }\n}'

class GetTaskQuery(BaseModel):
    """No documentation found for this operation."""
    task: Task
    'A task by id.'

    class Arguments(BaseModel):
        """Arguments for GetTask """
        id: ID

    class Meta:
        """Meta class for GetTask """
        document = 'fragment Address on Address {\n  name\n  address\n  __typename\n}\n\nfragment ListMessage on Message {\n  id\n  subject\n  sender {\n    ...Address\n    __typename\n  }\n  date\n  receivedAt\n  snippet\n  flags\n  isRead\n  isFlagged\n  isAnswered\n  hasAttachments\n  syncState\n  account {\n    id\n    __typename\n  }\n  folder {\n    id\n    role\n    __typename\n  }\n  thread {\n    id\n    __typename\n  }\n  categories {\n    id\n    name\n    color\n    __typename\n  }\n  __typename\n}\n\nfragment ListTask on Task {\n  id\n  title\n  notes\n  status\n  pinned\n  dueAt\n  snoozedUntil\n  snoozed\n  position\n  externalKey\n  completedAt\n  createdAt\n  updatedAt\n  threadCount\n  unreadCount\n  list {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment ListThread on Thread {\n  id\n  subject\n  lastMessageAt\n  messageCount\n  unread\n  flagged\n  hasAttachments\n  participants {\n    ...Address\n    __typename\n  }\n  account {\n    id\n    __typename\n  }\n  latestMessage {\n    ...ListMessage\n    __typename\n  }\n  __typename\n}\n\nfragment TaskThread on TaskThread {\n  id\n  source\n  confidence\n  reason\n  position\n  createdAt\n  task {\n    id\n    __typename\n  }\n  thread {\n    id\n    subject\n    __typename\n  }\n  __typename\n}\n\nfragment Task on Task {\n  ...ListTask\n  links {\n    ...TaskThread\n    __typename\n  }\n  threads {\n    ...ListThread\n    __typename\n  }\n  __typename\n}\n\nquery GetTask($id: ID!) {\n  task(id: $id) {\n    ...Task\n    __typename\n  }\n}'

class ListTasksQuery(BaseModel):
    """No documentation found for this operation."""
    tasks: tuple[ListTask, ...]
    "The caller's tasks (paginated, filterable — `active` is the Inbox view — and orderable)."

    class Arguments(BaseModel):
        """Arguments for ListTasks """
        filter: TaskFilter | None = Field(default=None)
        order: list[TaskOrder] | None = Field(default=None)
        pagination: OffsetPaginationInput | None = Field(default=None)

    class Meta:
        """Meta class for ListTasks """
        document = 'fragment ListTask on Task {\n  id\n  title\n  notes\n  status\n  pinned\n  dueAt\n  snoozedUntil\n  snoozed\n  position\n  externalKey\n  completedAt\n  createdAt\n  updatedAt\n  threadCount\n  unreadCount\n  list {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nquery ListTasks($filter: TaskFilter, $order: [TaskOrder!], $pagination: OffsetPaginationInput) {\n  tasks(filters: $filter, ordering: $order, pagination: $pagination) {\n    ...ListTask\n    __typename\n  }\n}'

class CountTasksQuery(BaseModel):
    """No documentation found for this operation."""
    tasks_count: int = Field(alias='tasksCount')
    "How many of the caller's tasks match the filters."

    class Arguments(BaseModel):
        """Arguments for CountTasks """
        filter: TaskFilter | None = Field(default=None)

    class Meta:
        """Meta class for CountTasks """
        document = 'query CountTasks($filter: TaskFilter) {\n  tasksCount(filters: $filter)\n}'

class GetTaskListQuery(BaseModel):
    """No documentation found for this operation."""
    task_list: TaskList = Field(alias='taskList')
    'A task list by id.'

    class Arguments(BaseModel):
        """Arguments for GetTaskList """
        id: ID

    class Meta:
        """Meta class for GetTaskList """
        document = 'fragment TaskList on TaskList {\n  id\n  name\n  color\n  position\n  createdAt\n  openCount\n  __typename\n}\n\nquery GetTaskList($id: ID!) {\n  taskList(id: $id) {\n    ...TaskList\n    __typename\n  }\n}'

class ListTaskListsQuery(BaseModel):
    """No documentation found for this operation."""
    task_lists: tuple[TaskList, ...] = Field(alias='taskLists')
    "The caller's task lists."

    class Arguments(BaseModel):
        """Arguments for ListTaskLists """
        filter: TaskListFilter | None = Field(default=None)
        pagination: OffsetPaginationInput | None = Field(default=None)

    class Meta:
        """Meta class for ListTaskLists """
        document = 'fragment TaskList on TaskList {\n  id\n  name\n  color\n  position\n  createdAt\n  openCount\n  __typename\n}\n\nquery ListTaskLists($filter: TaskListFilter, $pagination: OffsetPaginationInput) {\n  taskLists(filters: $filter, pagination: $pagination) {\n    ...TaskList\n    __typename\n  }\n}'

class SearchTasksQueryOptions(BaseModel):
    """Something to do, made of mail conversations from any mailbox its owner can see. Only its owner sees it. Its status is independent of the mail: finishing a task changes no message."""
    typename: Literal['Task'] = Field(alias='__typename', default='Task', exclude=True)
    value: ID
    label: str
    'What to do.'
    model_config = ConfigDict(frozen=True)

class SearchTasksQuery(BaseModel):
    """No documentation found for this operation."""
    options: tuple[SearchTasksQueryOptions, ...]
    "The caller's tasks (paginated, filterable — `active` is the Inbox view — and orderable)."

    class Arguments(BaseModel):
        """Arguments for SearchTasks """
        search: str | None = Field(default=None)
        values: list[ID] | None = Field(default=None)
        limit: Annotated[int | None, GraphQLDefault('10')] = Field(default=None)
        offset: Annotated[int | None, GraphQLDefault('0')] = Field(default=None)

    class Meta:
        """Meta class for SearchTasks """
        document = 'query SearchTasks($search: String, $values: [ID!], $limit: Int = 10, $offset: Int = 0) {\n  options: tasks(\n    filters: { search: $search, ids: $values }\n    pagination: { limit: $limit, offset: $offset }\n  ) {\n    value: id\n    label: title\n    __typename\n  }\n}'

class SearchTaskListsQueryOptions(BaseModel):
    """A member's list of tasks (an Inbox bundle or project). Only its owner sees it."""
    typename: Literal['TaskList'] = Field(alias='__typename', default='TaskList', exclude=True)
    value: ID
    label: str
    "The list's name."
    model_config = ConfigDict(frozen=True)

class SearchTaskListsQuery(BaseModel):
    """No documentation found for this operation."""
    options: tuple[SearchTaskListsQueryOptions, ...]
    "The caller's task lists."

    class Arguments(BaseModel):
        """Arguments for SearchTaskLists """
        search: str | None = Field(default=None)
        values: list[ID] | None = Field(default=None)
        limit: Annotated[int | None, GraphQLDefault('10')] = Field(default=None)
        offset: Annotated[int | None, GraphQLDefault('0')] = Field(default=None)

    class Meta:
        """Meta class for SearchTaskLists """
        document = 'query SearchTaskLists($search: String, $values: [ID!], $limit: Int = 10, $offset: Int = 0) {\n  options: taskLists(\n    filters: { search: $search, ids: $values }\n    pagination: { limit: $limit, offset: $offset }\n  ) {\n    value: id\n    label: name\n    __typename\n  }\n}'

class GetThreadQuery(BaseModel):
    """No documentation found for this operation."""
    thread: Thread
    'A conversation by id.'

    class Arguments(BaseModel):
        """Arguments for GetThread """
        id: ID

    class Meta:
        """Meta class for GetThread """
        document = 'fragment Address on Address {\n  name\n  address\n  __typename\n}\n\nfragment ListMessage on Message {\n  id\n  subject\n  sender {\n    ...Address\n    __typename\n  }\n  date\n  receivedAt\n  snippet\n  flags\n  isRead\n  isFlagged\n  isAnswered\n  hasAttachments\n  syncState\n  account {\n    id\n    __typename\n  }\n  folder {\n    id\n    role\n    __typename\n  }\n  thread {\n    id\n    __typename\n  }\n  categories {\n    id\n    name\n    color\n    __typename\n  }\n  __typename\n}\n\nfragment ListTask on Task {\n  id\n  title\n  notes\n  status\n  pinned\n  dueAt\n  snoozedUntil\n  snoozed\n  position\n  externalKey\n  completedAt\n  createdAt\n  updatedAt\n  threadCount\n  unreadCount\n  list {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment ListThread on Thread {\n  id\n  subject\n  lastMessageAt\n  messageCount\n  unread\n  flagged\n  hasAttachments\n  participants {\n    ...Address\n    __typename\n  }\n  account {\n    id\n    __typename\n  }\n  latestMessage {\n    ...ListMessage\n    __typename\n  }\n  __typename\n}\n\nfragment Thread on Thread {\n  ...ListThread\n  messages {\n    ...ListMessage\n    __typename\n  }\n  tasks {\n    ...ListTask\n    __typename\n  }\n  __typename\n}\n\nquery GetThread($id: ID!) {\n  thread(id: $id) {\n    ...Thread\n    __typename\n  }\n}'

class ListThreadsQuery(BaseModel):
    """No documentation found for this operation."""
    threads: tuple[ListThread, ...]
    'Conversations of the visible mailboxes (paginated, filterable, orderable).'

    class Arguments(BaseModel):
        """Arguments for ListThreads """
        filter: ThreadFilter | None = Field(default=None)
        order: list[ThreadOrder] | None = Field(default=None)
        pagination: OffsetPaginationInput | None = Field(default=None)

    class Meta:
        """Meta class for ListThreads """
        document = 'fragment Address on Address {\n  name\n  address\n  __typename\n}\n\nfragment ListMessage on Message {\n  id\n  subject\n  sender {\n    ...Address\n    __typename\n  }\n  date\n  receivedAt\n  snippet\n  flags\n  isRead\n  isFlagged\n  isAnswered\n  hasAttachments\n  syncState\n  account {\n    id\n    __typename\n  }\n  folder {\n    id\n    role\n    __typename\n  }\n  thread {\n    id\n    __typename\n  }\n  categories {\n    id\n    name\n    color\n    __typename\n  }\n  __typename\n}\n\nfragment ListThread on Thread {\n  id\n  subject\n  lastMessageAt\n  messageCount\n  unread\n  flagged\n  hasAttachments\n  participants {\n    ...Address\n    __typename\n  }\n  account {\n    id\n    __typename\n  }\n  latestMessage {\n    ...ListMessage\n    __typename\n  }\n  __typename\n}\n\nquery ListThreads($filter: ThreadFilter, $order: [ThreadOrder!], $pagination: OffsetPaginationInput) {\n  threads(filters: $filter, ordering: $order, pagination: $pagination) {\n    ...ListThread\n    __typename\n  }\n}'

class CountThreadsQuery(BaseModel):
    """No documentation found for this operation."""
    threads_count: int = Field(alias='threadsCount')
    'How many conversations match the filters (for a list header).'

    class Arguments(BaseModel):
        """Arguments for CountThreads """
        filter: ThreadFilter | None = Field(default=None)

    class Meta:
        """Meta class for CountThreads """
        document = 'query CountThreads($filter: ThreadFilter) {\n  threadsCount(filters: $filter)\n}'

class SearchThreadsQueryOptions(BaseModel):
    """A conversation: messages linked by In-Reply-To/References, across the mailbox's folders."""
    typename: Literal['Thread'] = Field(alias='__typename', default='Thread', exclude=True)
    value: ID
    label: str
    'The subject without Re:/Fwd: prefixes.'
    model_config = ConfigDict(frozen=True)

class SearchThreadsQuery(BaseModel):
    """No documentation found for this operation."""
    options: tuple[SearchThreadsQueryOptions, ...]
    'Conversations of the visible mailboxes (paginated, filterable, orderable).'

    class Arguments(BaseModel):
        """Arguments for SearchThreads """
        search: str | None = Field(default=None)
        values: list[ID] | None = Field(default=None)
        limit: Annotated[int | None, GraphQLDefault('10')] = Field(default=None)
        offset: Annotated[int | None, GraphQLDefault('0')] = Field(default=None)

    class Meta:
        """Meta class for SearchThreads """
        document = 'query SearchThreads($search: String, $values: [ID!], $limit: Int = 10, $offset: Int = 0) {\n  options: threads(\n    filters: { search: $search, ids: $values }\n    pagination: { limit: $limit, offset: $offset }\n  ) {\n    value: id\n    label: subject\n    __typename\n  }\n}'

class WatchMailboxSyncsSubscription(BaseModel):
    """No documentation found for this operation."""
    mailbox_syncs: MailboxSyncEvent = Field(alias='mailboxSyncs')
    'Events whenever a visible mailbox finished syncing.'

    class Arguments(BaseModel):
        """Arguments for WatchMailboxSyncs """
        pass

    class Meta:
        """Meta class for WatchMailboxSyncs """
        document = 'fragment MailboxSyncEvent on MailboxSyncEvent {\n  accountId\n  created\n  updated\n  deleted\n  more\n  folders\n  __typename\n}\n\nsubscription WatchMailboxSyncs {\n  mailboxSyncs {\n    ...MailboxSyncEvent\n    __typename\n  }\n}'

class KuvertApi:
    """Every operation of this API as a method. Generated by turms.

Each method hands its operation to ``execute``, ``aexecute``, ``subscribe``, ``asubscribe`` of ``self``, which the class this one is mixed into (or a base of it) provides."""
    __scopes__: ClassVar[tuple[str, ...]] = ('kuvert_mailboxes', 'kuvert_providers', 'kuvert_read', 'kuvert_send', 'kuvert_write')

    async def acreate_mail_account(self, provider: IDCoercible, email_address: str, password: str, name: str | None | UnsetType=UNSET, display_name: str | None | UnsetType=UNSET, protocol: Protocol | None | UnsetType=UNSET, incoming: ServerInput | None | UnsetType=UNSET, smtp: ServerInput | None | UnsetType=UNSET, username: str | None | UnsetType=UNSET, smtp_username: str | None | UnsetType=UNSET, smtp_password: str | None | UnsetType=UNSET, save_sent_copy: bool | None | UnsetType=UNSET, pop_leave_on_server: bool | None | UnsetType=UNSET, visibility: Visibility | None | UnsetType=UNSET, task: TaskLike | None=None) -> DetailMailAccount:
        """CreateMailAccount 

Link a mailbox with a username and (app) password through an IMAP provider; the login is tested first.

Args:
    provider (ID): No description
    email_address (str): No description
    password (str): No description
    name (str | None, optional): No description. 
    display_name (str | None, optional): No description. 
    protocol (Protocol | None, optional): No description. 
    incoming (ServerInput | None, optional): No description. 
    smtp (ServerInput | None, optional): No description. 
    username (str | None, optional): No description. 
    smtp_username (str | None, optional): No description. 
    smtp_password (str | None, optional): No description. 
    save_sent_copy (bool | None, optional): No description. 
    pop_leave_on_server (bool | None, optional): No description. 
    visibility (Visibility | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    DetailMailAccount
"""
        variables: dict[str, builtins.object] = {}
        variables['provider'] = provider
        variables['emailAddress'] = email_address
        variables['password'] = password
        if name is not UNSET:
            variables['name'] = name
        if display_name is not UNSET:
            variables['displayName'] = display_name
        if protocol is not UNSET:
            variables['protocol'] = protocol
        if incoming is not UNSET:
            variables['incoming'] = incoming
        if smtp is not UNSET:
            variables['smtp'] = smtp
        if username is not UNSET:
            variables['username'] = username
        if smtp_username is not UNSET:
            variables['smtpUsername'] = smtp_username
        if smtp_password is not UNSET:
            variables['smtpPassword'] = smtp_password
        if save_sent_copy is not UNSET:
            variables['saveSentCopy'] = save_sent_copy
        if pop_leave_on_server is not UNSET:
            variables['popLeaveOnServer'] = pop_leave_on_server
        if visibility is not UNSET:
            variables['visibility'] = visibility
        return (await self.aexecute(CreateMailAccountMutation, variables, task=task)).create_mail_account

    def create_mail_account(self, provider: IDCoercible, email_address: str, password: str, name: str | None | UnsetType=UNSET, display_name: str | None | UnsetType=UNSET, protocol: Protocol | None | UnsetType=UNSET, incoming: ServerInput | None | UnsetType=UNSET, smtp: ServerInput | None | UnsetType=UNSET, username: str | None | UnsetType=UNSET, smtp_username: str | None | UnsetType=UNSET, smtp_password: str | None | UnsetType=UNSET, save_sent_copy: bool | None | UnsetType=UNSET, pop_leave_on_server: bool | None | UnsetType=UNSET, visibility: Visibility | None | UnsetType=UNSET, task: TaskLike | None=None) -> DetailMailAccount:
        """CreateMailAccount 

Link a mailbox with a username and (app) password through an IMAP provider; the login is tested first.

Args:
    provider (ID): No description
    email_address (str): No description
    password (str): No description
    name (str | None, optional): No description. 
    display_name (str | None, optional): No description. 
    protocol (Protocol | None, optional): No description. 
    incoming (ServerInput | None, optional): No description. 
    smtp (ServerInput | None, optional): No description. 
    username (str | None, optional): No description. 
    smtp_username (str | None, optional): No description. 
    smtp_password (str | None, optional): No description. 
    save_sent_copy (bool | None, optional): No description. 
    pop_leave_on_server (bool | None, optional): No description. 
    visibility (Visibility | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    DetailMailAccount
"""
        variables: dict[str, builtins.object] = {}
        variables['provider'] = provider
        variables['emailAddress'] = email_address
        variables['password'] = password
        if name is not UNSET:
            variables['name'] = name
        if display_name is not UNSET:
            variables['displayName'] = display_name
        if protocol is not UNSET:
            variables['protocol'] = protocol
        if incoming is not UNSET:
            variables['incoming'] = incoming
        if smtp is not UNSET:
            variables['smtp'] = smtp
        if username is not UNSET:
            variables['username'] = username
        if smtp_username is not UNSET:
            variables['smtpUsername'] = smtp_username
        if smtp_password is not UNSET:
            variables['smtpPassword'] = smtp_password
        if save_sent_copy is not UNSET:
            variables['saveSentCopy'] = save_sent_copy
        if pop_leave_on_server is not UNSET:
            variables['popLeaveOnServer'] = pop_leave_on_server
        if visibility is not UNSET:
            variables['visibility'] = visibility
        return self.execute(CreateMailAccountMutation, variables, task=task).create_mail_account

    async def aupdate_mail_account(self, id: IDCoercible, name: str | None | UnsetType=UNSET, display_name: str | None | UnsetType=UNSET, password: str | None | UnsetType=UNSET, username: str | None | UnsetType=UNSET, incoming: ServerInput | None | UnsetType=UNSET, smtp: ServerInput | None | UnsetType=UNSET, smtp_username: str | None | UnsetType=UNSET, smtp_password: str | None | UnsetType=UNSET, save_sent_copy: bool | None | UnsetType=UNSET, pop_leave_on_server: bool | None | UnsetType=UNSET, enabled: bool | None | UnsetType=UNSET, push_seen: bool | None | UnsetType=UNSET, push_flagged: bool | None | UnsetType=UNSET, push_keywords: bool | None | UnsetType=UNSET, push_moves: bool | None | UnsetType=UNSET, push_deletes: bool | None | UnsetType=UNSET, task: TaskLike | None=None) -> DetailMailAccount:
        """UpdateMailAccount 

Change a mailbox (owner only); new servers or credentials are tested first.

Args:
    id: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    display_name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    password: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    username: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    incoming: Where a server is reached.
    smtp: Where a server is reached.
    smtp_username: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    smtp_password: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    save_sent_copy: The `Boolean` scalar type represents `true` or `false`.
    pop_leave_on_server: The `Boolean` scalar type represents `true` or `false`.
    enabled: False pauses the mailbox (DISABLED); true makes it ACTIVE again (after a successful login).
    push_seen: Push read/unread to the server. Off keeps it here; turning it on pushes what was kept.
    push_flagged: Push flagging to the server. Off keeps it here.
    push_keywords: Push keywords (KEYWORD categories) to the server. Off keeps them here.
    push_moves: Push moves and archiving. Off refuses moves (a folder only exists on the server).
    push_deletes: Push deletes. Off only hides deleted mail here.
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    DetailMailAccount
"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input['id'] = id
        if name is not UNSET:
            _input['name'] = name
        if display_name is not UNSET:
            _input['displayName'] = display_name
        if password is not UNSET:
            _input['password'] = password
        if username is not UNSET:
            _input['username'] = username
        if incoming is not UNSET:
            _input['incoming'] = incoming
        if smtp is not UNSET:
            _input['smtp'] = smtp
        if smtp_username is not UNSET:
            _input['smtpUsername'] = smtp_username
        if smtp_password is not UNSET:
            _input['smtpPassword'] = smtp_password
        if save_sent_copy is not UNSET:
            _input['saveSentCopy'] = save_sent_copy
        if pop_leave_on_server is not UNSET:
            _input['popLeaveOnServer'] = pop_leave_on_server
        if enabled is not UNSET:
            _input['enabled'] = enabled
        if push_seen is not UNSET:
            _input['pushSeen'] = push_seen
        if push_flagged is not UNSET:
            _input['pushFlagged'] = push_flagged
        if push_keywords is not UNSET:
            _input['pushKeywords'] = push_keywords
        if push_moves is not UNSET:
            _input['pushMoves'] = push_moves
        if push_deletes is not UNSET:
            _input['pushDeletes'] = push_deletes
        variables['input'] = _input
        return (await self.aexecute(UpdateMailAccountMutation, variables, task=task)).update_mail_account

    def update_mail_account(self, id: IDCoercible, name: str | None | UnsetType=UNSET, display_name: str | None | UnsetType=UNSET, password: str | None | UnsetType=UNSET, username: str | None | UnsetType=UNSET, incoming: ServerInput | None | UnsetType=UNSET, smtp: ServerInput | None | UnsetType=UNSET, smtp_username: str | None | UnsetType=UNSET, smtp_password: str | None | UnsetType=UNSET, save_sent_copy: bool | None | UnsetType=UNSET, pop_leave_on_server: bool | None | UnsetType=UNSET, enabled: bool | None | UnsetType=UNSET, push_seen: bool | None | UnsetType=UNSET, push_flagged: bool | None | UnsetType=UNSET, push_keywords: bool | None | UnsetType=UNSET, push_moves: bool | None | UnsetType=UNSET, push_deletes: bool | None | UnsetType=UNSET, task: TaskLike | None=None) -> DetailMailAccount:
        """UpdateMailAccount 

Change a mailbox (owner only); new servers or credentials are tested first.

Args:
    id: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    display_name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    password: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    username: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    incoming: Where a server is reached.
    smtp: Where a server is reached.
    smtp_username: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    smtp_password: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    save_sent_copy: The `Boolean` scalar type represents `true` or `false`.
    pop_leave_on_server: The `Boolean` scalar type represents `true` or `false`.
    enabled: False pauses the mailbox (DISABLED); true makes it ACTIVE again (after a successful login).
    push_seen: Push read/unread to the server. Off keeps it here; turning it on pushes what was kept.
    push_flagged: Push flagging to the server. Off keeps it here.
    push_keywords: Push keywords (KEYWORD categories) to the server. Off keeps them here.
    push_moves: Push moves and archiving. Off refuses moves (a folder only exists on the server).
    push_deletes: Push deletes. Off only hides deleted mail here.
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    DetailMailAccount
"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input['id'] = id
        if name is not UNSET:
            _input['name'] = name
        if display_name is not UNSET:
            _input['displayName'] = display_name
        if password is not UNSET:
            _input['password'] = password
        if username is not UNSET:
            _input['username'] = username
        if incoming is not UNSET:
            _input['incoming'] = incoming
        if smtp is not UNSET:
            _input['smtp'] = smtp
        if smtp_username is not UNSET:
            _input['smtpUsername'] = smtp_username
        if smtp_password is not UNSET:
            _input['smtpPassword'] = smtp_password
        if save_sent_copy is not UNSET:
            _input['saveSentCopy'] = save_sent_copy
        if pop_leave_on_server is not UNSET:
            _input['popLeaveOnServer'] = pop_leave_on_server
        if enabled is not UNSET:
            _input['enabled'] = enabled
        if push_seen is not UNSET:
            _input['pushSeen'] = push_seen
        if push_flagged is not UNSET:
            _input['pushFlagged'] = push_flagged
        if push_keywords is not UNSET:
            _input['pushKeywords'] = push_keywords
        if push_moves is not UNSET:
            _input['pushMoves'] = push_moves
        if push_deletes is not UNSET:
            _input['pushDeletes'] = push_deletes
        variables['input'] = _input
        return self.execute(UpdateMailAccountMutation, variables, task=task).update_mail_account

    async def ashare_mail_account(self, id: IDCoercible, visibility: Visibility, users: Iterable[IDCoercible] | None | UnsetType=UNSET, task: TaskLike | None=None) -> DetailMailAccount:
        """ShareMailAccount 

Set who sees a mailbox (owner only).

Args:
    id: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    visibility: Visibility (required)
    users: The members a SHARED mailbox is shared with (replaces the list). Must be members of the organization.
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    DetailMailAccount
"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input['id'] = id
        _input['visibility'] = visibility
        if users is not UNSET:
            _input['users'] = users
        variables['input'] = _input
        return (await self.aexecute(ShareMailAccountMutation, variables, task=task)).share_mail_account

    def share_mail_account(self, id: IDCoercible, visibility: Visibility, users: Iterable[IDCoercible] | None | UnsetType=UNSET, task: TaskLike | None=None) -> DetailMailAccount:
        """ShareMailAccount 

Set who sees a mailbox (owner only).

Args:
    id: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    visibility: Visibility (required)
    users: The members a SHARED mailbox is shared with (replaces the list). Must be members of the organization.
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    DetailMailAccount
"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input['id'] = id
        _input['visibility'] = visibility
        if users is not UNSET:
            _input['users'] = users
        variables['input'] = _input
        return self.execute(ShareMailAccountMutation, variables, task=task).share_mail_account

    async def atest_mail_account(self, id: IDCoercible, task: TaskLike | None=None) -> MailAccount:
        """TestMailAccount 

Log in to a mailbox's servers now.

Args:
    id (ID): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    MailAccount
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        return (await self.aexecute(TestMailAccountMutation, variables, task=task)).test_mail_account

    def test_mail_account(self, id: IDCoercible, task: TaskLike | None=None) -> MailAccount:
        """TestMailAccount 

Log in to a mailbox's servers now.

Args:
    id (ID): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    MailAccount
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        return self.execute(TestMailAccountMutation, variables, task=task).test_mail_account

    async def adelete_mail_account(self, id: IDCoercible, task: TaskLike | None=None) -> ID:
        """DeleteMailAccount 

Unlink a mailbox (owner only). Mail on the server is untouched.

Args:
    id (ID): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    ID
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        return (await self.aexecute(DeleteMailAccountMutation, variables, task=task)).delete_mail_account

    def delete_mail_account(self, id: IDCoercible, task: TaskLike | None=None) -> ID:
        """DeleteMailAccount 

Unlink a mailbox (owner only). Mail on the server is untouched.

Args:
    id (ID): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    ID
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        return self.execute(DeleteMailAccountMutation, variables, task=task).delete_mail_account

    async def async_mail_account(self, id: IDCoercible, folders: list[IDCoercible] | None | UnsetType=UNSET, task: TaskLike | None=None) -> SyncResult:
        """SyncMailAccount 

Sync a mailbox now.

Args:
    id (ID): No description
    folders (list[ID] | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    SyncResult
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        if folders is not UNSET:
            variables['folders'] = folders
        return (await self.aexecute(SyncMailAccountMutation, variables, task=task)).sync_mail_account

    def sync_mail_account(self, id: IDCoercible, folders: list[IDCoercible] | None | UnsetType=UNSET, task: TaskLike | None=None) -> SyncResult:
        """SyncMailAccount 

Sync a mailbox now.

Args:
    id (ID): No description
    folders (list[ID] | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    SyncResult
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        if folders is not UNSET:
            variables['folders'] = folders
        return self.execute(SyncMailAccountMutation, variables, task=task).sync_mail_account

    async def apush_mail_changes(self, account: IDCoercible, task: TaskLike | None=None) -> PushResult:
        """PushMailChanges 

Push a mailbox's due changes now.

Args:
    account (ID): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    PushResult
"""
        variables: dict[str, builtins.object] = {}
        variables['account'] = account
        return (await self.aexecute(PushMailChangesMutation, variables, task=task)).push_mail_changes

    def push_mail_changes(self, account: IDCoercible, task: TaskLike | None=None) -> PushResult:
        """PushMailChanges 

Push a mailbox's due changes now.

Args:
    account (ID): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    PushResult
"""
        variables: dict[str, builtins.object] = {}
        variables['account'] = account
        return self.execute(PushMailChangesMutation, variables, task=task).push_mail_changes

    async def acreate_category(self, account: IDCoercible, name: str, color: str | None | UnsetType=UNSET, sync: CategorySync | None | UnsetType=UNSET, keyword: str | None | UnsetType=UNSET, task: TaskLike | None=None) -> Category:
        """CreateCategory 

Create a category of a mailbox.

Args:
    account (ID): No description
    name (str): No description
    color (str | None, optional): No description. 
    sync (CategorySync | None, optional): No description. 
    keyword (str | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    Category
"""
        variables: dict[str, builtins.object] = {}
        variables['account'] = account
        variables['name'] = name
        if color is not UNSET:
            variables['color'] = color
        if sync is not UNSET:
            variables['sync'] = sync
        if keyword is not UNSET:
            variables['keyword'] = keyword
        return (await self.aexecute(CreateCategoryMutation, variables, task=task)).create_category

    def create_category(self, account: IDCoercible, name: str, color: str | None | UnsetType=UNSET, sync: CategorySync | None | UnsetType=UNSET, keyword: str | None | UnsetType=UNSET, task: TaskLike | None=None) -> Category:
        """CreateCategory 

Create a category of a mailbox.

Args:
    account (ID): No description
    name (str): No description
    color (str | None, optional): No description. 
    sync (CategorySync | None, optional): No description. 
    keyword (str | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    Category
"""
        variables: dict[str, builtins.object] = {}
        variables['account'] = account
        variables['name'] = name
        if color is not UNSET:
            variables['color'] = color
        if sync is not UNSET:
            variables['sync'] = sync
        if keyword is not UNSET:
            variables['keyword'] = keyword
        return self.execute(CreateCategoryMutation, variables, task=task).create_category

    async def aupdate_category(self, id: IDCoercible, name: str | None | UnsetType=UNSET, color: str | None | UnsetType=UNSET, sync: CategorySync | None | UnsetType=UNSET, keyword: str | None | UnsetType=UNSET, remove_keywords: bool | None | UnsetType=UNSET, task: TaskLike | None=None) -> Category:
        """UpdateCategory 

Change a category.

Args:
    id (ID): No description
    name (str | None, optional): No description. 
    color (str | None, optional): No description. 
    sync (CategorySync | None, optional): No description. 
    keyword (str | None, optional): No description. 
    remove_keywords (bool | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    Category
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        if name is not UNSET:
            variables['name'] = name
        if color is not UNSET:
            variables['color'] = color
        if sync is not UNSET:
            variables['sync'] = sync
        if keyword is not UNSET:
            variables['keyword'] = keyword
        if remove_keywords is not UNSET:
            variables['removeKeywords'] = remove_keywords
        return (await self.aexecute(UpdateCategoryMutation, variables, task=task)).update_category

    def update_category(self, id: IDCoercible, name: str | None | UnsetType=UNSET, color: str | None | UnsetType=UNSET, sync: CategorySync | None | UnsetType=UNSET, keyword: str | None | UnsetType=UNSET, remove_keywords: bool | None | UnsetType=UNSET, task: TaskLike | None=None) -> Category:
        """UpdateCategory 

Change a category.

Args:
    id (ID): No description
    name (str | None, optional): No description. 
    color (str | None, optional): No description. 
    sync (CategorySync | None, optional): No description. 
    keyword (str | None, optional): No description. 
    remove_keywords (bool | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    Category
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        if name is not UNSET:
            variables['name'] = name
        if color is not UNSET:
            variables['color'] = color
        if sync is not UNSET:
            variables['sync'] = sync
        if keyword is not UNSET:
            variables['keyword'] = keyword
        if remove_keywords is not UNSET:
            variables['removeKeywords'] = remove_keywords
        return self.execute(UpdateCategoryMutation, variables, task=task).update_category

    async def adelete_category(self, id: IDCoercible, remove_keywords: bool | UnsetType=UNSET, task: TaskLike | None=None) -> ID:
        """DeleteCategory 

Delete a category.

Args:
    id (ID): No description
    remove_keywords (bool, optional): No description. Defaults to False
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    ID
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        if remove_keywords is not UNSET:
            variables['removeKeywords'] = remove_keywords
        return (await self.aexecute(DeleteCategoryMutation, variables, task=task)).delete_category

    def delete_category(self, id: IDCoercible, remove_keywords: bool | UnsetType=UNSET, task: TaskLike | None=None) -> ID:
        """DeleteCategory 

Delete a category.

Args:
    id (ID): No description
    remove_keywords (bool, optional): No description. Defaults to False
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    ID
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        if remove_keywords is not UNSET:
            variables['removeKeywords'] = remove_keywords
        return self.execute(DeleteCategoryMutation, variables, task=task).delete_category

    async def aupdate_mail_folder(self, id: IDCoercible, sync_enabled: bool, task: TaskLike | None=None) -> MailFolder:
        """UpdateMailFolder 

Turn syncing a folder on or off.

Args:
    id: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    sync_enabled: Whether syncs read the folder. Turning it off keeps what is stored.
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    MailFolder
"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input['id'] = id
        _input['syncEnabled'] = sync_enabled
        variables['input'] = _input
        return (await self.aexecute(UpdateMailFolderMutation, variables, task=task)).update_mail_folder

    def update_mail_folder(self, id: IDCoercible, sync_enabled: bool, task: TaskLike | None=None) -> MailFolder:
        """UpdateMailFolder 

Turn syncing a folder on or off.

Args:
    id: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    sync_enabled: Whether syncs read the folder. Turning it off keeps what is stored.
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    MailFolder
"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input['id'] = id
        _input['syncEnabled'] = sync_enabled
        variables['input'] = _input
        return self.execute(UpdateMailFolderMutation, variables, task=task).update_mail_folder

    async def aset_message_flags(self, messages: list[IDCoercible], add: list[str] | None | UnsetType=UNSET, remove: list[str] | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[ListMessage, ...]:
        """SetMessageFlags 

Add and remove flags of messages.

Args:
    messages (list[ID]): No description
    add (list[str] | None, optional): No description. 
    remove (list[str] | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[ListMessage]
"""
        variables: dict[str, builtins.object] = {}
        variables['messages'] = messages
        if add is not UNSET:
            variables['add'] = add
        if remove is not UNSET:
            variables['remove'] = remove
        return (await self.aexecute(SetMessageFlagsMutation, variables, task=task)).set_message_flags

    def set_message_flags(self, messages: list[IDCoercible], add: list[str] | None | UnsetType=UNSET, remove: list[str] | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[ListMessage, ...]:
        """SetMessageFlags 

Add and remove flags of messages.

Args:
    messages (list[ID]): No description
    add (list[str] | None, optional): No description. 
    remove (list[str] | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[ListMessage]
"""
        variables: dict[str, builtins.object] = {}
        variables['messages'] = messages
        if add is not UNSET:
            variables['add'] = add
        if remove is not UNSET:
            variables['remove'] = remove
        return self.execute(SetMessageFlagsMutation, variables, task=task).set_message_flags

    async def amark_messages_read(self, messages: list[IDCoercible], read: bool | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[ListMessage, ...]:
        """MarkMessagesRead 

Mark messages read or unread.

Args:
    messages (list[ID]): No description
    read (bool | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[ListMessage]
"""
        variables: dict[str, builtins.object] = {}
        variables['messages'] = messages
        if read is not UNSET:
            variables['read'] = read
        return (await self.aexecute(MarkMessagesReadMutation, variables, task=task)).mark_messages_read

    def mark_messages_read(self, messages: list[IDCoercible], read: bool | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[ListMessage, ...]:
        """MarkMessagesRead 

Mark messages read or unread.

Args:
    messages (list[ID]): No description
    read (bool | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[ListMessage]
"""
        variables: dict[str, builtins.object] = {}
        variables['messages'] = messages
        if read is not UNSET:
            variables['read'] = read
        return self.execute(MarkMessagesReadMutation, variables, task=task).mark_messages_read

    async def amove_messages(self, messages: Iterable[IDCoercible], folder: IDCoercible, task: TaskLike | None=None) -> tuple[ListMessage, ...]:
        """MoveMessages 

Move messages to another folder of their mailbox.

Args:
    messages: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required) (list) (required)
    folder: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[ListMessage]
"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input['messages'] = messages
        _input['folder'] = folder
        variables['input'] = _input
        return (await self.aexecute(MoveMessagesMutation, variables, task=task)).move_messages

    def move_messages(self, messages: Iterable[IDCoercible], folder: IDCoercible, task: TaskLike | None=None) -> tuple[ListMessage, ...]:
        """MoveMessages 

Move messages to another folder of their mailbox.

Args:
    messages: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required) (list) (required)
    folder: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[ListMessage]
"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input['messages'] = messages
        _input['folder'] = folder
        variables['input'] = _input
        return self.execute(MoveMessagesMutation, variables, task=task).move_messages

    async def acategorize_messages(self, messages: list[IDCoercible], add: list[IDCoercible] | None | UnsetType=UNSET, remove: list[IDCoercible] | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[ListMessage, ...]:
        """CategorizeMessages 

Put messages into categories and take them out.

Args:
    messages (list[ID]): No description
    add (list[ID] | None, optional): No description. 
    remove (list[ID] | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[ListMessage]
"""
        variables: dict[str, builtins.object] = {}
        variables['messages'] = messages
        if add is not UNSET:
            variables['add'] = add
        if remove is not UNSET:
            variables['remove'] = remove
        return (await self.aexecute(CategorizeMessagesMutation, variables, task=task)).categorize_messages

    def categorize_messages(self, messages: list[IDCoercible], add: list[IDCoercible] | None | UnsetType=UNSET, remove: list[IDCoercible] | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[ListMessage, ...]:
        """CategorizeMessages 

Put messages into categories and take them out.

Args:
    messages (list[ID]): No description
    add (list[ID] | None, optional): No description. 
    remove (list[ID] | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[ListMessage]
"""
        variables: dict[str, builtins.object] = {}
        variables['messages'] = messages
        if add is not UNSET:
            variables['add'] = add
        if remove is not UNSET:
            variables['remove'] = remove
        return self.execute(CategorizeMessagesMutation, variables, task=task).categorize_messages

    async def aundo_mail_changes(self, changes: Iterable[IDCoercible] | None | UnsetType=UNSET, messages: Iterable[IDCoercible] | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[ListMessage, ...]:
        """UndoMailChanges 

Take back changes that have not reached the server.

Args:
    changes: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required) (list)
    messages: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required) (list)
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[ListMessage]
"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        if changes is not UNSET:
            _input['changes'] = changes
        if messages is not UNSET:
            _input['messages'] = messages
        variables['input'] = _input
        return (await self.aexecute(UndoMailChangesMutation, variables, task=task)).undo_mail_changes

    def undo_mail_changes(self, changes: Iterable[IDCoercible] | None | UnsetType=UNSET, messages: Iterable[IDCoercible] | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[ListMessage, ...]:
        """UndoMailChanges 

Take back changes that have not reached the server.

Args:
    changes: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required) (list)
    messages: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required) (list)
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[ListMessage]
"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        if changes is not UNSET:
            _input['changes'] = changes
        if messages is not UNSET:
            _input['messages'] = messages
        variables['input'] = _input
        return self.execute(UndoMailChangesMutation, variables, task=task).undo_mail_changes

    async def adelete_messages(self, messages: list[IDCoercible], permanent: bool | None | UnsetType=UNSET, task: TaskLike | None=None) -> DeleteMessagesMutationDeleteMessages:
        """DeleteMessages 

Delete messages (into Trash, or for good).

Args:
    messages (list[ID]): No description
    permanent (bool | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    DeleteMessagesMutationDeleteMessages
"""
        variables: dict[str, builtins.object] = {}
        variables['messages'] = messages
        if permanent is not UNSET:
            variables['permanent'] = permanent
        return (await self.aexecute(DeleteMessagesMutation, variables, task=task)).delete_messages

    def delete_messages(self, messages: list[IDCoercible], permanent: bool | None | UnsetType=UNSET, task: TaskLike | None=None) -> DeleteMessagesMutationDeleteMessages:
        """DeleteMessages 

Delete messages (into Trash, or for good).

Args:
    messages (list[ID]): No description
    permanent (bool | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    DeleteMessagesMutationDeleteMessages
"""
        variables: dict[str, builtins.object] = {}
        variables['messages'] = messages
        if permanent is not UNSET:
            variables['permanent'] = permanent
        return self.execute(DeleteMessagesMutation, variables, task=task).delete_messages

    async def arevert_messages_to_server(self, messages: list[IDCoercible], task: TaskLike | None=None) -> tuple[ListMessage, ...]:
        """RevertMessagesToServer 

Drop local-only and queued flag changes of messages: back to what the server has.

Args:
    messages (list[ID]): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[ListMessage]
"""
        variables: dict[str, builtins.object] = {}
        variables['messages'] = messages
        return (await self.aexecute(RevertMessagesToServerMutation, variables, task=task)).revert_messages_to_server

    def revert_messages_to_server(self, messages: list[IDCoercible], task: TaskLike | None=None) -> tuple[ListMessage, ...]:
        """RevertMessagesToServer 

Drop local-only and queued flag changes of messages: back to what the server has.

Args:
    messages (list[ID]): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[ListMessage]
"""
        variables: dict[str, builtins.object] = {}
        variables['messages'] = messages
        return self.execute(RevertMessagesToServerMutation, variables, task=task).revert_messages_to_server

    async def aretry_mail_changes(self, changes: list[IDCoercible], task: TaskLike | None=None) -> tuple[MailChange, ...]:
        """RetryMailChanges 

Queue failed changes again.

Args:
    changes (list[ID]): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[MailChange]
"""
        variables: dict[str, builtins.object] = {}
        variables['changes'] = changes
        return (await self.aexecute(RetryMailChangesMutation, variables, task=task)).retry_mail_changes

    def retry_mail_changes(self, changes: list[IDCoercible], task: TaskLike | None=None) -> tuple[MailChange, ...]:
        """RetryMailChanges 

Queue failed changes again.

Args:
    changes (list[ID]): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[MailChange]
"""
        variables: dict[str, builtins.object] = {}
        variables['changes'] = changes
        return self.execute(RetryMailChangesMutation, variables, task=task).retry_mail_changes

    async def astart_o_auth_link(self, provider: IDCoercible | None | UnsetType=UNSET, protocol: Protocol | None | UnsetType=UNSET, redirect_url: str | None | UnsetType=UNSET, name: str | None | UnsetType=UNSET, account: IDCoercible | None | UnsetType=UNSET, login_hint: str | None | UnsetType=UNSET, task: TaskLike | None=None) -> AuthSession:
        """StartOAuthLink 

Start linking (or re-linking) a mailbox through a Gmail or Microsoft provider.

Args:
    provider (ID | None, optional): No description. 
    protocol (Protocol | None, optional): No description. 
    redirect_url (str | None, optional): No description. 
    name (str | None, optional): No description. 
    account (ID | None, optional): No description. 
    login_hint (str | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    AuthSession
"""
        variables: dict[str, builtins.object] = {}
        if provider is not UNSET:
            variables['provider'] = provider
        if protocol is not UNSET:
            variables['protocol'] = protocol
        if redirect_url is not UNSET:
            variables['redirectUrl'] = redirect_url
        if name is not UNSET:
            variables['name'] = name
        if account is not UNSET:
            variables['account'] = account
        if login_hint is not UNSET:
            variables['loginHint'] = login_hint
        return (await self.aexecute(StartOAuthLinkMutation, variables, task=task)).start_o_auth_link

    def start_o_auth_link(self, provider: IDCoercible | None | UnsetType=UNSET, protocol: Protocol | None | UnsetType=UNSET, redirect_url: str | None | UnsetType=UNSET, name: str | None | UnsetType=UNSET, account: IDCoercible | None | UnsetType=UNSET, login_hint: str | None | UnsetType=UNSET, task: TaskLike | None=None) -> AuthSession:
        """StartOAuthLink 

Start linking (or re-linking) a mailbox through a Gmail or Microsoft provider.

Args:
    provider (ID | None, optional): No description. 
    protocol (Protocol | None, optional): No description. 
    redirect_url (str | None, optional): No description. 
    name (str | None, optional): No description. 
    account (ID | None, optional): No description. 
    login_hint (str | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    AuthSession
"""
        variables: dict[str, builtins.object] = {}
        if provider is not UNSET:
            variables['provider'] = provider
        if protocol is not UNSET:
            variables['protocol'] = protocol
        if redirect_url is not UNSET:
            variables['redirectUrl'] = redirect_url
        if name is not UNSET:
            variables['name'] = name
        if account is not UNSET:
            variables['account'] = account
        if login_hint is not UNSET:
            variables['loginHint'] = login_hint
        return self.execute(StartOAuthLinkMutation, variables, task=task).start_o_auth_link

    async def acomplete_auth(self, state: str, code: str | None | UnsetType=UNSET, error: str | None | UnsetType=UNSET, error_description: str | None | UnsetType=UNSET, task: TaskLike | None=None) -> AuthSession:
        """CompleteAuth 

REDIRECT: finish with the code. POLL: advance one step; call until not PENDING.

Args:
    state: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    code: REDIRECT: the `code` query parameter of the redirect. POLL: omitted.
    error: REDIRECT: the provider's `error` / `error_description`, when it refused.
    error_description: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    AuthSession
"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input['state'] = state
        if code is not UNSET:
            _input['code'] = code
        if error is not UNSET:
            _input['error'] = error
        if error_description is not UNSET:
            _input['errorDescription'] = error_description
        variables['input'] = _input
        return (await self.aexecute(CompleteAuthMutation, variables, task=task)).complete_auth

    def complete_auth(self, state: str, code: str | None | UnsetType=UNSET, error: str | None | UnsetType=UNSET, error_description: str | None | UnsetType=UNSET, task: TaskLike | None=None) -> AuthSession:
        """CompleteAuth 

REDIRECT: finish with the code. POLL: advance one step; call until not PENDING.

Args:
    state: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    code: REDIRECT: the `code` query parameter of the redirect. POLL: omitted.
    error: REDIRECT: the provider's `error` / `error_description`, when it refused.
    error_description: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    AuthSession
"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input['state'] = state
        if code is not UNSET:
            _input['code'] = code
        if error is not UNSET:
            _input['error'] = error
        if error_description is not UNSET:
            _input['errorDescription'] = error_description
        variables['input'] = _input
        return self.execute(CompleteAuthMutation, variables, task=task).complete_auth

    async def aresume_auth(self, state: str, task: TaskLike | None=None) -> AuthSession:
        """ResumeAuth 

The same login again (a fresh openUrl if the old one cannot be reused).

Args:
    state (str): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    AuthSession
"""
        variables: dict[str, builtins.object] = {}
        variables['state'] = state
        return (await self.aexecute(ResumeAuthMutation, variables, task=task)).resume_auth

    def resume_auth(self, state: str, task: TaskLike | None=None) -> AuthSession:
        """ResumeAuth 

The same login again (a fresh openUrl if the old one cannot be reused).

Args:
    state (str): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    AuthSession
"""
        variables: dict[str, builtins.object] = {}
        variables['state'] = state
        return self.execute(ResumeAuthMutation, variables, task=task).resume_auth

    async def acancel_auth(self, state: str, task: TaskLike | None=None) -> AuthSession:
        """CancelAuth 

Drop a login that will not be finished. Idempotent.

Args:
    state (str): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    AuthSession
"""
        variables: dict[str, builtins.object] = {}
        variables['state'] = state
        return (await self.aexecute(CancelAuthMutation, variables, task=task)).cancel_auth

    def cancel_auth(self, state: str, task: TaskLike | None=None) -> AuthSession:
        """CancelAuth 

Drop a login that will not be finished. Idempotent.

Args:
    state (str): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    AuthSession
"""
        variables: dict[str, builtins.object] = {}
        variables['state'] = state
        return self.execute(CancelAuthMutation, variables, task=task).cancel_auth

    async def asend_message(self, account: IDCoercible, to: list[RecipientInput] | None | UnsetType=UNSET, cc: list[RecipientInput] | None | UnsetType=UNSET, bcc: list[RecipientInput] | None | UnsetType=UNSET, subject: str | None | UnsetType=UNSET, text: str | None | UnsetType=UNSET, html: str | None | UnsetType=UNSET, in_reply_to: IDCoercible | None | UnsetType=UNSET, attachments: list[str] | None | UnsetType=UNSET, task: TaskLike | None=None) -> OutgoingMessage:
        """SendMessage 

Send a message through a mailbox's SMTP server.

Args:
    account (ID): No description
    to (list[RecipientInput] | None, optional): No description. 
    cc (list[RecipientInput] | None, optional): No description. 
    bcc (list[RecipientInput] | None, optional): No description. 
    subject (str | None, optional): No description. 
    text (str | None, optional): No description. 
    html (str | None, optional): No description. 
    in_reply_to (ID | None, optional): No description. 
    attachments (list[str] | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    OutgoingMessage
"""
        variables: dict[str, builtins.object] = {}
        variables['account'] = account
        if to is not UNSET:
            variables['to'] = to
        if cc is not UNSET:
            variables['cc'] = cc
        if bcc is not UNSET:
            variables['bcc'] = bcc
        if subject is not UNSET:
            variables['subject'] = subject
        if text is not UNSET:
            variables['text'] = text
        if html is not UNSET:
            variables['html'] = html
        if in_reply_to is not UNSET:
            variables['inReplyTo'] = in_reply_to
        if attachments is not UNSET:
            variables['attachments'] = attachments
        return (await self.aexecute(SendMessageMutation, variables, task=task)).send_message

    def send_message(self, account: IDCoercible, to: list[RecipientInput] | None | UnsetType=UNSET, cc: list[RecipientInput] | None | UnsetType=UNSET, bcc: list[RecipientInput] | None | UnsetType=UNSET, subject: str | None | UnsetType=UNSET, text: str | None | UnsetType=UNSET, html: str | None | UnsetType=UNSET, in_reply_to: IDCoercible | None | UnsetType=UNSET, attachments: list[str] | None | UnsetType=UNSET, task: TaskLike | None=None) -> OutgoingMessage:
        """SendMessage 

Send a message through a mailbox's SMTP server.

Args:
    account (ID): No description
    to (list[RecipientInput] | None, optional): No description. 
    cc (list[RecipientInput] | None, optional): No description. 
    bcc (list[RecipientInput] | None, optional): No description. 
    subject (str | None, optional): No description. 
    text (str | None, optional): No description. 
    html (str | None, optional): No description. 
    in_reply_to (ID | None, optional): No description. 
    attachments (list[str] | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    OutgoingMessage
"""
        variables: dict[str, builtins.object] = {}
        variables['account'] = account
        if to is not UNSET:
            variables['to'] = to
        if cc is not UNSET:
            variables['cc'] = cc
        if bcc is not UNSET:
            variables['bcc'] = bcc
        if subject is not UNSET:
            variables['subject'] = subject
        if text is not UNSET:
            variables['text'] = text
        if html is not UNSET:
            variables['html'] = html
        if in_reply_to is not UNSET:
            variables['inReplyTo'] = in_reply_to
        if attachments is not UNSET:
            variables['attachments'] = attachments
        return self.execute(SendMessageMutation, variables, task=task).send_message

    async def acreate_server_provider(self, name: str, protocol: Protocol | None | UnsetType=UNSET, incoming: ServerInput | None | UnsetType=UNSET, smtp: ServerInput | None | UnsetType=UNSET, save_sent_copy: bool | None | UnsetType=UNSET, capabilities: list[ProviderCapability] | None | UnsetType=UNSET, task: TaskLike | None=None) -> MailProvider:
        """CreateServerProvider 
 A provider an admin sets up for the organization, through which its mailboxes are
 linked: a server provider (IMAP/POP3 + SMTP, the servers fixed or left to each link)
 or an OAuth client (Gmail, Microsoft).

Args:
    name (str): No description
    protocol (Protocol | None, optional): No description. 
    incoming (ServerInput | None, optional): No description. 
    smtp (ServerInput | None, optional): No description. 
    save_sent_copy (bool | None, optional): No description. 
    capabilities (list[ProviderCapability] | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    MailProvider
"""
        variables: dict[str, builtins.object] = {}
        variables['name'] = name
        if protocol is not UNSET:
            variables['protocol'] = protocol
        if incoming is not UNSET:
            variables['incoming'] = incoming
        if smtp is not UNSET:
            variables['smtp'] = smtp
        if save_sent_copy is not UNSET:
            variables['saveSentCopy'] = save_sent_copy
        if capabilities is not UNSET:
            variables['capabilities'] = capabilities
        return (await self.aexecute(CreateServerProviderMutation, variables, task=task)).create_server_provider

    def create_server_provider(self, name: str, protocol: Protocol | None | UnsetType=UNSET, incoming: ServerInput | None | UnsetType=UNSET, smtp: ServerInput | None | UnsetType=UNSET, save_sent_copy: bool | None | UnsetType=UNSET, capabilities: list[ProviderCapability] | None | UnsetType=UNSET, task: TaskLike | None=None) -> MailProvider:
        """CreateServerProvider 
 A provider an admin sets up for the organization, through which its mailboxes are
 linked: a server provider (IMAP/POP3 + SMTP, the servers fixed or left to each link)
 or an OAuth client (Gmail, Microsoft).

Args:
    name (str): No description
    protocol (Protocol | None, optional): No description. 
    incoming (ServerInput | None, optional): No description. 
    smtp (ServerInput | None, optional): No description. 
    save_sent_copy (bool | None, optional): No description. 
    capabilities (list[ProviderCapability] | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    MailProvider
"""
        variables: dict[str, builtins.object] = {}
        variables['name'] = name
        if protocol is not UNSET:
            variables['protocol'] = protocol
        if incoming is not UNSET:
            variables['incoming'] = incoming
        if smtp is not UNSET:
            variables['smtp'] = smtp
        if save_sent_copy is not UNSET:
            variables['saveSentCopy'] = save_sent_copy
        if capabilities is not UNSET:
            variables['capabilities'] = capabilities
        return self.execute(CreateServerProviderMutation, variables, task=task).create_server_provider

    async def acreate_o_auth_provider(self, kind: Provider, name: str, client_id: str, redirect_urls: Iterable[str], client_secret: str | None | UnsetType=UNSET, tenant: str | None | UnsetType=UNSET, capabilities: Iterable[ProviderCapability] | None | UnsetType=UNSET, task: TaskLike | None=None) -> MailProvider:
        """CreateOAuthProvider 

Admins: set up a Gmail or Microsoft OAuth client as a provider.

Args:
    kind: GMAIL or MICROSOFT.
    name: What to call it, unique in the organization.
    client_id: The OAuth client id.
    client_secret: The client secret (a public client with PKCE has none). Stored encrypted and never returned.
    redirect_urls: The redirect URLs registered for the client, the default first.
    tenant: Microsoft: the Entra tenant (id or domain); `common` (any account) by default.
    capabilities: What to switch on; everything the kind can do by default (see `providerKinds`).
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    MailProvider
"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input['kind'] = kind
        _input['name'] = name
        _input['clientId'] = client_id
        if client_secret is not UNSET:
            _input['clientSecret'] = client_secret
        _input['redirectUrls'] = redirect_urls
        if tenant is not UNSET:
            _input['tenant'] = tenant
        if capabilities is not UNSET:
            _input['capabilities'] = capabilities
        variables['input'] = _input
        return (await self.aexecute(CreateOAuthProviderMutation, variables, task=task)).create_o_auth_provider

    def create_o_auth_provider(self, kind: Provider, name: str, client_id: str, redirect_urls: Iterable[str], client_secret: str | None | UnsetType=UNSET, tenant: str | None | UnsetType=UNSET, capabilities: Iterable[ProviderCapability] | None | UnsetType=UNSET, task: TaskLike | None=None) -> MailProvider:
        """CreateOAuthProvider 

Admins: set up a Gmail or Microsoft OAuth client as a provider.

Args:
    kind: GMAIL or MICROSOFT.
    name: What to call it, unique in the organization.
    client_id: The OAuth client id.
    client_secret: The client secret (a public client with PKCE has none). Stored encrypted and never returned.
    redirect_urls: The redirect URLs registered for the client, the default first.
    tenant: Microsoft: the Entra tenant (id or domain); `common` (any account) by default.
    capabilities: What to switch on; everything the kind can do by default (see `providerKinds`).
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    MailProvider
"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input['kind'] = kind
        _input['name'] = name
        _input['clientId'] = client_id
        if client_secret is not UNSET:
            _input['clientSecret'] = client_secret
        _input['redirectUrls'] = redirect_urls
        if tenant is not UNSET:
            _input['tenant'] = tenant
        if capabilities is not UNSET:
            _input['capabilities'] = capabilities
        variables['input'] = _input
        return self.execute(CreateOAuthProviderMutation, variables, task=task).create_o_auth_provider

    async def aupdate_server_provider(self, id: IDCoercible, name: str | None | UnsetType=UNSET, enabled: bool | None | UnsetType=UNSET, protocol: Protocol | None | UnsetType=UNSET, incoming: ServerInput | None | UnsetType=UNSET, smtp: ServerInput | None | UnsetType=UNSET, save_sent_copy: bool | None | UnsetType=UNSET, capabilities: Iterable[ProviderCapability] | None | UnsetType=UNSET, task: TaskLike | None=None) -> MailProvider:
        """UpdateServerProvider 

Admins: change an IMAP provider; its mailboxes follow new fixed servers.

Args:
    id: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    enabled: The `Boolean` scalar type represents `true` or `false`.
    protocol: Protocol
    incoming: Where a server is reached.
    smtp: Where a server is reached.
    save_sent_copy: The `Boolean` scalar type represents `true` or `false`.
    capabilities: ProviderCapability (required) (list)
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    MailProvider
"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input['id'] = id
        if name is not UNSET:
            _input['name'] = name
        if enabled is not UNSET:
            _input['enabled'] = enabled
        if protocol is not UNSET:
            _input['protocol'] = protocol
        if incoming is not UNSET:
            _input['incoming'] = incoming
        if smtp is not UNSET:
            _input['smtp'] = smtp
        if save_sent_copy is not UNSET:
            _input['saveSentCopy'] = save_sent_copy
        if capabilities is not UNSET:
            _input['capabilities'] = capabilities
        variables['input'] = _input
        return (await self.aexecute(UpdateServerProviderMutation, variables, task=task)).update_server_provider

    def update_server_provider(self, id: IDCoercible, name: str | None | UnsetType=UNSET, enabled: bool | None | UnsetType=UNSET, protocol: Protocol | None | UnsetType=UNSET, incoming: ServerInput | None | UnsetType=UNSET, smtp: ServerInput | None | UnsetType=UNSET, save_sent_copy: bool | None | UnsetType=UNSET, capabilities: Iterable[ProviderCapability] | None | UnsetType=UNSET, task: TaskLike | None=None) -> MailProvider:
        """UpdateServerProvider 

Admins: change an IMAP provider; its mailboxes follow new fixed servers.

Args:
    id: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    enabled: The `Boolean` scalar type represents `true` or `false`.
    protocol: Protocol
    incoming: Where a server is reached.
    smtp: Where a server is reached.
    save_sent_copy: The `Boolean` scalar type represents `true` or `false`.
    capabilities: ProviderCapability (required) (list)
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    MailProvider
"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input['id'] = id
        if name is not UNSET:
            _input['name'] = name
        if enabled is not UNSET:
            _input['enabled'] = enabled
        if protocol is not UNSET:
            _input['protocol'] = protocol
        if incoming is not UNSET:
            _input['incoming'] = incoming
        if smtp is not UNSET:
            _input['smtp'] = smtp
        if save_sent_copy is not UNSET:
            _input['saveSentCopy'] = save_sent_copy
        if capabilities is not UNSET:
            _input['capabilities'] = capabilities
        variables['input'] = _input
        return self.execute(UpdateServerProviderMutation, variables, task=task).update_server_provider

    async def aupdate_o_auth_provider(self, id: IDCoercible, name: str | None | UnsetType=UNSET, enabled: bool | None | UnsetType=UNSET, client_id: str | None | UnsetType=UNSET, client_secret: str | None | UnsetType=UNSET, redirect_urls: Iterable[str] | None | UnsetType=UNSET, tenant: str | None | UnsetType=UNSET, capabilities: Iterable[ProviderCapability] | None | UnsetType=UNSET, task: TaskLike | None=None) -> MailProvider:
        """UpdateOAuthProvider 

Admins: change a Gmail or Microsoft provider; an empty secret keeps the stored one.

Args:
    id: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    enabled: The `Boolean` scalar type represents `true` or `false`.
    client_id: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    client_secret: A new client secret. Omitted or empty: the stored one is kept.
    redirect_urls: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required) (list)
    tenant: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    capabilities: ProviderCapability (required) (list)
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    MailProvider
"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input['id'] = id
        if name is not UNSET:
            _input['name'] = name
        if enabled is not UNSET:
            _input['enabled'] = enabled
        if client_id is not UNSET:
            _input['clientId'] = client_id
        if client_secret is not UNSET:
            _input['clientSecret'] = client_secret
        if redirect_urls is not UNSET:
            _input['redirectUrls'] = redirect_urls
        if tenant is not UNSET:
            _input['tenant'] = tenant
        if capabilities is not UNSET:
            _input['capabilities'] = capabilities
        variables['input'] = _input
        return (await self.aexecute(UpdateOAuthProviderMutation, variables, task=task)).update_o_auth_provider

    def update_o_auth_provider(self, id: IDCoercible, name: str | None | UnsetType=UNSET, enabled: bool | None | UnsetType=UNSET, client_id: str | None | UnsetType=UNSET, client_secret: str | None | UnsetType=UNSET, redirect_urls: Iterable[str] | None | UnsetType=UNSET, tenant: str | None | UnsetType=UNSET, capabilities: Iterable[ProviderCapability] | None | UnsetType=UNSET, task: TaskLike | None=None) -> MailProvider:
        """UpdateOAuthProvider 

Admins: change a Gmail or Microsoft provider; an empty secret keeps the stored one.

Args:
    id: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    enabled: The `Boolean` scalar type represents `true` or `false`.
    client_id: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    client_secret: A new client secret. Omitted or empty: the stored one is kept.
    redirect_urls: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required) (list)
    tenant: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    capabilities: ProviderCapability (required) (list)
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    MailProvider
"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input['id'] = id
        if name is not UNSET:
            _input['name'] = name
        if enabled is not UNSET:
            _input['enabled'] = enabled
        if client_id is not UNSET:
            _input['clientId'] = client_id
        if client_secret is not UNSET:
            _input['clientSecret'] = client_secret
        if redirect_urls is not UNSET:
            _input['redirectUrls'] = redirect_urls
        if tenant is not UNSET:
            _input['tenant'] = tenant
        if capabilities is not UNSET:
            _input['capabilities'] = capabilities
        variables['input'] = _input
        return self.execute(UpdateOAuthProviderMutation, variables, task=task).update_o_auth_provider

    async def aupdate_provider(self, id: IDCoercible, name: str | None | UnsetType=UNSET, enabled: bool | None | UnsetType=UNSET, capabilities: Iterable[ProviderCapability] | None | UnsetType=UNSET, task: TaskLike | None=None) -> MailProvider:
        """UpdateProvider 

Admins: rename, enable or disable any provider, or change its capabilities.

Args:
    id: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    enabled: The `Boolean` scalar type represents `true` or `false`.
    capabilities: ProviderCapability (required) (list)
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    MailProvider
"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input['id'] = id
        if name is not UNSET:
            _input['name'] = name
        if enabled is not UNSET:
            _input['enabled'] = enabled
        if capabilities is not UNSET:
            _input['capabilities'] = capabilities
        variables['input'] = _input
        return (await self.aexecute(UpdateProviderMutation, variables, task=task)).update_provider

    def update_provider(self, id: IDCoercible, name: str | None | UnsetType=UNSET, enabled: bool | None | UnsetType=UNSET, capabilities: Iterable[ProviderCapability] | None | UnsetType=UNSET, task: TaskLike | None=None) -> MailProvider:
        """UpdateProvider 

Admins: rename, enable or disable any provider, or change its capabilities.

Args:
    id: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    enabled: The `Boolean` scalar type represents `true` or `false`.
    capabilities: ProviderCapability (required) (list)
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    MailProvider
"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input['id'] = id
        if name is not UNSET:
            _input['name'] = name
        if enabled is not UNSET:
            _input['enabled'] = enabled
        if capabilities is not UNSET:
            _input['capabilities'] = capabilities
        variables['input'] = _input
        return self.execute(UpdateProviderMutation, variables, task=task).update_provider

    async def adelete_provider(self, id: IDCoercible, task: TaskLike | None=None) -> ID:
        """DeleteProvider 

Admins: remove a provider no mailbox goes through.

Args:
    id (ID): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    ID
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        return (await self.aexecute(DeleteProviderMutation, variables, task=task)).delete_provider

    def delete_provider(self, id: IDCoercible, task: TaskLike | None=None) -> ID:
        """DeleteProvider 

Admins: remove a provider no mailbox goes through.

Args:
    id (ID): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    ID
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        return self.execute(DeleteProviderMutation, variables, task=task).delete_provider

    async def acreate_task_list(self, name: str, color: str | None | UnsetType=UNSET, position: float | None | UnsetType=UNSET, task: TaskLike | None=None) -> TaskList:
        """CreateTaskList 

Create a task list.

Args:
    name (str): No description
    color (str | None, optional): No description. 
    position (float | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    TaskList
"""
        variables: dict[str, builtins.object] = {}
        variables['name'] = name
        if color is not UNSET:
            variables['color'] = color
        if position is not UNSET:
            variables['position'] = position
        return (await self.aexecute(CreateTaskListMutation, variables, task=task)).create_task_list

    def create_task_list(self, name: str, color: str | None | UnsetType=UNSET, position: float | None | UnsetType=UNSET, task: TaskLike | None=None) -> TaskList:
        """CreateTaskList 

Create a task list.

Args:
    name (str): No description
    color (str | None, optional): No description. 
    position (float | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    TaskList
"""
        variables: dict[str, builtins.object] = {}
        variables['name'] = name
        if color is not UNSET:
            variables['color'] = color
        if position is not UNSET:
            variables['position'] = position
        return self.execute(CreateTaskListMutation, variables, task=task).create_task_list

    async def aupdate_task_list(self, id: IDCoercible, name: str | None | UnsetType=UNSET, color: str | None | UnsetType=UNSET, position: float | None | UnsetType=UNSET, task: TaskLike | None=None) -> TaskList:
        """UpdateTaskList 

Rename, recolor or move a task list.

Args:
    id: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    color: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    position: The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point).
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    TaskList
"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input['id'] = id
        if name is not UNSET:
            _input['name'] = name
        if color is not UNSET:
            _input['color'] = color
        if position is not UNSET:
            _input['position'] = position
        variables['input'] = _input
        return (await self.aexecute(UpdateTaskListMutation, variables, task=task)).update_task_list

    def update_task_list(self, id: IDCoercible, name: str | None | UnsetType=UNSET, color: str | None | UnsetType=UNSET, position: float | None | UnsetType=UNSET, task: TaskLike | None=None) -> TaskList:
        """UpdateTaskList 

Rename, recolor or move a task list.

Args:
    id: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    color: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    position: The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point).
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    TaskList
"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input['id'] = id
        if name is not UNSET:
            _input['name'] = name
        if color is not UNSET:
            _input['color'] = color
        if position is not UNSET:
            _input['position'] = position
        variables['input'] = _input
        return self.execute(UpdateTaskListMutation, variables, task=task).update_task_list

    async def adelete_task_list(self, id: IDCoercible, task: TaskLike | None=None) -> ID:
        """DeleteTaskList 

Delete a task list; its tasks stay, on no list.

Args:
    id (ID): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    ID
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        return (await self.aexecute(DeleteTaskListMutation, variables, task=task)).delete_task_list

    def delete_task_list(self, id: IDCoercible, task: TaskLike | None=None) -> ID:
        """DeleteTaskList 

Delete a task list; its tasks stay, on no list.

Args:
    id (ID): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    ID
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        return self.execute(DeleteTaskListMutation, variables, task=task).delete_task_list

    async def acreate_task(self, title: str, notes: str | None | UnsetType=UNSET, task_list: IDCoercible | None | UnsetType=UNSET, due_at: datetime | None | UnsetType=UNSET, pinned: bool | None | UnsetType=UNSET, position: float | None | UnsetType=UNSET, external_key: str | None | UnsetType=UNSET, threads: list[IDCoercible] | None | UnsetType=UNSET, link: ThreadLinkInput | None | UnsetType=UNSET, task: TaskLike | None=None) -> Task:
        """CreateTask 

Create a task, optionally with conversations.

Args:
    title (str): No description
    notes (str | None, optional): No description. 
    task_list (ID | None, optional): No description. 
    due_at (datetime | None, optional): No description. 
    pinned (bool | None, optional): No description. 
    position (float | None, optional): No description. 
    external_key (str | None, optional): No description. 
    threads (list[ID] | None, optional): No description. 
    link (ThreadLinkInput | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    Task
"""
        variables: dict[str, builtins.object] = {}
        variables['title'] = title
        if notes is not UNSET:
            variables['notes'] = notes
        if task_list is not UNSET:
            variables['taskList'] = task_list
        if due_at is not UNSET:
            variables['dueAt'] = due_at
        if pinned is not UNSET:
            variables['pinned'] = pinned
        if position is not UNSET:
            variables['position'] = position
        if external_key is not UNSET:
            variables['externalKey'] = external_key
        if threads is not UNSET:
            variables['threads'] = threads
        if link is not UNSET:
            variables['link'] = link
        return (await self.aexecute(CreateTaskMutation, variables, task=task)).create_task

    def create_task(self, title: str, notes: str | None | UnsetType=UNSET, task_list: IDCoercible | None | UnsetType=UNSET, due_at: datetime | None | UnsetType=UNSET, pinned: bool | None | UnsetType=UNSET, position: float | None | UnsetType=UNSET, external_key: str | None | UnsetType=UNSET, threads: list[IDCoercible] | None | UnsetType=UNSET, link: ThreadLinkInput | None | UnsetType=UNSET, task: TaskLike | None=None) -> Task:
        """CreateTask 

Create a task, optionally with conversations.

Args:
    title (str): No description
    notes (str | None, optional): No description. 
    task_list (ID | None, optional): No description. 
    due_at (datetime | None, optional): No description. 
    pinned (bool | None, optional): No description. 
    position (float | None, optional): No description. 
    external_key (str | None, optional): No description. 
    threads (list[ID] | None, optional): No description. 
    link (ThreadLinkInput | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    Task
"""
        variables: dict[str, builtins.object] = {}
        variables['title'] = title
        if notes is not UNSET:
            variables['notes'] = notes
        if task_list is not UNSET:
            variables['taskList'] = task_list
        if due_at is not UNSET:
            variables['dueAt'] = due_at
        if pinned is not UNSET:
            variables['pinned'] = pinned
        if position is not UNSET:
            variables['position'] = position
        if external_key is not UNSET:
            variables['externalKey'] = external_key
        if threads is not UNSET:
            variables['threads'] = threads
        if link is not UNSET:
            variables['link'] = link
        return self.execute(CreateTaskMutation, variables, task=task).create_task

    async def aupsert_task(self, external_key: str, title: str, notes: str | None | UnsetType=UNSET, task_list: IDCoercible | None | UnsetType=UNSET, due_at: datetime | None | UnsetType=UNSET, pinned: bool | None | UnsetType=UNSET, threads: list[IDCoercible] | None | UnsetType=UNSET, link: ThreadLinkInput | None | UnsetType=UNSET, task: TaskLike | None=None) -> Task:
        """UpsertTask 

Create or update the caller's task with this externalKey, and add conversations to it.

Args:
    external_key (str): No description
    title (str): No description
    notes (str | None, optional): No description. 
    task_list (ID | None, optional): No description. 
    due_at (datetime | None, optional): No description. 
    pinned (bool | None, optional): No description. 
    threads (list[ID] | None, optional): No description. 
    link (ThreadLinkInput | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    Task
"""
        variables: dict[str, builtins.object] = {}
        variables['externalKey'] = external_key
        variables['title'] = title
        if notes is not UNSET:
            variables['notes'] = notes
        if task_list is not UNSET:
            variables['taskList'] = task_list
        if due_at is not UNSET:
            variables['dueAt'] = due_at
        if pinned is not UNSET:
            variables['pinned'] = pinned
        if threads is not UNSET:
            variables['threads'] = threads
        if link is not UNSET:
            variables['link'] = link
        return (await self.aexecute(UpsertTaskMutation, variables, task=task)).upsert_task

    def upsert_task(self, external_key: str, title: str, notes: str | None | UnsetType=UNSET, task_list: IDCoercible | None | UnsetType=UNSET, due_at: datetime | None | UnsetType=UNSET, pinned: bool | None | UnsetType=UNSET, threads: list[IDCoercible] | None | UnsetType=UNSET, link: ThreadLinkInput | None | UnsetType=UNSET, task: TaskLike | None=None) -> Task:
        """UpsertTask 

Create or update the caller's task with this externalKey, and add conversations to it.

Args:
    external_key (str): No description
    title (str): No description
    notes (str | None, optional): No description. 
    task_list (ID | None, optional): No description. 
    due_at (datetime | None, optional): No description. 
    pinned (bool | None, optional): No description. 
    threads (list[ID] | None, optional): No description. 
    link (ThreadLinkInput | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    Task
"""
        variables: dict[str, builtins.object] = {}
        variables['externalKey'] = external_key
        variables['title'] = title
        if notes is not UNSET:
            variables['notes'] = notes
        if task_list is not UNSET:
            variables['taskList'] = task_list
        if due_at is not UNSET:
            variables['dueAt'] = due_at
        if pinned is not UNSET:
            variables['pinned'] = pinned
        if threads is not UNSET:
            variables['threads'] = threads
        if link is not UNSET:
            variables['link'] = link
        return self.execute(UpsertTaskMutation, variables, task=task).upsert_task

    async def aupdate_task(self, id: IDCoercible, title: str | None | UnsetType=UNSET, notes: str | None | UnsetType=UNSET, list: IDCoercible | None | UnsetType=UNSET, due_at: datetime | None | UnsetType=UNSET, pinned: bool | None | UnsetType=UNSET, position: float | None | UnsetType=UNSET, task: TaskLike | None=None) -> Task:
        """UpdateTask 

Change a task.

Args:
    id: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    title: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    notes: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    list: Another list; null takes it off its list.
    due_at: Date with time (isoformat)
    pinned: The `Boolean` scalar type represents `true` or `false`.
    position: The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point).
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    Task
"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input['id'] = id
        if title is not UNSET:
            _input['title'] = title
        if notes is not UNSET:
            _input['notes'] = notes
        if list is not UNSET:
            _input['list'] = list
        if due_at is not UNSET:
            _input['dueAt'] = due_at
        if pinned is not UNSET:
            _input['pinned'] = pinned
        if position is not UNSET:
            _input['position'] = position
        variables['input'] = _input
        return (await self.aexecute(UpdateTaskMutation, variables, task=task)).update_task

    def update_task(self, id: IDCoercible, title: str | None | UnsetType=UNSET, notes: str | None | UnsetType=UNSET, list: IDCoercible | None | UnsetType=UNSET, due_at: datetime | None | UnsetType=UNSET, pinned: bool | None | UnsetType=UNSET, position: float | None | UnsetType=UNSET, task: TaskLike | None=None) -> Task:
        """UpdateTask 

Change a task.

Args:
    id: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    title: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    notes: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    list: Another list; null takes it off its list.
    due_at: Date with time (isoformat)
    pinned: The `Boolean` scalar type represents `true` or `false`.
    position: The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point).
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    Task
"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input['id'] = id
        if title is not UNSET:
            _input['title'] = title
        if notes is not UNSET:
            _input['notes'] = notes
        if list is not UNSET:
            _input['list'] = list
        if due_at is not UNSET:
            _input['dueAt'] = due_at
        if pinned is not UNSET:
            _input['pinned'] = pinned
        if position is not UNSET:
            _input['position'] = position
        variables['input'] = _input
        return self.execute(UpdateTaskMutation, variables, task=task).update_task

    async def aset_task_status(self, tasks: Iterable[IDCoercible], status: TaskStatus, task: TaskLike | None=None) -> tuple[ListTask, ...]:
        """SetTaskStatus 

Mark tasks OPEN, DONE or DISMISSED.

Args:
    tasks: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required) (list) (required)
    status: TaskStatus (required)
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[ListTask]
"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input['tasks'] = tasks
        _input['status'] = status
        variables['input'] = _input
        return (await self.aexecute(SetTaskStatusMutation, variables, task=task)).set_task_status

    def set_task_status(self, tasks: Iterable[IDCoercible], status: TaskStatus, task: TaskLike | None=None) -> tuple[ListTask, ...]:
        """SetTaskStatus 

Mark tasks OPEN, DONE or DISMISSED.

Args:
    tasks: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required) (list) (required)
    status: TaskStatus (required)
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[ListTask]
"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input['tasks'] = tasks
        _input['status'] = status
        variables['input'] = _input
        return self.execute(SetTaskStatusMutation, variables, task=task).set_task_status

    async def asnooze_tasks(self, tasks: Iterable[IDCoercible], until: datetime | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[ListTask, ...]:
        """SnoozeTasks 

Snooze tasks until a time (null wakes them).

Args:
    tasks: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required) (list) (required)
    until: Date with time (isoformat)
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[ListTask]
"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input['tasks'] = tasks
        if until is not UNSET:
            _input['until'] = until
        variables['input'] = _input
        return (await self.aexecute(SnoozeTasksMutation, variables, task=task)).snooze_tasks

    def snooze_tasks(self, tasks: Iterable[IDCoercible], until: datetime | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[ListTask, ...]:
        """SnoozeTasks 

Snooze tasks until a time (null wakes them).

Args:
    tasks: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required) (list) (required)
    until: Date with time (isoformat)
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[ListTask]
"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input['tasks'] = tasks
        if until is not UNSET:
            _input['until'] = until
        variables['input'] = _input
        return self.execute(SnoozeTasksMutation, variables, task=task).snooze_tasks

    async def adelete_task(self, id: IDCoercible, task: TaskLike | None=None) -> ID:
        """DeleteTask 

Delete a task.

Args:
    id (ID): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    ID
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        return (await self.aexecute(DeleteTaskMutation, variables, task=task)).delete_task

    def delete_task(self, id: IDCoercible, task: TaskLike | None=None) -> ID:
        """DeleteTask 

Delete a task.

Args:
    id (ID): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    ID
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        return self.execute(DeleteTaskMutation, variables, task=task).delete_task

    async def alink_threads(self, task_id: IDCoercible, threads: list[IDCoercible], link: ThreadLinkInput | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[TaskThread, ...]:
        """LinkThreads 
 Link conversations to the task `task_id`.

Args:
    task_id (ID): No description
    threads (list[ID]): No description
    link (ThreadLinkInput | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[TaskThread]
"""
        variables: dict[str, builtins.object] = {}
        variables['taskId'] = task_id
        variables['threads'] = threads
        if link is not UNSET:
            variables['link'] = link
        return (await self.aexecute(LinkThreadsMutation, variables, task=task)).link_threads

    def link_threads(self, task_id: IDCoercible, threads: list[IDCoercible], link: ThreadLinkInput | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[TaskThread, ...]:
        """LinkThreads 
 Link conversations to the task `task_id`.

Args:
    task_id (ID): No description
    threads (list[ID]): No description
    link (ThreadLinkInput | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[TaskThread]
"""
        variables: dict[str, builtins.object] = {}
        variables['taskId'] = task_id
        variables['threads'] = threads
        if link is not UNSET:
            variables['link'] = link
        return self.execute(LinkThreadsMutation, variables, task=task).link_threads

    async def aunlink_threads(self, task_id: IDCoercible, threads: list[IDCoercible], task: TaskLike | None=None) -> Task:
        """UnlinkThreads 

Take conversations out of a task.

Args:
    task_id (ID): No description
    threads (list[ID]): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    Task
"""
        variables: dict[str, builtins.object] = {}
        variables['taskId'] = task_id
        variables['threads'] = threads
        return (await self.aexecute(UnlinkThreadsMutation, variables, task=task)).unlink_threads

    def unlink_threads(self, task_id: IDCoercible, threads: list[IDCoercible], task: TaskLike | None=None) -> Task:
        """UnlinkThreads 

Take conversations out of a task.

Args:
    task_id (ID): No description
    threads (list[ID]): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    Task
"""
        variables: dict[str, builtins.object] = {}
        variables['taskId'] = task_id
        variables['threads'] = threads
        return self.execute(UnlinkThreadsMutation, variables, task=task).unlink_threads

    async def arequest_bigfile_upload(self, original_file_name: str, file_size: int, content_type: str | None | UnsetType=UNSET, task: TaskLike | None=None) -> BigFileUploadGrant:
        """RequestBigfileUpload 

Request temporary S3 credentials to upload one file (an attachment to send).

Args:
    original_file_name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    file_size: A number of bytes. 64-bit, unlike Int: serialized as a JSON number, and accepted as a number or a numeric string. (required)
    content_type: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    BigFileUploadGrant
"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input['originalFileName'] = original_file_name
        _input['fileSize'] = file_size
        if content_type is not UNSET:
            _input['contentType'] = content_type
        variables['input'] = _input
        return (await self.aexecute(RequestBigfileUploadMutation, variables, task=task)).request_bigfile_upload

    def request_bigfile_upload(self, original_file_name: str, file_size: int, content_type: str | None | UnsetType=UNSET, task: TaskLike | None=None) -> BigFileUploadGrant:
        """RequestBigfileUpload 

Request temporary S3 credentials to upload one file (an attachment to send).

Args:
    original_file_name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    file_size: A number of bytes. 64-bit, unlike Int: serialized as a JSON number, and accepted as a number or a numeric string. (required)
    content_type: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    BigFileUploadGrant
"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input['originalFileName'] = original_file_name
        _input['fileSize'] = file_size
        if content_type is not UNSET:
            _input['contentType'] = content_type
        variables['input'] = _input
        return self.execute(RequestBigfileUploadMutation, variables, task=task).request_bigfile_upload

    async def afinish_bigfile_upload(self, store_id: str, valid: bool | None | UnsetType=UNSET, task: TaskLike | None=None) -> BigFileStore:
        """FinishBigfileUpload 

Finalize the caller's file upload after the client has written the object.

Args:
    store_id (str): No description
    valid (bool | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    BigFileStore
"""
        variables: dict[str, builtins.object] = {}
        variables['storeId'] = store_id
        if valid is not UNSET:
            variables['valid'] = valid
        return (await self.aexecute(FinishBigfileUploadMutation, variables, task=task)).finish_bigfile_upload

    def finish_bigfile_upload(self, store_id: str, valid: bool | None | UnsetType=UNSET, task: TaskLike | None=None) -> BigFileStore:
        """FinishBigfileUpload 

Finalize the caller's file upload after the client has written the object.

Args:
    store_id (str): No description
    valid (bool | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    BigFileStore
"""
        variables: dict[str, builtins.object] = {}
        variables['storeId'] = store_id
        if valid is not UNSET:
            variables['valid'] = valid
        return self.execute(FinishBigfileUploadMutation, variables, task=task).finish_bigfile_upload

    async def arefresh_bigfile_upload(self, store_id: str, task: TaskLike | None=None) -> BigFileUploadGrant:
        """RefreshBigfileUpload 
 Reissues credentials for an upload still in flight, to the same key: a write that outlives its
 credentials asks for this before they expire and carries on. Only the uploader may.

Args:
    store_id (str): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    BigFileUploadGrant
"""
        variables: dict[str, builtins.object] = {}
        variables['storeId'] = store_id
        return (await self.aexecute(RefreshBigfileUploadMutation, variables, task=task)).refresh_bigfile_upload

    def refresh_bigfile_upload(self, store_id: str, task: TaskLike | None=None) -> BigFileUploadGrant:
        """RefreshBigfileUpload 
 Reissues credentials for an upload still in flight, to the same key: a write that outlives its
 credentials asks for this before they expire and carries on. Only the uploader may.

Args:
    store_id (str): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    BigFileUploadGrant
"""
        variables: dict[str, builtins.object] = {}
        variables['storeId'] = store_id
        return self.execute(RefreshBigfileUploadMutation, variables, task=task).refresh_bigfile_upload

    async def aget_mail_account(self, id: IDCoercible, task: TaskLike | None=None) -> DetailMailAccount:
        """GetMailAccount 

A mailbox by id.

Args:
    id (ID): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    DetailMailAccount
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        return (await self.aexecute(GetMailAccountQuery, variables, task=task)).mail_account

    def get_mail_account(self, id: IDCoercible, task: TaskLike | None=None) -> DetailMailAccount:
        """GetMailAccount 

A mailbox by id.

Args:
    id (ID): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    DetailMailAccount
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        return self.execute(GetMailAccountQuery, variables, task=task).mail_account

    async def alist_mail_accounts(self, filter: MailAccountFilter | None | UnsetType=UNSET, pagination: OffsetPaginationInput | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[MailAccount, ...]:
        """ListMailAccounts 

The mailboxes the caller sees: their own, shared with them, and the organization's.

Args:
    filter (MailAccountFilter | None, optional): No description. 
    pagination (OffsetPaginationInput | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[MailAccount]
"""
        variables: dict[str, builtins.object] = {}
        if filter is not UNSET:
            variables['filter'] = filter
        if pagination is not UNSET:
            variables['pagination'] = pagination
        return (await self.aexecute(ListMailAccountsQuery, variables, task=task)).mail_accounts

    def list_mail_accounts(self, filter: MailAccountFilter | None | UnsetType=UNSET, pagination: OffsetPaginationInput | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[MailAccount, ...]:
        """ListMailAccounts 

The mailboxes the caller sees: their own, shared with them, and the organization's.

Args:
    filter (MailAccountFilter | None, optional): No description. 
    pagination (OffsetPaginationInput | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[MailAccount]
"""
        variables: dict[str, builtins.object] = {}
        if filter is not UNSET:
            variables['filter'] = filter
        if pagination is not UNSET:
            variables['pagination'] = pagination
        return self.execute(ListMailAccountsQuery, variables, task=task).mail_accounts

    async def amail_presets(self, address: str | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[MailPreset, ...]:
        """MailPresets 

Server settings of well-known providers (the one for `address`, when given).

Args:
    address (str | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[MailPreset]
"""
        variables: dict[str, builtins.object] = {}
        if address is not UNSET:
            variables['address'] = address
        return (await self.aexecute(MailPresetsQuery, variables, task=task)).mail_presets

    def mail_presets(self, address: str | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[MailPreset, ...]:
        """MailPresets 

Server settings of well-known providers (the one for `address`, when given).

Args:
    address (str | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[MailPreset]
"""
        variables: dict[str, builtins.object] = {}
        if address is not UNSET:
            variables['address'] = address
        return self.execute(MailPresetsQuery, variables, task=task).mail_presets

    async def aget_auth_session(self, state: str, task: TaskLike | None=None) -> AuthSession:
        """GetAuthSession 

Where a login is. No side effect.

Args:
    state (str): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    AuthSession
"""
        variables: dict[str, builtins.object] = {}
        variables['state'] = state
        return (await self.aexecute(GetAuthSessionQuery, variables, task=task)).auth_session

    def get_auth_session(self, state: str, task: TaskLike | None=None) -> AuthSession:
        """GetAuthSession 

Where a login is. No side effect.

Args:
    state (str): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    AuthSession
"""
        variables: dict[str, builtins.object] = {}
        variables['state'] = state
        return self.execute(GetAuthSessionQuery, variables, task=task).auth_session

    async def asearch_mail_accounts(self, search: str | None | UnsetType=UNSET, values: list[IDCoercible] | None | UnsetType=UNSET, limit: int | None | UnsetType=UNSET, offset: int | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[SearchMailAccountsQueryOptions, ...]:
        """SearchMailAccounts 

The mailboxes the caller sees: their own, shared with them, and the organization's.

Args:
    search (str | None, optional): No description. 
    values (list[ID] | None, optional): No description. 
    limit (int | None, optional): No description. Defaults to 10
    offset (int | None, optional): No description. Defaults to 0
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[SearchMailAccountsQueryMailAccounts]
"""
        variables: dict[str, builtins.object] = {}
        if search is not UNSET:
            variables['search'] = search
        if values is not UNSET:
            variables['values'] = values
        if limit is not UNSET:
            variables['limit'] = limit
        if offset is not UNSET:
            variables['offset'] = offset
        return (await self.aexecute(SearchMailAccountsQuery, variables, task=task)).options

    def search_mail_accounts(self, search: str | None | UnsetType=UNSET, values: list[IDCoercible] | None | UnsetType=UNSET, limit: int | None | UnsetType=UNSET, offset: int | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[SearchMailAccountsQueryOptions, ...]:
        """SearchMailAccounts 

The mailboxes the caller sees: their own, shared with them, and the organization's.

Args:
    search (str | None, optional): No description. 
    values (list[ID] | None, optional): No description. 
    limit (int | None, optional): No description. Defaults to 10
    offset (int | None, optional): No description. Defaults to 0
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[SearchMailAccountsQueryMailAccounts]
"""
        variables: dict[str, builtins.object] = {}
        if search is not UNSET:
            variables['search'] = search
        if values is not UNSET:
            variables['values'] = values
        if limit is not UNSET:
            variables['limit'] = limit
        if offset is not UNSET:
            variables['offset'] = offset
        return self.execute(SearchMailAccountsQuery, variables, task=task).options

    async def aget_category(self, id: IDCoercible, task: TaskLike | None=None) -> Category:
        """GetCategory 

A category by id.

Args:
    id (ID): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    Category
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        return (await self.aexecute(GetCategoryQuery, variables, task=task)).category

    def get_category(self, id: IDCoercible, task: TaskLike | None=None) -> Category:
        """GetCategory 

A category by id.

Args:
    id (ID): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    Category
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        return self.execute(GetCategoryQuery, variables, task=task).category

    async def alist_categories(self, filter: CategoryFilter | None | UnsetType=UNSET, pagination: OffsetPaginationInput | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[Category, ...]:
        """ListCategories 

Categories of the visible mailboxes (filter by `account`).

Args:
    filter (CategoryFilter | None, optional): No description. 
    pagination (OffsetPaginationInput | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[Category]
"""
        variables: dict[str, builtins.object] = {}
        if filter is not UNSET:
            variables['filter'] = filter
        if pagination is not UNSET:
            variables['pagination'] = pagination
        return (await self.aexecute(ListCategoriesQuery, variables, task=task)).categories

    def list_categories(self, filter: CategoryFilter | None | UnsetType=UNSET, pagination: OffsetPaginationInput | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[Category, ...]:
        """ListCategories 

Categories of the visible mailboxes (filter by `account`).

Args:
    filter (CategoryFilter | None, optional): No description. 
    pagination (OffsetPaginationInput | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[Category]
"""
        variables: dict[str, builtins.object] = {}
        if filter is not UNSET:
            variables['filter'] = filter
        if pagination is not UNSET:
            variables['pagination'] = pagination
        return self.execute(ListCategoriesQuery, variables, task=task).categories

    async def alist_mail_changes(self, filter: MailChangeFilter | None | UnsetType=UNSET, pagination: OffsetPaginationInput | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[MailChange, ...]:
        """ListMailChanges 

Changes made here that have not reached the server yet (pending or failed), oldest first.

Args:
    filter (MailChangeFilter | None, optional): No description. 
    pagination (OffsetPaginationInput | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[MailChange]
"""
        variables: dict[str, builtins.object] = {}
        if filter is not UNSET:
            variables['filter'] = filter
        if pagination is not UNSET:
            variables['pagination'] = pagination
        return (await self.aexecute(ListMailChangesQuery, variables, task=task)).mail_changes

    def list_mail_changes(self, filter: MailChangeFilter | None | UnsetType=UNSET, pagination: OffsetPaginationInput | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[MailChange, ...]:
        """ListMailChanges 

Changes made here that have not reached the server yet (pending or failed), oldest first.

Args:
    filter (MailChangeFilter | None, optional): No description. 
    pagination (OffsetPaginationInput | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[MailChange]
"""
        variables: dict[str, builtins.object] = {}
        if filter is not UNSET:
            variables['filter'] = filter
        if pagination is not UNSET:
            variables['pagination'] = pagination
        return self.execute(ListMailChangesQuery, variables, task=task).mail_changes

    async def aget_mail_folder(self, id: IDCoercible, task: TaskLike | None=None) -> MailFolder:
        """GetMailFolder 

A folder by id.

Args:
    id (ID): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    MailFolder
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        return (await self.aexecute(GetMailFolderQuery, variables, task=task)).mail_folder

    def get_mail_folder(self, id: IDCoercible, task: TaskLike | None=None) -> MailFolder:
        """GetMailFolder 

A folder by id.

Args:
    id (ID): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    MailFolder
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        return self.execute(GetMailFolderQuery, variables, task=task).mail_folder

    async def alist_mail_folders(self, filter: MailFolderFilter | None | UnsetType=UNSET, pagination: OffsetPaginationInput | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[MailFolder, ...]:
        """ListMailFolders 

Folders of the visible mailboxes (filter by `account`).

Args:
    filter (MailFolderFilter | None, optional): No description. 
    pagination (OffsetPaginationInput | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[MailFolder]
"""
        variables: dict[str, builtins.object] = {}
        if filter is not UNSET:
            variables['filter'] = filter
        if pagination is not UNSET:
            variables['pagination'] = pagination
        return (await self.aexecute(ListMailFoldersQuery, variables, task=task)).mail_folders

    def list_mail_folders(self, filter: MailFolderFilter | None | UnsetType=UNSET, pagination: OffsetPaginationInput | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[MailFolder, ...]:
        """ListMailFolders 

Folders of the visible mailboxes (filter by `account`).

Args:
    filter (MailFolderFilter | None, optional): No description. 
    pagination (OffsetPaginationInput | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[MailFolder]
"""
        variables: dict[str, builtins.object] = {}
        if filter is not UNSET:
            variables['filter'] = filter
        if pagination is not UNSET:
            variables['pagination'] = pagination
        return self.execute(ListMailFoldersQuery, variables, task=task).mail_folders

    async def aget_message(self, id: IDCoercible, task: TaskLike | None=None) -> Message:
        """GetMessage 

A message by id.

Args:
    id (ID): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    Message
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        return (await self.aexecute(GetMessageQuery, variables, task=task)).message

    def get_message(self, id: IDCoercible, task: TaskLike | None=None) -> Message:
        """GetMessage 

A message by id.

Args:
    id (ID): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    Message
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        return self.execute(GetMessageQuery, variables, task=task).message

    async def aget_message_html(self, id: IDCoercible, allow_remote: bool | UnsetType=UNSET, task: TaskLike | None=None) -> GetMessageHtmlQueryMessage:
        """GetMessageHtml 

A message by id.

Args:
    id (ID): No description
    allow_remote (bool, optional): No description. Defaults to False
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    GetMessageHtmlQueryMessage
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        if allow_remote is not UNSET:
            variables['allowRemote'] = allow_remote
        return (await self.aexecute(GetMessageHtmlQuery, variables, task=task)).message

    def get_message_html(self, id: IDCoercible, allow_remote: bool | UnsetType=UNSET, task: TaskLike | None=None) -> GetMessageHtmlQueryMessage:
        """GetMessageHtml 

A message by id.

Args:
    id (ID): No description
    allow_remote (bool, optional): No description. Defaults to False
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    GetMessageHtmlQueryMessage
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        if allow_remote is not UNSET:
            variables['allowRemote'] = allow_remote
        return self.execute(GetMessageHtmlQuery, variables, task=task).message

    async def alist_messages(self, filter: MessageFilter | None | UnsetType=UNSET, order: list[MessageOrder] | None | UnsetType=UNSET, pagination: OffsetPaginationInput | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[ListMessage, ...]:
        """ListMessages 

Messages of the visible mailboxes (paginated, filterable — `search` also matches by meaning — and orderable).

Args:
    filter (MessageFilter | None, optional): No description. 
    order (list[MessageOrder] | None, optional): No description. 
    pagination (OffsetPaginationInput | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[ListMessage]
"""
        variables: dict[str, builtins.object] = {}
        if filter is not UNSET:
            variables['filter'] = filter
        if order is not UNSET:
            variables['order'] = order
        if pagination is not UNSET:
            variables['pagination'] = pagination
        return (await self.aexecute(ListMessagesQuery, variables, task=task)).messages

    def list_messages(self, filter: MessageFilter | None | UnsetType=UNSET, order: list[MessageOrder] | None | UnsetType=UNSET, pagination: OffsetPaginationInput | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[ListMessage, ...]:
        """ListMessages 

Messages of the visible mailboxes (paginated, filterable — `search` also matches by meaning — and orderable).

Args:
    filter (MessageFilter | None, optional): No description. 
    order (list[MessageOrder] | None, optional): No description. 
    pagination (OffsetPaginationInput | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[ListMessage]
"""
        variables: dict[str, builtins.object] = {}
        if filter is not UNSET:
            variables['filter'] = filter
        if order is not UNSET:
            variables['order'] = order
        if pagination is not UNSET:
            variables['pagination'] = pagination
        return self.execute(ListMessagesQuery, variables, task=task).messages

    async def acount_messages(self, filter: MessageFilter | None | UnsetType=UNSET, task: TaskLike | None=None) -> int:
        """CountMessages 

How many messages match the filters.

Args:
    filter (MessageFilter | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    int
"""
        variables: dict[str, builtins.object] = {}
        if filter is not UNSET:
            variables['filter'] = filter
        return (await self.aexecute(CountMessagesQuery, variables, task=task)).messages_count

    def count_messages(self, filter: MessageFilter | None | UnsetType=UNSET, task: TaskLike | None=None) -> int:
        """CountMessages 

How many messages match the filters.

Args:
    filter (MessageFilter | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    int
"""
        variables: dict[str, builtins.object] = {}
        if filter is not UNSET:
            variables['filter'] = filter
        return self.execute(CountMessagesQuery, variables, task=task).messages_count

    async def asearch_messages(self, search: str | None | UnsetType=UNSET, values: list[IDCoercible] | None | UnsetType=UNSET, limit: int | None | UnsetType=UNSET, offset: int | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[SearchMessagesQueryOptions, ...]:
        """SearchMessages 

Messages of the visible mailboxes (paginated, filterable — `search` also matches by meaning — and orderable).

Args:
    search (str | None, optional): No description. 
    values (list[ID] | None, optional): No description. 
    limit (int | None, optional): No description. Defaults to 10
    offset (int | None, optional): No description. Defaults to 0
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[SearchMessagesQueryMessages]
"""
        variables: dict[str, builtins.object] = {}
        if search is not UNSET:
            variables['search'] = search
        if values is not UNSET:
            variables['values'] = values
        if limit is not UNSET:
            variables['limit'] = limit
        if offset is not UNSET:
            variables['offset'] = offset
        return (await self.aexecute(SearchMessagesQuery, variables, task=task)).options

    def search_messages(self, search: str | None | UnsetType=UNSET, values: list[IDCoercible] | None | UnsetType=UNSET, limit: int | None | UnsetType=UNSET, offset: int | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[SearchMessagesQueryOptions, ...]:
        """SearchMessages 

Messages of the visible mailboxes (paginated, filterable — `search` also matches by meaning — and orderable).

Args:
    search (str | None, optional): No description. 
    values (list[ID] | None, optional): No description. 
    limit (int | None, optional): No description. Defaults to 10
    offset (int | None, optional): No description. Defaults to 0
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[SearchMessagesQueryMessages]
"""
        variables: dict[str, builtins.object] = {}
        if search is not UNSET:
            variables['search'] = search
        if values is not UNSET:
            variables['values'] = values
        if limit is not UNSET:
            variables['limit'] = limit
        if offset is not UNSET:
            variables['offset'] = offset
        return self.execute(SearchMessagesQuery, variables, task=task).options

    async def aget_outgoing_message(self, id: IDCoercible, task: TaskLike | None=None) -> OutgoingMessage:
        """GetOutgoingMessage 

A sent message by id.

Args:
    id (ID): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    OutgoingMessage
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        return (await self.aexecute(GetOutgoingMessageQuery, variables, task=task)).outgoing_message

    def get_outgoing_message(self, id: IDCoercible, task: TaskLike | None=None) -> OutgoingMessage:
        """GetOutgoingMessage 

A sent message by id.

Args:
    id (ID): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    OutgoingMessage
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        return self.execute(GetOutgoingMessageQuery, variables, task=task).outgoing_message

    async def alist_outbox(self, filter: OutgoingMessageFilter | None | UnsetType=UNSET, pagination: OffsetPaginationInput | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[OutgoingMessage, ...]:
        """ListOutbox 

Mail sent through the visible mailboxes, newest first.

Args:
    filter (OutgoingMessageFilter | None, optional): No description. 
    pagination (OffsetPaginationInput | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[OutgoingMessage]
"""
        variables: dict[str, builtins.object] = {}
        if filter is not UNSET:
            variables['filter'] = filter
        if pagination is not UNSET:
            variables['pagination'] = pagination
        return (await self.aexecute(ListOutboxQuery, variables, task=task)).outbox

    def list_outbox(self, filter: OutgoingMessageFilter | None | UnsetType=UNSET, pagination: OffsetPaginationInput | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[OutgoingMessage, ...]:
        """ListOutbox 

Mail sent through the visible mailboxes, newest first.

Args:
    filter (OutgoingMessageFilter | None, optional): No description. 
    pagination (OffsetPaginationInput | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[OutgoingMessage]
"""
        variables: dict[str, builtins.object] = {}
        if filter is not UNSET:
            variables['filter'] = filter
        if pagination is not UNSET:
            variables['pagination'] = pagination
        return self.execute(ListOutboxQuery, variables, task=task).outbox

    async def aget_mail_provider(self, id: IDCoercible, task: TaskLike | None=None) -> MailProvider:
        """GetMailProvider 

A provider by id.

Args:
    id (ID): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    MailProvider
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        return (await self.aexecute(GetMailProviderQuery, variables, task=task)).mail_provider

    def get_mail_provider(self, id: IDCoercible, task: TaskLike | None=None) -> MailProvider:
        """GetMailProvider 

A provider by id.

Args:
    id (ID): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    MailProvider
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        return self.execute(GetMailProviderQuery, variables, task=task).mail_provider

    async def alist_mail_providers(self, filter: MailProviderFilter | None | UnsetType=UNSET, pagination: OffsetPaginationInput | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[MailProvider, ...]:
        """ListMailProviders 

The providers the organization set up; every mailbox is linked through one.

Args:
    filter (MailProviderFilter | None, optional): No description. 
    pagination (OffsetPaginationInput | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[MailProvider]
"""
        variables: dict[str, builtins.object] = {}
        if filter is not UNSET:
            variables['filter'] = filter
        if pagination is not UNSET:
            variables['pagination'] = pagination
        return (await self.aexecute(ListMailProvidersQuery, variables, task=task)).mail_providers

    def list_mail_providers(self, filter: MailProviderFilter | None | UnsetType=UNSET, pagination: OffsetPaginationInput | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[MailProvider, ...]:
        """ListMailProviders 

The providers the organization set up; every mailbox is linked through one.

Args:
    filter (MailProviderFilter | None, optional): No description. 
    pagination (OffsetPaginationInput | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[MailProvider]
"""
        variables: dict[str, builtins.object] = {}
        if filter is not UNSET:
            variables['filter'] = filter
        if pagination is not UNSET:
            variables['pagination'] = pagination
        return self.execute(ListMailProvidersQuery, variables, task=task).mail_providers

    async def aprovider_kinds(self, task: TaskLike | None=None) -> tuple[ProviderKind, ...]:
        """ProviderKinds 

The kinds of provider this server can run, each with its capabilities.

Args:
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[ProviderKind]
"""
        variables: dict[str, builtins.object] = {}
        return (await self.aexecute(ProviderKindsQuery, variables, task=task)).provider_kinds

    def provider_kinds(self, task: TaskLike | None=None) -> tuple[ProviderKind, ...]:
        """ProviderKinds 

The kinds of provider this server can run, each with its capabilities.

Args:
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[ProviderKind]
"""
        variables: dict[str, builtins.object] = {}
        return self.execute(ProviderKindsQuery, variables, task=task).provider_kinds

    async def aget_task(self, id: IDCoercible, task: TaskLike | None=None) -> Task:
        """GetTask 

A task by id.

Args:
    id (ID): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    Task
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        return (await self.aexecute(GetTaskQuery, variables, task=task)).task

    def get_task(self, id: IDCoercible, task: TaskLike | None=None) -> Task:
        """GetTask 

A task by id.

Args:
    id (ID): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    Task
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        return self.execute(GetTaskQuery, variables, task=task).task

    async def alist_tasks(self, filter: TaskFilter | None | UnsetType=UNSET, order: list[TaskOrder] | None | UnsetType=UNSET, pagination: OffsetPaginationInput | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[ListTask, ...]:
        """ListTasks 

The caller's tasks (paginated, filterable — `active` is the Inbox view — and orderable).

Args:
    filter (TaskFilter | None, optional): No description. 
    order (list[TaskOrder] | None, optional): No description. 
    pagination (OffsetPaginationInput | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[ListTask]
"""
        variables: dict[str, builtins.object] = {}
        if filter is not UNSET:
            variables['filter'] = filter
        if order is not UNSET:
            variables['order'] = order
        if pagination is not UNSET:
            variables['pagination'] = pagination
        return (await self.aexecute(ListTasksQuery, variables, task=task)).tasks

    def list_tasks(self, filter: TaskFilter | None | UnsetType=UNSET, order: list[TaskOrder] | None | UnsetType=UNSET, pagination: OffsetPaginationInput | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[ListTask, ...]:
        """ListTasks 

The caller's tasks (paginated, filterable — `active` is the Inbox view — and orderable).

Args:
    filter (TaskFilter | None, optional): No description. 
    order (list[TaskOrder] | None, optional): No description. 
    pagination (OffsetPaginationInput | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[ListTask]
"""
        variables: dict[str, builtins.object] = {}
        if filter is not UNSET:
            variables['filter'] = filter
        if order is not UNSET:
            variables['order'] = order
        if pagination is not UNSET:
            variables['pagination'] = pagination
        return self.execute(ListTasksQuery, variables, task=task).tasks

    async def acount_tasks(self, filter: TaskFilter | None | UnsetType=UNSET, task: TaskLike | None=None) -> int:
        """CountTasks 

How many of the caller's tasks match the filters.

Args:
    filter (TaskFilter | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    int
"""
        variables: dict[str, builtins.object] = {}
        if filter is not UNSET:
            variables['filter'] = filter
        return (await self.aexecute(CountTasksQuery, variables, task=task)).tasks_count

    def count_tasks(self, filter: TaskFilter | None | UnsetType=UNSET, task: TaskLike | None=None) -> int:
        """CountTasks 

How many of the caller's tasks match the filters.

Args:
    filter (TaskFilter | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    int
"""
        variables: dict[str, builtins.object] = {}
        if filter is not UNSET:
            variables['filter'] = filter
        return self.execute(CountTasksQuery, variables, task=task).tasks_count

    async def aget_task_list(self, id: IDCoercible, task: TaskLike | None=None) -> TaskList:
        """GetTaskList 

A task list by id.

Args:
    id (ID): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    TaskList
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        return (await self.aexecute(GetTaskListQuery, variables, task=task)).task_list

    def get_task_list(self, id: IDCoercible, task: TaskLike | None=None) -> TaskList:
        """GetTaskList 

A task list by id.

Args:
    id (ID): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    TaskList
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        return self.execute(GetTaskListQuery, variables, task=task).task_list

    async def alist_task_lists(self, filter: TaskListFilter | None | UnsetType=UNSET, pagination: OffsetPaginationInput | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[TaskList, ...]:
        """ListTaskLists 

The caller's task lists.

Args:
    filter (TaskListFilter | None, optional): No description. 
    pagination (OffsetPaginationInput | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[TaskList]
"""
        variables: dict[str, builtins.object] = {}
        if filter is not UNSET:
            variables['filter'] = filter
        if pagination is not UNSET:
            variables['pagination'] = pagination
        return (await self.aexecute(ListTaskListsQuery, variables, task=task)).task_lists

    def list_task_lists(self, filter: TaskListFilter | None | UnsetType=UNSET, pagination: OffsetPaginationInput | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[TaskList, ...]:
        """ListTaskLists 

The caller's task lists.

Args:
    filter (TaskListFilter | None, optional): No description. 
    pagination (OffsetPaginationInput | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[TaskList]
"""
        variables: dict[str, builtins.object] = {}
        if filter is not UNSET:
            variables['filter'] = filter
        if pagination is not UNSET:
            variables['pagination'] = pagination
        return self.execute(ListTaskListsQuery, variables, task=task).task_lists

    async def asearch_tasks(self, search: str | None | UnsetType=UNSET, values: list[IDCoercible] | None | UnsetType=UNSET, limit: int | None | UnsetType=UNSET, offset: int | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[SearchTasksQueryOptions, ...]:
        """SearchTasks 

The caller's tasks (paginated, filterable — `active` is the Inbox view — and orderable).

Args:
    search (str | None, optional): No description. 
    values (list[ID] | None, optional): No description. 
    limit (int | None, optional): No description. Defaults to 10
    offset (int | None, optional): No description. Defaults to 0
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[SearchTasksQueryTasks]
"""
        variables: dict[str, builtins.object] = {}
        if search is not UNSET:
            variables['search'] = search
        if values is not UNSET:
            variables['values'] = values
        if limit is not UNSET:
            variables['limit'] = limit
        if offset is not UNSET:
            variables['offset'] = offset
        return (await self.aexecute(SearchTasksQuery, variables, task=task)).options

    def search_tasks(self, search: str | None | UnsetType=UNSET, values: list[IDCoercible] | None | UnsetType=UNSET, limit: int | None | UnsetType=UNSET, offset: int | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[SearchTasksQueryOptions, ...]:
        """SearchTasks 

The caller's tasks (paginated, filterable — `active` is the Inbox view — and orderable).

Args:
    search (str | None, optional): No description. 
    values (list[ID] | None, optional): No description. 
    limit (int | None, optional): No description. Defaults to 10
    offset (int | None, optional): No description. Defaults to 0
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[SearchTasksQueryTasks]
"""
        variables: dict[str, builtins.object] = {}
        if search is not UNSET:
            variables['search'] = search
        if values is not UNSET:
            variables['values'] = values
        if limit is not UNSET:
            variables['limit'] = limit
        if offset is not UNSET:
            variables['offset'] = offset
        return self.execute(SearchTasksQuery, variables, task=task).options

    async def asearch_task_lists(self, search: str | None | UnsetType=UNSET, values: list[IDCoercible] | None | UnsetType=UNSET, limit: int | None | UnsetType=UNSET, offset: int | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[SearchTaskListsQueryOptions, ...]:
        """SearchTaskLists 

The caller's task lists.

Args:
    search (str | None, optional): No description. 
    values (list[ID] | None, optional): No description. 
    limit (int | None, optional): No description. Defaults to 10
    offset (int | None, optional): No description. Defaults to 0
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[SearchTaskListsQueryTaskLists]
"""
        variables: dict[str, builtins.object] = {}
        if search is not UNSET:
            variables['search'] = search
        if values is not UNSET:
            variables['values'] = values
        if limit is not UNSET:
            variables['limit'] = limit
        if offset is not UNSET:
            variables['offset'] = offset
        return (await self.aexecute(SearchTaskListsQuery, variables, task=task)).options

    def search_task_lists(self, search: str | None | UnsetType=UNSET, values: list[IDCoercible] | None | UnsetType=UNSET, limit: int | None | UnsetType=UNSET, offset: int | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[SearchTaskListsQueryOptions, ...]:
        """SearchTaskLists 

The caller's task lists.

Args:
    search (str | None, optional): No description. 
    values (list[ID] | None, optional): No description. 
    limit (int | None, optional): No description. Defaults to 10
    offset (int | None, optional): No description. Defaults to 0
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[SearchTaskListsQueryTaskLists]
"""
        variables: dict[str, builtins.object] = {}
        if search is not UNSET:
            variables['search'] = search
        if values is not UNSET:
            variables['values'] = values
        if limit is not UNSET:
            variables['limit'] = limit
        if offset is not UNSET:
            variables['offset'] = offset
        return self.execute(SearchTaskListsQuery, variables, task=task).options

    async def aget_thread(self, id: IDCoercible, task: TaskLike | None=None) -> Thread:
        """GetThread 

A conversation by id.

Args:
    id (ID): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    Thread
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        return (await self.aexecute(GetThreadQuery, variables, task=task)).thread

    def get_thread(self, id: IDCoercible, task: TaskLike | None=None) -> Thread:
        """GetThread 

A conversation by id.

Args:
    id (ID): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    Thread
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        return self.execute(GetThreadQuery, variables, task=task).thread

    async def alist_threads(self, filter: ThreadFilter | None | UnsetType=UNSET, order: list[ThreadOrder] | None | UnsetType=UNSET, pagination: OffsetPaginationInput | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[ListThread, ...]:
        """ListThreads 

Conversations of the visible mailboxes (paginated, filterable, orderable).

Args:
    filter (ThreadFilter | None, optional): No description. 
    order (list[ThreadOrder] | None, optional): No description. 
    pagination (OffsetPaginationInput | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[ListThread]
"""
        variables: dict[str, builtins.object] = {}
        if filter is not UNSET:
            variables['filter'] = filter
        if order is not UNSET:
            variables['order'] = order
        if pagination is not UNSET:
            variables['pagination'] = pagination
        return (await self.aexecute(ListThreadsQuery, variables, task=task)).threads

    def list_threads(self, filter: ThreadFilter | None | UnsetType=UNSET, order: list[ThreadOrder] | None | UnsetType=UNSET, pagination: OffsetPaginationInput | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[ListThread, ...]:
        """ListThreads 

Conversations of the visible mailboxes (paginated, filterable, orderable).

Args:
    filter (ThreadFilter | None, optional): No description. 
    order (list[ThreadOrder] | None, optional): No description. 
    pagination (OffsetPaginationInput | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[ListThread]
"""
        variables: dict[str, builtins.object] = {}
        if filter is not UNSET:
            variables['filter'] = filter
        if order is not UNSET:
            variables['order'] = order
        if pagination is not UNSET:
            variables['pagination'] = pagination
        return self.execute(ListThreadsQuery, variables, task=task).threads

    async def acount_threads(self, filter: ThreadFilter | None | UnsetType=UNSET, task: TaskLike | None=None) -> int:
        """CountThreads 

How many conversations match the filters (for a list header).

Args:
    filter (ThreadFilter | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    int
"""
        variables: dict[str, builtins.object] = {}
        if filter is not UNSET:
            variables['filter'] = filter
        return (await self.aexecute(CountThreadsQuery, variables, task=task)).threads_count

    def count_threads(self, filter: ThreadFilter | None | UnsetType=UNSET, task: TaskLike | None=None) -> int:
        """CountThreads 

How many conversations match the filters (for a list header).

Args:
    filter (ThreadFilter | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    int
"""
        variables: dict[str, builtins.object] = {}
        if filter is not UNSET:
            variables['filter'] = filter
        return self.execute(CountThreadsQuery, variables, task=task).threads_count

    async def asearch_threads(self, search: str | None | UnsetType=UNSET, values: list[IDCoercible] | None | UnsetType=UNSET, limit: int | None | UnsetType=UNSET, offset: int | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[SearchThreadsQueryOptions, ...]:
        """SearchThreads 

Conversations of the visible mailboxes (paginated, filterable, orderable).

Args:
    search (str | None, optional): No description. 
    values (list[ID] | None, optional): No description. 
    limit (int | None, optional): No description. Defaults to 10
    offset (int | None, optional): No description. Defaults to 0
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[SearchThreadsQueryThreads]
"""
        variables: dict[str, builtins.object] = {}
        if search is not UNSET:
            variables['search'] = search
        if values is not UNSET:
            variables['values'] = values
        if limit is not UNSET:
            variables['limit'] = limit
        if offset is not UNSET:
            variables['offset'] = offset
        return (await self.aexecute(SearchThreadsQuery, variables, task=task)).options

    def search_threads(self, search: str | None | UnsetType=UNSET, values: list[IDCoercible] | None | UnsetType=UNSET, limit: int | None | UnsetType=UNSET, offset: int | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[SearchThreadsQueryOptions, ...]:
        """SearchThreads 

Conversations of the visible mailboxes (paginated, filterable, orderable).

Args:
    search (str | None, optional): No description. 
    values (list[ID] | None, optional): No description. 
    limit (int | None, optional): No description. Defaults to 10
    offset (int | None, optional): No description. Defaults to 0
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[SearchThreadsQueryThreads]
"""
        variables: dict[str, builtins.object] = {}
        if search is not UNSET:
            variables['search'] = search
        if values is not UNSET:
            variables['values'] = values
        if limit is not UNSET:
            variables['limit'] = limit
        if offset is not UNSET:
            variables['offset'] = offset
        return self.execute(SearchThreadsQuery, variables, task=task).options

    async def awatch_mailbox_syncs(self, task: TaskLike | None=None) -> AsyncIterator[MailboxSyncEvent]:
        """WatchMailboxSyncs 

Events whenever a visible mailbox finished syncing.

Args:
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    MailboxSyncEvent
"""
        variables: dict[str, builtins.object] = {}
        async for event in self.asubscribe(WatchMailboxSyncsSubscription, variables, task=task):
            yield event.mailbox_syncs

    def watch_mailbox_syncs(self, task: TaskLike | None=None) -> Iterator[MailboxSyncEvent]:
        """WatchMailboxSyncs 

Events whenever a visible mailbox finished syncing.

Args:
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    MailboxSyncEvent
"""
        variables: dict[str, builtins.object] = {}
        for event in self.subscribe(WatchMailboxSyncsSubscription, variables, task=task):
            yield event.mailbox_syncs
CategoryFilter.model_rebuild()
MailAccountFilter.model_rebuild()
MailChangeFilter.model_rebuild()
MailFolderFilter.model_rebuild()
MailProviderFilter.model_rebuild()
MessageFilter.model_rebuild()
OutgoingMessageFilter.model_rebuild()
TaskFilter.model_rebuild()
TaskListFilter.model_rebuild()
ThreadFilter.model_rebuild()