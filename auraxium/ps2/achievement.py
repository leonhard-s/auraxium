"""Achievement class definition.

Achievements include weapon medals and service ribbons.
"""

from ..base import ImageMixin, Named
from ..models import AchievementData
from ..types import LocaleData


class Achievement(Named, ImageMixin, cache_size=50, cache_ttu=60.0):
    """An achievement a player may pursue.

    Achievements include weapon medals and service ribbons.
    """

    collection = 'achievement'
    data: AchievementData
    dataclass = AchievementData
    id_field = 'achievement_id'

    # Type hints for data class fallback attributes
    achievement_id: int
    item_id: int
    objective_group_id: int
    reward_id: int
    repeatable: bool
    name: LocaleData
    description: LocaleData
