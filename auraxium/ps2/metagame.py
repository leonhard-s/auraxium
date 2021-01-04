"""Alert and alert state class definitions."""

import enum

from ..base import Cached
from ..models import MetagameEventData


class MetagameEventState(enum.IntEnum):
    """The state of a :class:`auraxium.ps2.metagame.MetagameEvent`."""

    STARTED = 135
    RESTARTED = 136
    CANCELLED = 137
    ENDED = 138
    XP_BONUS_CHANGED = 139


class MetagameEvent(Cached, cache_size=100, cache_ttu=60.0):
    """An event or alert on a continent."""

    collection = 'metagame_event'
    data: MetagameEventData
    dataclass = MetagameEventData
    id_field = 'metagame_event_id'
