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
        id: The unique ID of this achievement.
        item_id: The item associated with this achievement. An item ID
            of ``0`` signifies that this achievement is a ribbon not
            tied to any weapon.
        name: Localised name of the achievement.
        objective_group_id: The objective group tied to this
            achievement.
        reward_id: The reward granted when this achievement is earned.
        repeatable: Whether this achievement is repeatable. Ribbons
            generally are repeatable, weapon medals are not.
        description: The localised description of achievement.

    """

    collection = 'achievement'
    data: AchievementData
    dataclass = AchievementData
    id_field = 'achievement_id'

    # Type hints for data class fallback attributes
    id: int
    item_id: int
    name: LocaleData
    objective_group_id: int
    reward_id: int
    repeatable: bool
    description: LocaleData
