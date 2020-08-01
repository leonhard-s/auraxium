"""Alert and alert state class definitions."""

import dataclasses
import enum

from ..base import Cached, Ps2Data
from ..types import CensusData
from ..utils import LocaleData


class MetagameEventState(enum.IntEnum):
    """The state of a :class:`auraxium.ps2.metagame.MetagameEvent`."""

    STARTED = 135
    RESTARTED = 136
    CANCELLED = 137
    ENDED = 138
    XP_BONUS_CHANGED = 139


@dataclasses.dataclass(frozen=True)
class MetagameEventData(Ps2Data):
    """Data class for :class:`auraxium.ps2.metagame.MetagameEvent`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    metagame_event_id: int
    name: LocaleData
    description: LocaleData
    type: int
    experience_bonus: int

    @classmethod
    def from_census(cls, data: CensusData) -> 'MetagameEventData':
        return cls(
            int(data['metagame_event_id']),
            LocaleData.from_census(data['name']),
            LocaleData.from_census(data['description']),
            int(data['type']),
            int(data['experience_bonus']))


class MetagameEvent(Cached, cache_size=100, cache_ttu=60.0):
    """An event or alert on a continent."""

    collection = 'metagame_event'
    data: MetagameEventData
    id_field = 'metagame_event_id'

    @staticmethod
    def _build_dataclass(data: CensusData) -> MetagameEventData:
        return MetagameEventData.from_census(data)
