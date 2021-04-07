"""Shared utility methods used throughout Auraxium."""

import functools
import warnings
from typing import Any, Callable, Iterator, TypeVar, cast

import backoff

__all__ = [
    'expo_scaled'
]

_CallableT = TypeVar('_CallableT', bound=Callable[..., Any])


def expo_scaled(factor: float = 1.0, max_: float = 3600.0
                ) -> Callable[[], Iterator[float]]:
    """Reusable factory for scaling :meth:`backoff.expo` values.

    This allows reducing the initial retry times for request retries.
    The returned function can be passed to the regular backoff handlers
    like :meth:`backoff.on_exception`.

    Arguments:
        factor (optional): The scaling factor for the exponential.
        Defaults to ``1.0``.
        max_ (optional): The maximum delay to wait for. Defaults to
        ``3600.0``.

    Returns:
        A callable that returns an iterator returning the delay to use
        in seconds.

    """
    gen: Iterator[float] = backoff.expo(base=2, max_value=max_)  # type: ignore

    def inner() -> Iterator[float]:
        """A scaled version :meth:`backoff.expo`."""
        while True:
            try:
                yield next(gen) * factor
            except StopIteration:
                return

    return inner


def deprecated(removed_in_version: str, replacement: str = ''
               ) -> Callable[[_CallableT], _CallableT]:
    """Mark the decorated function as deprecated.

    The `removal_in` argument may be used to specify a version at which
    the deprecated function will no longer be available.
    """

    def decorator(func: _CallableT) -> _CallableT:

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            msg = (f'{func.__name__} is deprecated and will be removed in '
                   f'version {removed_in_version}.')
            if replacement:
                msg += f' Use \'{replacement}\' instead'
            warnings.simplefilter('always', DeprecationWarning)
            warnings.warn(
                msg, category=DeprecationWarning, stacklevel=2)
            warnings.simplefilter('default', DeprecationWarning)
            return func(*args, **kwargs)

        return cast(_CallableT, wrapper)

    return decorator
