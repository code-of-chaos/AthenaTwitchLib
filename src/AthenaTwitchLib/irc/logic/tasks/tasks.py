# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from typing import Callable,ClassVar
import asyncio
import datetime
import inspect

# Athena Packages

# Local Imports
from AthenaTwitchLib.irc.logic.types import BaseTaskLogic
from AthenaTwitchLib.irc.logic.tasks.task_data import TaskData

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class TaskLogic(BaseTaskLogic):
    """
    Logic system behind hard coded tasks.
    """
    open_tasks:list[asyncio.Task]
    _logic_components: ClassVar[list[tuple[Callable,TaskData]]] = []

    def __init__(self):
        self.open_tasks = []

    def start_all_tasks(self, transport:asyncio.Transport, loop:asyncio.AbstractEventLoop):
        if self.open_tasks:
            self.stop_all_tasks()

        self.open_tasks = [
            loop.create_task(self._create_task(transport, coroutine, task_data))
            for coroutine, task_data in self._logic_components
        ]

    def stop_all_tasks(self):
        for task in self.open_tasks:
            task.cancel()
        self.open_tasks.clear()

    async def _create_task(self, transport:asyncio.Transport, coroutine:Callable, task_data:TaskData):
        """
        Main function to create a task in the correct format
        Gets called by `TaskLogic.start_all_tasks` as it controls the actions of a task
        """
        # it the time has been set to be at a certain part of the hour
        #   Wait until we get to that part of the hour
        if task_data.at is not None:
            now = datetime.datetime.now()
            await asyncio.sleep((
                task_data.at
                - (datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second) % task_data.at)
            ).seconds)

            while True:
                await coroutine(self,transport)
                await asyncio.sleep(task_data.interval.total_seconds())

        # If we don't have to set the task at a certain part of the hour
        #   Start up the _loop regularly
        else:
            while True:
                await asyncio.sleep(task_data.interval.total_seconds())
                await coroutine(self,transport)


    @staticmethod
    def task(task_data:TaskData):
        """
        Decorator to be used by the BotData,
            to assign a method as a task that has to be run at a given interval
        """
        def decorator(fnc):
            assert inspect.iscoroutinefunction(fnc), f"{fnc} was not a asyncio coroutine"
            TaskLogic._logic_components.append((fnc, task_data))
            return fnc
        return decorator