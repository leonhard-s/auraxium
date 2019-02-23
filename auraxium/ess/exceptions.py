"""Custom exceptions used by the ESS submodule.

All exceptions are still subclassed to `AuraxiumError`, as well as
`AuraxiumESSError` defined herein.
"""

from ..exceptions import AuraxiumError


class AuraxiumESSError(AuraxiumError):
    """Base exception for exceptions raised by the ESS submodule."""


class UnknownEventTypeError(AuraxiumESSError):
    """Raised when the ESS client receives an unknown event type."""


class EventTypeAmbiguityError(AuraxiumESSError):
    """Raised when multiple event objects reference the same census
    event name.
    """
