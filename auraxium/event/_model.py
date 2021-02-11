"""Base classes for event base and mixin classes."""

import datetime

from ..base import Ps2Data


class Event(Ps2Data):
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
