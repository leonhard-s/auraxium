"""Achievement class definition.

Achievements include weapon medals and service ribbons.
"""

from ..base import ImageMixin, Named
from ..models import AchievementData
from ..types import LocaleData

__all__ = [
    'Achievement'
]


class Achievement(Named, ImageMixin, cache_size=50, cache_ttu=60.0):
    """An achievement a player may pursue.

    Achievements include weapon medals and service ribbons.

    Attributes:
        achievement_id: The unique ID of this achievement.
        item_id: The item associated with this achievement. An item ID
            of ``0`` signifies that this achievement is a ribbon not
            tied to any weapon.
        objective_group_id: The objective group tied to this
            achievement.
        reward_id: The reward granted when this achievement is earned.
        repeatable: Whether this achievement is repeatable. Ribbons
            generally are repeatable, weapon medals are not.
        name: The localised name of the achievement.
        description: The localised description of achievement.

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
