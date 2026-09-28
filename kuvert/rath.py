from types import TracebackType

from pydantic import Field
from rath import rath
from rath.links.auth import AuthTokenLink
from rath.links.compose import TypedComposedLink
from rath.links.dictinglink import DictingLink
from rath.links.shrink import ShrinkingLink
from rath.links.split import SplitLink


class KuvertLinkComposition(TypedComposedLink):
    shrinking: ShrinkingLink = Field(default_factory=ShrinkingLink)
    dicting: DictingLink = Field(default_factory=DictingLink)
    auth: AuthTokenLink
    split: SplitLink


class KuvertRath(rath.Rath):
    """Kuvert Rath

    The GraphQL client for kuvert. It is the transport of a
    :class:`kuvert.kuvert.Kuvert` client; calls go through that client.
    """

    async def __aenter__(self):
        """Enter the client.

        Entering does not make it "the current client": nothing is. Calls go
        through the :class:`kuvert.kuvert.Kuvert` client that holds it.
        """
        await super().__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await super().__aexit__(exc_type, exc_val, traceback)
