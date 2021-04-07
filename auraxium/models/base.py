"""Shared base classes for API data model implementations."""

import abc
import dataclasses
import datetime
from typing import Optional, TypeVar

import pydantic

from ..types import CensusData

# pylint: disable=too-few-public-methods

_T = TypeVar('_T')


class Payload(pydantic.BaseModel):
    """A payload received through the REST or WebSocket interface.

    Instances of this class are read-only.
    """

    class Config:
        """Pydantic model configuration."""

        allow_mutation = False


class RESTPayload(Payload):

    @pydantic.validator('*', pre=True)
    @classmethod
    def _convert_null(cls, value: _T) -> Optional[_T]:
        """Replace any "NULL" string inputs with :obj:`None`.

        This is a pre-validator; it is run before any other validation
        or conversion takes place.

        By default, the API will omit any "NULL" fields in the
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
    """

    @staticmethod
    @abc.abstractmethod
    def fallback_hook(id_: int) -> CensusData:
        ...


@dataclasses.dataclass(frozen=True)
class ImageData:
    """Mixin dataclass for types supporting image access."""

    image_id: Optional[int] = None
    image_set_id: Optional[int] = None
    image_path: Optional[str] = None


class Event(Payload):
    """An event returned via the ESS websocket connection."""

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

    Events inheriting from this calss support subscription by character
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
