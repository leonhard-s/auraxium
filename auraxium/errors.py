"""Custom exceptions specific to the auraxium module."""

from typing import Optional

import aiohttp
import yarl

__all__ = [
    'AuraxiumException',
    'CensusError',
    'UnknownCollectionError',
    'ServiceUnavailableError',
    'InvalidServiceIDError',
    'MissingServiceIDError',
    'BadRequestSyntaxError',
    'ServerError',
    'InvalidSearchTermError',
    'MaintenanceError',
    'NotFoundError',
    'ResponseError',
    'PayloadError'
]


class AuraxiumException(Exception):
    """Base exception class for auraxium.

    This mostly exists to allow blanket-catching any errors specific to
    the auraxium module.
    """


class CensusError(AuraxiumException):
    """Raised for server-side API errors.

    These are errors that are reported by the API endpoint and mostly
    inform of syntax errors, as well as invalid operations or API
    outages.

    Attributes:
        url: The URL that gave rise to the error.

    """

    def __init__(self, message: str, url: yarl.URL) -> None:
        super().__init__(message)
        self.url = url


class UnknownCollectionError(CensusError):
    """Raised if the queried collection does not exist.

    For the purposes of this error, a collection is tied to its
    namespace (aka. game and platform). Together, they form a qualified
    collection name, e.g. ``ps2/character`` or ``dcuo/world``.
    """

    def __init__(self, message: str, url: yarl.URL, namespace: str,
                 collection: Optional[str]) -> None:
        super().__init__(message, url)
        self.namespace = namespace
        self.collection = collection


class ServiceUnavailableError(CensusError):
    """Raised if the API reports a service as temporarily unavailable.

    This is likely to occur after big patches, or when the API is
    undergoing maintenance or has other issues.

    The issue causing this error is often specific to individual
    collections like ``ps2/characters_online_status``, the rest of the
    API might be fine.

    Unlike :class:`MaintenanceError`, this error state often persists
    for hours or even days.
    """


class InvalidServiceIDError(CensusError):
    """Raised when using an unknown service ID.

    Make sure your service ID is spelled correctly.

    If you only just applied for a custom service ID, you will have to
    wait for an email response before it is valid and usable.
    """


class MissingServiceIDError(CensusError):
    """Raised when using the default service ID.

    This error is raised when using the default service ID,
    ``s:example``, beyond its 10 requests per minute limit.

    This is easily fixed by applying for a custom service ID at
    http://census.daybreakgames.com/#devSignup.

    Once you have your own service ID, pass it to the
    :class:`auraxium.Client` or :class:`auraxium.census.Query`
    class initialiser respectively.
    """


class BadRequestSyntaxError(CensusError):
    """Raised if the query string itself was erroneous.

    This error points to a bug in the :mod:`auraxium.census` module. If
    you encounter it, please submit an issue at
    https://github.com/leonhard-s/auraxium/issues.
    """


class ServerError(CensusError):
    """Server-side error encountered when parsing the query string.

    This error generally points to a bug either the
    :mod:`auraxium.census` URL generator, or the game-specific object
    model.

    If you encounter this instance in the wild (i.e. not one of its
    subclasses), please submit an issue at
    https://github.com/leonhard-s/auraxium/issues.
    """


class InvalidSearchTermError(ServerError):
    """Server error for invalid search term strings.

    This means received when misusing API collections, or when trying
    to perform an invalid or unsupported operation on a given field.

    Attributes:
        collection: The collection that was accessed.
        namespace: The namespace of the collection.
        field: The field that caused the error. Might be ``None`` if
            the culprit could not be determined.

    """

    def __init__(self, message: str, url: yarl.URL, namespace: str,
                 collection: str, field: Optional[str]) -> None:
        super().__init__(message, url)
        self.namespace = namespace
        self.collection = collection
        self.field = field


class MaintenanceError(CensusError):
    """Raised if the API is down or undergoing maintenance."""

    def __init__(self, message: str, url: yarl.URL,
                 response: Optional[aiohttp.ClientResponse]) -> None:
        super().__init__(message, url)
        self.response = response


class ResponseError(AuraxiumException):
    """Raised for unexpected or invalid API responses.

    This can generally not be handled. Please submit an issue at
    https://github.com/leonhard-s/auraxium/issues if you encounter this
    error repeatedly.
    """


class PayloadError(AuraxiumException):
    """Raised if the payload returned by the API is unexpected.

    This generally points to a bug in the object model, or to the API
    having changed and requiring the object model to be updated.

    Please submit an issue at
    https://github.com/leonhard-s/auraxium/issues either way.
    """


class NotFoundError(AuraxiumException):
    """Raised if a request unexpectedly did not return any matches."""
