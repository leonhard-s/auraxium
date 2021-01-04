"""Data classes for :mod:`auraxium.ps2.metagame`."""

from typing import Optional

from ..base import Ps2Data
from ..types import LocaleData

__all__ = [
    'MetagameEventData'
]

# pylint: disable=too-few-public-methods


class MetagameEventData(Ps2Data):
    """Data class for :class:`auraxium.ps2.metagame.MetagameEvent`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        metagame_event_id: The unique ID of this event.
        name: The localised name of the event.
        description: The localised description of the event.
        type: The type of event. Legacy alerts like "Dome Domination"
            used to share the same type despite being different events
            due to taking place on different continents.
        experience_bonus: The experience bonus applied to players in
            percent.

    """

    metagame_event_id: int
    name: LocaleData
    description: LocaleData
    type: int
    experience_bonus: Optional[int] = None
