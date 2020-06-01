"""Custom exceptions specific to the auraxium module."""


class AuraxiumException(BaseException):
    """Base exception class for auraxium.

    This can be caught to handle all exceptions specific to this
    library.
    """


class UserError(AuraxiumException):
    """Raised for exceptions resulting from improper API use.

    These exceptions should generally not be handled; fix the calling
    code to avoid the issue.
    """


class CensusError(AuraxiumException):
    """Raised for Census API-related errrors.

    These are generally not user-provoked and should rarely leave the
    wrapper module.
    """


class ResponseError(CensusError):
    """Exception for HTTP-related errors.

    This will generally be an instance of aiohttp.ClientResponse().
    """


class BadPayloadError(CensusError):
    """Raised if the payload returned by the API is unexpected.

    This could be due to API changes or other inconsistencies in the
    return data.
    """
