"""Shared utility methods used throughout Auraxium."""

import functools
import inspect
import warnings
from typing import Any, Callable, TypeVar, cast

__all__ = [
    'deprecated'
]

_CallableT = TypeVar('_CallableT', bound=Callable[..., Any])


def deprecated(start: str, removal_in: str, replacement: str = ''
               ) -> Callable[[_CallableT], _CallableT]:  # pragma: no cover
    """Mark the decorated function as deprecated.

    The `removal_in` argument may be used to specify a version at which
    the deprecated function will no longer be available.
    """

    def decorator(func: _CallableT) -> _CallableT:

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            msg = (f'{func.__name__} is deprecated and will be removed in '
                   f'version {removal_in}.')
            if replacement:
                msg += f' Use \'{replacement}\' instead'
            warnings.simplefilter('always', DeprecationWarning)
            warnings.warn(
                msg, category=DeprecationWarning, stacklevel=2)
            warnings.simplefilter('default', DeprecationWarning)
            return func(*args, **kwargs)

        wrapper.__doc__ = inspect.cleandoc(wrapper.__doc__ or '')
        wrapper.__doc__ += (
            f'\n\n.. deprecated:: {start}\n\n'
            f'   Scheduled for removal in {removal_in}.')
        if replacement:
            wrapper.__doc__ += f'\n   Use {replacement} instead.\n'
        return cast(_CallableT, wrapper)

    return decorator
