"""Armor mapping class definitions."""

import enum
from typing import Optional

from .._base import Cached
from ..models import ArmourInfoData

__all__ = [
    'ArmourFacing',
    'ArmourInfo'
]


class ArmourFacing(enum.IntEnum):
    """Enumerator for armour facing directions.

    This is used to list different armour values for a vehicle based on
    the angle of attack.
    """

    FRONT = 0
    RIGHT = 1
    TOP = 2
    REAR = 3
    LEFT = 4
    BOTTOM = 5
    ALL = 6


class ArmourInfo(Cached, cache_size=100, cache_ttu=60.0):
    """An armour stat for a given entity.

    Note that any given entity may have multiple :class:`ArmourInfo`
    instances associated with it, one for each :class:`ArmourFacing`
    value.

    Attributes:
        armor_info_id: The unique ID of this entry.
        armor_facing_id: The enum value the facing direction this entry
            provides armour data for.
        armor_percent: Damage reduction in percent.
        armor_amount: A flat damage absorption applied to the damage
            effect; generally unused.
        description: A description for this entry.

    """

    collection = 'armor_info'
    data: ArmourInfoData
    _dataclass = ArmourInfoData
    id_field = 'armor_info_id'

    # Type hints for data class fallback attributes
    armor_info_id: int
    armor_facing_id: int
    armor_percent: int
    armor_amount: Optional[int]
    description: str

    @property
    def facing(self) -> ArmourFacing:
        """Return the facing direction for this stat entry."""
        return ArmourFacing(self.data.armor_info_id)
