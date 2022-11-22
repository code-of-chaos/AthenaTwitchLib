# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import asyncio
import datetime
from dataclasses import dataclass
from typing import Callable

# Athena Packages

# Local Imports
from AthenaTwitchLib.irc.logic._logic import BaseLogic, register_callback_as_logical_component


# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True)
class TaskData:
    interval:datetime.timedelta
    output_deferred:bool = False

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class TaskLogic(BaseLogic):
    open_tasks:list[asyncio.Task]
    _tasks:list[tuple[Callable,TaskData]]

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls, *args, *kwargs)
        obj._tasks = [
            (coroutine, coroutine._data)
            for coroutine in
            obj._logic_components
        ]
        obj.open_tasks = []
        return obj

    async def start_all_tasks(self, transport:asyncio.Transport):
        loop = asyncio.get_running_loop()
        for coroutine, task_data in self._tasks:
            self.open_tasks.append(
                loop.create_task(self._create_task(transport, coroutine, task_data))
            )

    async def stop_all_tasks(self):
        for task in self.open_tasks:
            task.cancel()
        self.open_tasks.clear()

    async def _create_task(self, transport:asyncio.Transport, coroutine:Callable, task_data: TaskData):
        if task_data.output_deferred:
            while True:
                await asyncio.sleep(task_data.interval.total_seconds())
                await coroutine(transport)
        else:
            while True:
                await coroutine(transport)
                await asyncio.sleep(task_data.interval.total_seconds())

    @staticmethod
    def task(task_data:TaskData):
        """
        Decorator to be used by the Bot,
            to assign a method as a task that has to be run at a given interval
        """
        def decorator(fnc):
            register_callback_as_logical_component(fnc)
            fnc._data = task_data
            return fnc
        return decorator