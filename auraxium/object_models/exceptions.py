"""Exception definitions for the object_models submodule."""

from ..exceptions import AuraxiumError, UserError


class UnknownEventTypeError(AuraxiumError):
    """Raised when the ESS client receives an unknown event response type."""


class NoMatchesFoundError(UserError):
    """Raised when a search comes back empty."""
