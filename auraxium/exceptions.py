"""auraxium exceptions."""

__all__ = ['AuraxiumError', 'InvalidSearchTermError', 'UserError', 'MaintenanceError']


class AuraxiumError(Exception):
    """Superclass for all auraxium-specific exceptions."""


class UserError(AuraxiumError):
    """Superclass for errors resulting from poor user decisions."""


class InvalidSearchTermError(UserError):
    """The user attempted to search a collection by a field it does
    not posess.

    """


class RegExTooShortError(UserError):
    """The user attempted to perform a RegEx search (i.e. a string
    match using the "contains" or "starts_with" search modifier)
    while specifying less than three characters to match.

    """


class UnknownCollectionError(UserError):
    """The user attempted to access a collection that does not exist
    for the current namespace.

    """


class ServerError(AuraxiumError):
    """Superclass for errors resulting in unexpected server-side
    occurrences.

    """


class MaintenanceError(ServerError):
    """The API endpoint is curently undergoing maintenance."""


class ServiceUnavailableError(ServerError):
    """Raised when attempting to access a disabled collection.

    Commonly occurs with the "characters_friend" and
    "characters_online_status" collections.

    The corresponding server response will look something like this:
    {"error":"service_unavailable"}

    """


class SerciceIDError(AuraxiumError):
    """Superclass for errors stemming from improper service ID use."""


class ServiceIDMissingError(SerciceIDError):
    """Raised when repeatedly sending requests without a valid
    service ID.

    """


class ServiceIDUnknownError(SerciceIDError):
    """Raised when the server cannot find the given service id."""
