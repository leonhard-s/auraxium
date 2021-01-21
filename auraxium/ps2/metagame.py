"""Alert and alert state class definitions."""

import enum
from typing import Optional

from .._base import Cached
from ..models import MetagameEventData
from ..types import LocaleData

__all__ = [
    'MetagameEvent',
    'MetagameEventState'
]


class MetagameEventState(enum.IntEnum):
    """The state of a :class:`auraxium.ps2.metagame.MetagameEvent`."""

    STARTED = 135
    RESTARTED = 136
    CANCELLED = 137
    ENDED = 138
    XP_BONUS_CHANGED = 139


class MetagameEvent(Cached, cache_size=100, cache_ttu=60.0):
    """An event or alert on a continent.

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

    collection = 'metagame_event'
    data: MetagameEventData
    dataclass = MetagameEventData
    id_field = 'metagame_event_id'

    # Type hints for data class fallback attributes
    metagame_event_id: int
    name: LocaleData
    description: LocaleData
    type: int
    experience_bonus: Optional[int]
