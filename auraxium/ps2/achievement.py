"""Achievement class definition.

Achievements include weapon medals and service ribbons.
"""

from ..base import ImageMixin, Named
from ..models import AchievementData


class Achievement(Named, ImageMixin, cache_size=50, cache_ttu=60.0):
    """An achievement a player may pursue.

    Achievements include weapon medals and service ribbons.
    """

    collection = 'achievement'
    data: AchievementData
    dataclass = AchievementData
    id_field = 'achievement_id'
