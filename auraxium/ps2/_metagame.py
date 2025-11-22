"""Alert and alert state class definitions."""

import enum
from ..base import Cached
from ..models import MetagameEventData
from ..types import LocaleData

__all__ = [
    'MetagameEvent',
    'MetagameEventState'
]


class MetagameEventState(enum.IntEnum):
    """The state of a :class:`auraxium.ps2.MetagameEvent`.

    The following event state changes are currently recognised:::

       STARTED          = 135
       RESTARTED        = 136
       CANCELLED        = 137
       ENDED            = 138
       XP_BONUS_CHANGED = 139
    """

    STARTED = 135
    RESTARTED = 136
    CANCELLED = 137
    ENDED = 138
    XP_BONUS_CHANGED = 139


class MetagameEvent(Cached, cache_size=100, cache_ttu=60.0):
    """An event or alert on a continent.

    .. attribute:: id
       :type: int

       The unique ID of this event. In the API payload, this
       field is called ``metagame_event_id``.

    .. attribute:: name
       :type: auraxium.types.LocaleData

       The localised name of the event.

    .. attribute:: description
       :type: auraxium.types.LocaleData

       The localised description of the event.

    .. attribute:: type
       :type: int

       The type of event. Legacy alerts like "Dome Domination" used to
       share the same type despite being different events due to taking
       place on different continents.

    .. attribute:: experience_bonus
       :type: float | None

       The experience bonus applied to participating players in
       percent.
    """

    collection = 'metagame_event'
    data: MetagameEventData
    id_field = 'metagame_event_id'
    _model = MetagameEventData

    # Type hints for data class fallback attributes
    id: int
    name: LocaleData
    description: LocaleData
    type: int
    experience_bonus: float | None
