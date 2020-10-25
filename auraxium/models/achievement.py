"""Data classes for :mod:`auraxium.ps2.achievement`."""

from ..base import ImageData, Ps2Data
from ..types import LocaleData

__all__ = [
    'AchievementData'
]


class AchievementData(Ps2Data, ImageData):
    """Data class for :class:`auraxium.ps2.achievement.Achievement`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

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

    achievement_id: int
    item_id: int
    objective_group_id: int
    reward_id: int
    repeatable: bool
    name: LocaleData
    description: LocaleData
