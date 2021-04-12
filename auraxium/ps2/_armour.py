"""Armor mapping class definitions."""

import enum
from typing import Optional

from ..base import Cached
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

    .. attribute:: id
       :type: int

       The unique ID of this entry.

    .. attribute:: armor_facing_id
       :type: int

       The enum value the facing direction this entry
            provides armour data for.

    .. attribute:: armor_percent
       :type: int

       Damage reduction in percent. A value of 10 signifies a 10%
       reduction.

    .. attribute:: armor_amount
       :type: int | None

       A flat damage absorption applied to the damage effect.

       .. note::

          This field is generally unused since the 2017 armour rework
          as part of the "Critical Mass" game update.

    .. attribute:: description
       :type: str

       A description of what situation this armour info entry is used
       for.
    """

    collection = 'armor_info'
    data: ArmourInfoData
    id_field = 'armor_info_id'
    _model = ArmourInfoData

    # Type hints for data class fallback attributes
    id: int
    armor_facing_id: int
    armor_percent: int
    armor_amount: Optional[int]
    description: str

    @property
    def facing(self) -> ArmourFacing:
        """Return the facing direction for this stat entry."""
        return ArmourFacing(self.data.armor_info_id)
