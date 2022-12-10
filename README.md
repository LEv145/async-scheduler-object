# Async scheduler object
Object-like async scheduler

## Install

https://pypi.org/project/async-scheduler-object/

## Usage

```py
import asyncio
from datetime import timedelta

from async_scheduler_object import AsyncScheduler, AsyncSchedulerEvent


class AgeSchedulerEvent(AsyncSchedulerEvent):
    def __init__(self, start: int) -> None:
        self._age = start

    async def run(self) -> None:
        print("Age", self._age)
        self._age += 1


class CatsSchedulerEvent(AsyncSchedulerEvent):
    def __init__(self, start: int) -> None:
        self._cats_count = start

    async def run(self) -> None:
        print("Cats", self._cats_count)
        self._cats_count *= 1


async def main() -> None:
    scheduler_1 = AsyncScheduler(
        events=[AgeSchedulerEvent(start=1)],
        interval=timedelta(seconds=1),
    )
    scheduler_2 = AsyncScheduler(
        events=[AgeSchedulerEvent(start=10), CatsSchedulerEvent(start=20)],
        interval=timedelta(seconds=0.5),
    )
    await scheduler_1.start()
    await scheduler_2.start()

    await asyncio.sleep(10)

    await scheduler_1.stop()
    await scheduler_2.stop()


asyncio.run(main())
```
