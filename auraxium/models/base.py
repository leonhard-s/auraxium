"""Shared base classes for API data model implementations."""

import abc
import datetime
from typing import Any, Optional, TypeVar, cast

import pydantic

from ..types import CensusData

# pylint: disable=too-few-public-methods

_T = TypeVar('_T')


class Payload(pydantic.BaseModel):
    """A payload received through the REST or WebSocket interface.

    Instances of this class are read-only.
    """

    class Config:
        """Pydantic model configuration.

        :meta private:
        """

        allow_mutation = False

    # Weird workaround for pydantic.BaseModel overwriting __hash__ with
    # None, at least according to Pylance.

    def _override__hash__(self) -> int:
        # NOTE: pydantic has a beta setting called `frozen=True` that would
        # generate a hash method, but it is not part of the stable API and
        # therefore not used here.
        # It should replace allow_mutation here once it out of beta.
        return hash(tuple(self.dict().items()))

    __hash__ = cast(Any, _override__hash__)


class RESTPayload(Payload):
    """A JSON payload received through the REST interface.

    This :class:`Payload` subclass implicitly converts NULL strings to
    :obj:`None`.
    """

    @pydantic.validator('*', pre=True)
    @classmethod
    def _convert_null(cls, value: _T) -> Optional[_T]:
        """Replace any "NULL" string inputs with :obj:`None`.

        This is a pre-validator; it is run before any other validation
        or conversion takes place.

        By default, the API will omit any NULL fields in the
        response unless the ``c:includeNull`` flag is set. In Python,
        a missing value is instead. This also ensures that optional
        values can be type-hinted with :obj:`typing.Optional` without
        risk of errors.
        """
        _ = cls
        if value == 'NULL':
            return None
        return value


class FallbackMixin(metaclass=abc.ABCMeta):
    """A mixin class used to provide hard-coded fallback instances.

    Some collections are out of date and do not contain all required
    data. This mixin provides a hook to insert this missing data into
    data types while not causing issues if the API ends up being
    updated to include these missing types.

    Subclasses must implement the :meth:`fallback_hook` method to
    inject custom fallback data into the type. If no value can be
    provided for a given `id_`, a :exc:`KeyError` should be raised.
    """

    @staticmethod
    @abc.abstractmethod
    def fallback_hook(id_: int) -> CensusData:
        """Hook for retrieving hard-coded fallback data.

        Some collections are missing data or providing bad data for
        some or all IDs. This method provides a non-destructive hook
        for inserting missing data if the API cannot produce a value.

        :param int id_: The ID of the value to look up.
        :raises KeyError: Raised if no fallback data can be provided
           for the given `id_`.
        :return: A fallback payload to treat as if it came from the
           server.
        """


class ImageData(pydantic.BaseModel):
    """Mixin dataclass for types supporting image access.

    .. attribute:: image_id
       :type: int | None

       The default image ID of the object.

    .. attribute:: image_set_id
       :type: int | None

       The image set ID of the object.

    .. attribute:: image_path
       :type: str | None

       The base path to the default :attr:`image_id`.
    """

    image_id: Optional[int] = None
    image_set_id: Optional[int] = None
    image_path: Optional[str] = None


class Event(Payload):
    """An event returned via the ESS websocket connection.

    .. attribute:: event_name
       :type: str
       :noindex:

       The raw event name linked to this type. Generally identical to
       the name of the class.

    .. attribute:: timestamp
       :type: int
       :noindex:

       The UTC timestamp of the event. May be used to infer latency to
       the event streaming endpoint.

    .. attribute:: world_id
       :type: int
       :noindex:

       ID of the :class:`~auraxium.ps2.World` whose event streaming
       endpoint broadcast the event.
    """

    event_name: str
    timestamp: datetime.datetime
    world_id: int

    @property
    def age(self) -> float:
        """The age of the event in seconds."""
        now = datetime.datetime.now()
        return (self.timestamp - now).total_seconds()


class CharacterEvent:
    """Mixin class for character-centric events.

    Events inheriting from this class support subscription by character
    ID.
    """

    # NOTE: This may not inherit from ``Event`` as this would cause an
    # ambiguous MRO for "PlayerLogin"/"-Logout" events, which are both
    # character- and world-centric.


class WorldEvent:
    """Mixin class for world-centric events.

    Events inheriting from this class support subscription by world ID.
    """

    # NOTE: This may not inherit from ``Event`` as this would cause an
    # ambiguous MRO for "PlayerLogin"/"-Logout" events, which are both
    # character- and world-centric.
