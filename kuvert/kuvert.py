"""The base client for kuvert"""

from collections.abc import AsyncGenerator, Generator
from typing import Any

from koil import unkoil, unkoil_gen
from koil.composition import Composition
from pydantic import Field
from rath.origin import origin_context
from rath.task import TASK_HEADER, TaskLike, current_task, token_of
from rath.turms.funcs import TOperation

from kuvert.api.schema import KuvertApi
from kuvert.rath import KuvertRath


class Kuvert(Composition, KuvertApi):
    """Kuvert

    Every kuvert operation is a method of it (``kuvert.aget_thread(id)``), mixed in
    from the generated ``KuvertApi``. Each generated method hands its operation
    class and variables to :meth:`execute`/:meth:`aexecute` (queries, mutations) or
    :meth:`subscribe`/:meth:`asubscribe` (subscriptions), which run it over
    ``self.rath``. Nothing is looked up; what a call returns remembers the client it
    was called on. Actions ask for it by annotation (``kuvert: Kuvert``) and are
    handed their app's client.
    """

    rath: KuvertRath = Field(
        ...,
        description="The Rath client used to interact with the Kuvert API.",
    )

    @staticmethod
    def _serialize(
        operation: type[TOperation], variables: dict[str, Any]
    ) -> dict[str, Any]:
        # kuvert omits every argument that was not set (exclude_unset), as it always has:
        # an optional left out stays off the wire rather than being sent as null.
        return operation.Arguments(**variables).model_dump(
            by_alias=True, exclude_unset=True
        )

    def _headers(self, task: "TaskLike | None" = None) -> dict[str, Any] | None:
        """The per-call headers: the provenance token of the task this call is for.

        ``task`` when the caller named one, else whichever task is running. There
        is no per-task copy of this client: one instance serves every task, and
        what a request is attributed to is decided per call.
        """
        token = token_of(task)
        return {TASK_HEADER: token} if token else None

    def execute(
        self,
        operation: type[TOperation],
        variables: dict[str, Any],
        task: "TaskLike | None" = None,
    ) -> TOperation:
        """Executes a query or mutation in a blocking way."""
        return unkoil(
            self.aexecute,
            operation,
            variables,
            task=task if task is not None else current_task.get(),
        )

    async def aexecute(
        self,
        operation: type[TOperation],
        variables: dict[str, Any],
        task: "TaskLike | None" = None,
    ) -> TOperation:
        """Executes a query or mutation in a non-blocking way."""
        x = await self.rath.aquery(
            operation.Meta.document,
            self._serialize(operation, variables),
            headers=self._headers(task),
        )
        return operation.model_validate(
            x.data, context=origin_context(client=self, rath=self.rath)
        )

    def subscribe(
        self,
        operation: type[TOperation],
        variables: dict[str, Any],
        task: "TaskLike | None" = None,
    ) -> Generator[TOperation, None, None]:
        """Subscribes to an operation in a blocking way."""
        return unkoil_gen(
            self.asubscribe,
            operation,
            variables,
            task=task if task is not None else current_task.get(),
        )

    async def asubscribe(
        self,
        operation: type[TOperation],
        variables: dict[str, Any],
        task: "TaskLike | None" = None,
    ) -> AsyncGenerator[TOperation, None]:
        """Subscribes to an operation in a non-blocking way."""
        async for event in self.rath.asubscribe(
            operation.Meta.document,
            self._serialize(operation, variables),
            headers=self._headers(task),
        ):
            yield operation.model_validate(
                event.data, context=origin_context(client=self, rath=self.rath)
            )
