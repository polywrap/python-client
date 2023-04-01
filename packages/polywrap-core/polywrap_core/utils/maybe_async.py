"""This module contains the utility function for executing a function that may be async."""
from __future__ import annotations

import inspect
from typing import Any, Awaitable, Callable, Optional, Union


def is_coroutine(test: Optional[Union[Awaitable[Any], Any]] = None) -> bool:
    """Check if the given object is a coroutine."""
    return test is not None and inspect.iscoroutine(test)


async def execute_maybe_async_function(func: Callable[..., Any], *args: Any) -> Any:
    """Execute a function that may be async."""
    result = func(*args)
    if is_coroutine(result):
        result = await result
    return result
