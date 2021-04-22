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

    This enum is used to list different :class:`ArmourInfo` values for
    the same vehicle depending on the attacker's position.

    Note that this mechanic uses the relative position of the attacker
    and the impacted vehicle, not the impact location the projectile.

    Values:::

       FRONT  = 0
       RIGHT  = 1
       TOP    = 2
       REAR   = 3
       LEFT   = 4
       BOTTOM = 5
       ALL    = 6
    """

    FRONT = 0
    RIGHT = 1
    TOP = 2
    REAR = 3
    LEFT = 4
    BOTTOM = 5
    ALL = 6

    def __str__(self) -> str:
        literals = ['Front', 'Right', 'Top', 'Rear', 'Left', 'Bottom', 'All']
        return literals[int(self.value)]


class ArmourInfo(Cached, cache_size=100, cache_ttu=60.0):
    """An armour info entry for an entity.

    Armour is a vehicle-specific property that modifies incoming damage
    depending on the angle of attack. Note that this mechanic uses the
    relative position of the attacker and the impacted vehicle, not the
    impact location the projectile.

    A vehicle may have multiple :class:`ArmourInfo` entries associated
    with different :class:`ArmourFacing` directions.

    Note that these armour percentages may be negative, in which case
    the damage dealt is increased beyond the base damage of the weapon.

    .. seealso::

       :class:`auraxium.ps2.Profile.armour_info` -- Access the armour
       info entries for a given :class:`auraxium.ps2.Profile`.

    .. attribute:: id
       :type: int

       The unique ID of this entry. In the API payload, this field is
       called ``armour_info_id``.

    .. attribute:: armor_facing_id
       :type: int

       The integer representation of the :class:`ArmourFacing` enum
       value this entry provides armour data for.

       .. seealso::

          :attr:`facing` -- The enum value of this entry.

    .. attribute:: armor_percent
       :type: int

       Damage reduction in percent. A value of 10.0 denotes an armour
       reduction of 10 percent. Negative armour values will increase
       damage taken:::

          actual_damage = (1 - (resistance / 100)) * base_damage

    .. attribute:: armor_amount
       :type: int | None

       A flat damage reduction applied to the damage effect prior to
       the percentage reduction.

       .. note::

          This field is unused since the 2017 armour rework as part of
          the "Critical Mass" game update.

    .. attribute:: description
       :type: str

       An internal description of what situation this armour info entry
       is used for.
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
