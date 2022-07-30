from __future__ import annotations

from dataclasses import dataclass
import sys
import typing


_T = typing.TypeVar('_T')


def _dataclass(**kwargs) -> typing.Callable[[typing.Type[_T]], typing.Type[_T]]:
    if sys.version_info >= (3, 10):
        return dataclass(**kwargs)
    else:
        kwargs.pop('slots', None)
        kwargs.pop('kw_only', None)
        return dataclass(**kwargs)