"""Helper module for implementing exponential backoff strategies.

Interface is designed to be compatible with the abandoned `backoff`
project (https://github.com/litl/backoff), but no code has been adopted.
"""

import asyncio
import functools
import inspect
import time
import typing
from collections.abc import Callable, Generator, Iterable

__all__ = [
    'BackoffHandler',
    'Details',
    'expo',
]

_FuncT = typing.TypeVar('_FuncT', bound=Callable[..., typing.Any])
_BackoffGenerator = Generator[float, None, None]
BackoffHandler = Callable[['Details'], None]


class Details(typing.TypedDict):
    """Details dictionary passed to backoff handlers."""

    elapsed: float
    tries: int
    wait: float


def expo(base: float, factor: float,
         max_value: float | None = None) -> Generator[float, None, None]:
    """Exponential backoff generator.

    :param base: The base of the exponentiation.
    :param factor: The factor to multiply the exponentiation by.
    :param max_value: The maximum value to yield.
    :yield: The next backoff time in seconds.
    """
    yield 0.0  # No delay for the first attempt
    n = 0
    while True:
        value = factor * (base ** n)
        if max_value is not None and value > max_value:
            yield max_value
        else:
            yield value
            n += 1


def on_exception(
    gen: _BackoffGenerator,
    exceptions: Iterable[type[Exception]],
    max_tries: int,
    on_backoff: BackoffHandler | None = None,
    on_giveup: BackoffHandler | None = None,
    on_success: BackoffHandler | None = None,
) -> Callable[[_FuncT], _FuncT]:
    """Decorator for backoff and retry triggered by exceptions.

    The decorated function will be retried with the configured
    backoff generator up to `max_tries` times if it raises one of the
    specified exceptions.

    :param gen: A generator yielding successive wait times in seconds.
    :param exceptions: An iterable of exception types which trigger
        backoff.
    :param max_tries: The maximum number of attempts to make before
        giving up.
    :param on_backoff: Optional handler called when backing off.
    :param on_giveup: Optional handler called when giving up.
    :param on_success: Optional handler called on successful call.
    :return: A decorator which applies the backoff strategy to a function.
    """
    if not inspect.isgenerator(gen):
        raise TypeError('gen must be a generator instance')
    if max_tries < 1:
        raise ValueError('max_tries must be at least 1')
    if inspect.iscoroutinefunction(gen):
        raise TypeError('gen must be a synchronous generator')

    def decorate(func: _FuncT) -> _FuncT:
        if inspect.iscoroutinefunction(func):
            @functools.wraps(func)
            async def wrapper_async(
                    *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
                started = time.monotonic()
                details: Details = {'elapsed': 0.0, 'tries': 0, 'wait': 0.0}
                while details['tries'] <= max_tries:
                    try:
                        details['tries'] += 1
                        details['elapsed'] = time.monotonic() - started
                        result = await func(*args, **kwargs)
                        if on_success is not None:
                            on_success(details)
                        return result
                    except (*exceptions,):
                        if details['tries'] > max_tries:
                            if on_giveup is not None:
                                on_giveup(details)
                            raise
                        wait = next(gen)
                        details['wait'] = wait
                        if on_backoff is not None:
                            on_backoff(details)
                        await asyncio.sleep(wait)
                raise RuntimeError(
                    'Unreachable code reached in backoff decorator')
            return typing.cast(_FuncT, wrapper_async)

        @functools.wraps(func)
        def wrapper_sync(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
            started = time.monotonic()
            details: Details = {'elapsed': 0.0, 'tries': 0, 'wait': 0.0}
            while details['tries'] <= max_tries:
                try:
                    details['tries'] += 1
                    details['elapsed'] = time.monotonic() - started
                    result = func(*args, **kwargs)
                    if on_success is not None:
                        on_success(details)
                    return result
                except (*exceptions,):
                    if details['tries'] > max_tries:
                        if on_giveup is not None:
                            on_giveup(details)
                        raise
                    wait = next(gen)
                    details['wait'] = wait
                    if on_backoff is not None:
                        on_backoff(details)
                    time.sleep(wait)
            raise RuntimeError('Unreachable code reached in backoff decorator')

        return typing.cast(_FuncT, wrapper_sync)

    return decorate
