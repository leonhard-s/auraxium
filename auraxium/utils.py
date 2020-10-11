"""Shared utility methods used throughout Auraxium."""

from typing import Callable, Iterator

import backoff


def expo_scaled(factor: float = 1.0) -> Callable[[], Iterator[float]]:
    """Reusable factory for scaling :meth:`backoff.expo` values.

    This allows reducing the initial retry times for request retries.
    The returned function can be passed to the regular backoff handlers
    like :meth:`backoff.on_exception`.

    Arguments:
        factor (optional): The scaling factor for the exponential.
        Defaults to 1.0.

    Returns:
        A callable that returns an iterator returning the delay to use
        in seconds.

    """
    gen: Iterator[float] = backoff.expo(base=2)  # type: ignore

    def inner() -> Iterator[float]:
        """A scaled version :meth:`backoff.expo`."""
        while True:
            try:
                yield next(gen) * factor
            except StopIteration:
                return

    return inner
