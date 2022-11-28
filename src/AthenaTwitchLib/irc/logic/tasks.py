# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

import asyncio
import datetime
from collections.abc import Awaitable
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any
from typing import NoReturn
from typing import Protocol
from typing import Self

from AthenaTwitchLib.irc.logic._logic import BaseHardCodedLogic
from AthenaTwitchLib.irc.logic._logic import BaseTaskLogic
from AthenaTwitchLib.irc.logic._logic import register_callback_as_logical_component
from AthenaTwitchLib.irc.logic._logic import TBHCL
from AthenaTwitchLib.irc.logic.commands import CLCommand
# Athena Packages
# Local Imports


# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class TLCommand(TBHCL, Protocol):
    @property
    def _data(self) -> TaskData: ...

    @_data.setter
    def _data(self, __val: TaskData) -> None: ...

    def __call__(self, *args: Any, **kwargs: Any) -> Any: ...


@dataclass(slots=True, kw_only=True)
class TaskData:
    """
    Simple dataclass to hold basic information about the hard coded task.
    Meant for the `TaskLogic` class to differentiate what to do when it needs to execute the tasks
    """
    at:datetime.timedelta|None = None
    interval:datetime.timedelta = datetime.timedelta(seconds=0)
    channel:str|None = None

    def __post_init__(self) -> None:
        if self.at is not None:
            self.interval = self.at

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class TaskLogic(BaseHardCodedLogic,BaseTaskLogic):
    """
    Logic system behind hard coded tasks.
    """
    open_tasks:list[asyncio.Task[TaskData]]
    _tasks:list[tuple[Callable[[asyncio.Transport], Awaitable[None]], TaskData]]

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:  # type: ignore [valid-type,misc]
        obj = super().__new__(cls, *args, *kwargs)

        # retrieve all tasks
        obj._tasks = [  # type: ignore [attr-defined]
            (coroutine, coroutine._data)
            for coroutine in
            obj._logic_components  # type: ignore [attr-defined]
        ]

        # Extract data from the bot, and make sure that tasks adhere to this

        obj.open_tasks = []  # type: ignore [attr-defined]
        return obj

    def start_all_tasks(self, transport:asyncio.Transport, loop:asyncio.AbstractEventLoop) -> None:
        if self.open_tasks:
            self.stop_all_tasks()

        self.open_tasks = [
            loop.create_task(self._create_task(transport, coroutine, task_data))
            for coroutine, task_data in self._tasks
        ]

    def stop_all_tasks(self) -> None:
        for task in self.open_tasks:
            task.cancel()
        self.open_tasks.clear()

    async def _create_task(self, transport:asyncio.Transport, coroutine:Callable[[asyncio.Transport], Awaitable[None]], task_data:TaskData) -> NoReturn:
        """
        Main function of a task
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
                await coroutine(transport)
                await asyncio.sleep(task_data.interval.total_seconds())

        # If we don't have to set the task at a certain part of the hour
        #   Start up the loop regularly
        else:
            while True:
                await asyncio.sleep(task_data.interval.total_seconds())
                await coroutine(transport)


    @staticmethod
    def task(task_data:TaskData) -> Callable[[TLCommand], TLCommand]:
        """
        Decorator to be used by the Bot,
            to assign a method as a task that has to be run at a given interval
        """
        def decorator(fnc: TLCommand) -> TLCommand:
            register_callback_as_logical_component(fnc)
            fnc._data = task_data
            return fnc
        return decorator
