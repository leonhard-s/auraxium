"""Achievement class definition.

Achievements include weapon medals and service ribbons.
"""

import dataclasses

from ..base import Named, Ps2Data
from ..types import CensusData
from ..utils import LocaleData


@dataclasses.dataclass(frozen=True)
class AchievementData(Ps2Data):
    """Data class for :class:`auraxium.ps2.achievement.Achievement`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    achievement_id: int
    item_id: int
    objective_group_id: int
    reward_id: int
    repeatable: bool
    name: LocaleData
    description: LocaleData
    image_set_id: int
    image_id: int
    image_path: str

    @classmethod
    def from_census(cls, data: CensusData) -> 'AchievementData':
        return cls(
            int(data['achievement_id']),
            int(data['item_id']),
            int(data['objective_group_id']),
            int(data['reward_id']),
            bool(int(data['repeatable'])),
            LocaleData.from_census(data['name']),
            LocaleData.from_census(data['description']),
            int(data['image_set_id']),
            int(data['image_id']),
            str(data['image_path']))


class Achievement(Named, cache_size=50, cache_ttu=60.0):
    """An achievement a player may pursue.

    Achievements include weapon medals and service ribbons.
    """

    collection = 'achievement'
    data: AchievementData
    id_field = 'achievement_id'

    @staticmethod
    def _build_dataclass(data: CensusData) -> AchievementData:
        return AchievementData.from_census(data)
