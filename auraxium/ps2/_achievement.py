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

    .. attribute:: id
       :type: int

       The unique ID of this achievement.

    .. attribute:: item_id
       :type: int

       The item associated with this achievement. An item ID of ``0``
       signifies that this achievement is a ribbon not tied to any
       weapon.

    .. attribute:: name
       :type: auraxium.types.LocaleData

       Localised name of the achievement.

    .. attribute:: objective_group_id
       :type: int

       The objective group tied to this achievement.

    .. attribute:: reward_id
       :type: int

       The reward granted when this achievement is earned.

    .. attribute:: repeatable
       :type: bool

       Whether this achievement is repeatable. Ribbons generally are
       repeatable, weapon medals are not.

    .. attribute:: description
       :type: auraxium.types.LocaleData

       The localised description of achievement.
    """

    collection = 'achievement'
    data: AchievementData
    id_field = 'achievement_id'
    _model = AchievementData

    # Type hints for data class fallback attributes
    id: int
    item_id: int
    name: LocaleData
    objective_group_id: int
    reward_id: int
    repeatable: bool
    description: LocaleData
