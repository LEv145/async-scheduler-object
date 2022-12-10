from __future__ import annotations

import typing as t
import abc
import asyncio
from contextlib import suppress

if t.TYPE_CHECKING:
    from datetime import timedelta


class AsyncScheduler():
    __slots__ = ("is_started", "_events", "_seconds_interval", "_task")

    def __init__(self, events: t.List[AsyncSchedulerEvent], interval: timedelta):
        self.is_started = False

        self._events = events
        self._seconds_interval = interval.total_seconds()
        self._task = None

    async def start(self):
        if self.is_started:
            return

        self.is_started = True
        self._task = asyncio.create_task(self._start_task_loop())

    async def stop(self):
        if not self.is_started:
            return

        self.is_started = False
        await self._cancel_task()

    async def _start_task_loop(self) -> t.NoReturn:
        while True:
            await self._start_task_loop_iteration()

    async def _start_task_loop_iteration(self) -> None:
        await self._sleep_interval()
        asyncio.create_task(self._start_events())

    async def _sleep_interval(self) -> None:
        await asyncio.sleep(self._seconds_interval)

    async def _start_events(self) -> None:
        await asyncio.gather(i.run() for i in self._events)

    async def _cancel_task(self) -> None:
        if self._task is None:
            return

        self._task.cancel()
        with suppress(asyncio.CancelledError):
            await self._task


class AsyncSchedulerEvent(abc.ABC):
    @abc.abstractmethod
    async def run(self) -> None:
        pass
