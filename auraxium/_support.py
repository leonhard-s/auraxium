"""Shared utility methods used throughout Auraxium."""

import functools
import warnings
from typing import Any, Callable, TypeVar, cast

__all__ = [
    'deprecated'
]

_CallableT = TypeVar('_CallableT', bound=Callable[..., Any])


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
