class AuraxiumBaseError(Exception):
    """The base exception for all the module's exceptions."""
    pass


class ServiceUnavailableError(AuraxiumBaseError):
    """Raised when attempting to access a disabled collection.

    Commonly occurs with the "characters_friend" and "characters_online_status"
    collections.

    The corresponding server response will look something like this:
    {"error":"service_unavailable"}
    """
    pass


class APILimitationError(AuraxiumBaseError):
    """Raised when a known limitation is breached.
    """
    pass


class UnknownCollectionError(AuraxiumBaseError):
    """Raised when attempting to access a collection that does not exist.

    Usually occurs with typos or otherwise incorrect collection names, such as
    "character_online_status" instead of "characters_online_status" (plural!).

    The corresponding server response will look something like this:
    {"error":"No data found."}
    """
    pass


class InvalidJoinError(AuraxiumBaseError):
    """Raised when attempting to perform a joined query while using the count
    verb.
    """
    pass


class InvalidSearchTermError(AuraxiumBaseError):
    """Occurs when attempting to filter a collection by an invalid field.

    Sometimes this means that the field does not exist at all, but some fields
    can also not be used in searches (see exceptions/limitations in the API
    documentation for more information).

    The corresponding server response will look something like this:
    {"errorCode":"SERVER_ERROR","errorMessage":"INVALID_SEARCH_TERM: Invalid search term. Valid search terms: [description_t4id, name_t4id, state, world_id]"}
    """
    pass


class ServiceIDMissingError(AuraxiumBaseError):
    """Raised when repeatedly sending requests without a valid service ID.

    The API allows about six requests per minute and IP address for public
    service IDs. For more bandwidth, a service ID has to be provided.

    The corresponding server response will look something like this:
    {"error":"Missing Service ID.  A valid Service ID is required for continued api use.  The Service ID s:example is for casual use only.  (http://census.daybreakgames.com/#devSignup)"}
    """
    pass


class ServiceIDUnknownError(AuraxiumBaseError):
    """Raised when the server cannot find the given service ID.

    This can either mean a typo in the service ID itself, but it can also occur
    when a new service ID is used that has only been created a few hours ago.
    In the latter case, the issue will resolve itself with a bit more time.

    The corresponding server response will look something like this:
    {"error":"Provided Service ID is not registered.  A valid Service ID is required for continued api use. (http://census.daybreakgames.com/#devSignup)"}#
    """
    pass
