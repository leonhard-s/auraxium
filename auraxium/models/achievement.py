"""Data classes for :mod:`auraxium.ps2.achievement`."""

import dataclasses

from ..base import Ps2Data
from ..types import CensusData, LocaleData

__all__ = [
    'AchievementData'
]


@dataclasses.dataclass(frozen=True)
class AchievementData(Ps2Data):
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
        image_set_id: The image set associated with this achievement.
        image_id: The default image for this achievement.
        image_path: The image path for this achievement.

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
            int(data.pop('achievement_id')),
            int(data.pop('item_id')),
            int(data.pop('objective_group_id')),
            int(data.pop('reward_id')),
            bool(int(data.pop('repeatable'))),
            LocaleData.from_census(data.pop('name')),
            LocaleData.from_census(data.pop('description')),
            int(data.pop('image_set_id')),
            int(data.pop('image_id')),
            str(data.pop('image_path')))
