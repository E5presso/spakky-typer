import asyncio
from typing import Callable, Awaitable
from functools import wraps

from spakky.core.types import P, R


def run_async(func: Callable[P, Awaitable[R]]) -> Callable[P, R]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        async def coroutine_wrapper() -> R:
            return await func(*args, **kwargs)

        return asyncio.run(coroutine_wrapper())

    return wrapper
