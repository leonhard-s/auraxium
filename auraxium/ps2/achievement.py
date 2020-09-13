"""Achievement class definition.

Achievements include weapon medals and service ribbons.
"""

from ..base import Named
from ..models import AchievementData
from ..types import CensusData


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
