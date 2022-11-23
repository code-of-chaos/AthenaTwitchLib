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
@dataclass(slots=True, kw_only=True)
class TaskData:
    at:datetime.timedelta = None
    interval:datetime.timedelta = None
    channel:str = None

    def __post_init__(self):
        if self.at is not None:
            self.interval = self.at

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class TaskLogic(BaseLogic):
    open_tasks:list[asyncio.Task]
    _tasks:list[tuple[Callable,TaskData]]

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls, *args, *kwargs)

        # retrieve all tasks
        obj._tasks = [
            (coroutine, coroutine._data)
            for coroutine in
            obj._logic_components
        ]

        # Extract data from the bot, and make sure that tasks adhere to this

        obj.open_tasks = []
        return obj

    def start_all_tasks(self, transport:asyncio.Transport, loop:asyncio.AbstractEventLoop):
        if self.open_tasks:
            self.stop_all_tasks()

        self.open_tasks = [
            loop.create_task(self._create_task(transport, coroutine, task_data))
            for coroutine, task_data in self._tasks
        ]

    def stop_all_tasks(self):
        for task in self.open_tasks:
            task.cancel()
        self.open_tasks.clear()

    async def _create_task(self, transport:asyncio.Transport, coroutine:Callable, task_data:TaskData):
        # it the time has been set to be at a certain part of the hour
        #   Wait until we get to that part of the hour
        if task_data.at is not None:
            now = datetime.datetime.now()
            await asyncio.sleep((
                task_data.at
                - (datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second) % task_data.at)
            ).seconds)

            while True:
                await coroutine(transport)
                await asyncio.sleep(task_data.interval.total_seconds())

        # If we don't have to set the task at a certain part of the hour
        #   Start up the loop regularly
        else:
            while True:
                await asyncio.sleep(task_data.interval.total_seconds())
                await coroutine(transport)


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