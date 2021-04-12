"""Data classes for :mod:`auraxium.ps2._weapon`."""

from typing import Optional

from .base import RESTPayload
from ..types import LocaleData

__all__ = [
    'WeaponAmmoSlot',
    'WeaponData',
    'WeaponDatasheet'
]

# pylint: disable=too-few-public-methods


class WeaponAmmoSlot(RESTPayload):
    """Data class for weapon ammo slot data.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    .. attribute:: weapon_id
       :type: int

       The ID of the associated :class:`~auraxium.ps2.Weapon`.

    .. attribute:: weapon_slot_index
       :type: int

       The position of the ammo type in the list of ammo types.

    .. attribute:: clip_size
       :type: int

       The number of bullets in a clip for this ammo slot.

    .. attribute:: capacity
       :type: int

       The maximum amount of ammo that can be held with this ammo type.

    .. attribute:: refill_ammo_rate
       :type: int

       The amount of ammo being replenished every ammo refill tick.

    .. attribute:: refill_ammo_delay_ms
       :type: int

       The time between two ammo replenishment ticks.
    """

    weapon_id: int
    weapon_slot_index: int
    clip_size: int
    capacity: int
    refill_ammo_rate: Optional[int] = None
    refill_ammo_delay_ms: Optional[int] = None


class WeaponData(RESTPayload):
    """Data class for :class:`auraxium.ps2.Weapon`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    weapon_id: int
    weapon_group_id: Optional[int] = None
    turn_modifier: float
    move_modifier: float
    sprint_recovery_ms: Optional[int] = None
    equip_ms: Optional[int]
    unequip_ms: Optional[int] = None
    to_iron_sights_ms: Optional[int] = None
    from_iron_sights_ms: Optional[int] = None
    heat_capacity: Optional[int] = None
    heat_bleed_off_rate: Optional[float] = None
    heat_overheat_penalty_ms: Optional[int] = None
    melee_detect_width: Optional[float] = None
    melee_detect_height: Optional[float] = None


class WeaponDatasheet(RESTPayload):
    """Data class for weapon datasheets.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    .. note::

       The data found herein is generally less reliable than the
       sources it was collected from, such as
       :class:`~auraxium.ps2.FireMode` or
       :class:`~auraxium.ps2.Projectile`.

       This data is mostly used for display in the depot and is often
       not inaccurate.

    .. attribute:: item_id
       :type: int

       The item the datasheet is for.

    .. attribute:: direct_damage
       :type: int | None

       Direct hit damage.

    .. attribute:: indirect_damage
       :type: int | None

       The maximum indirect hit (i.e. splash) damage.

    .. attribute:: damage
       :type: int

       (Not yet documented)

    .. attribute: damage_min
       :type: int

       (Not yet documented)

    .. attribute:: damage_max
       :type: int

       (Not yet documented)

    .. attribute:: fire_cone
       :type: float

       (Not yet documented)

    .. attribute:: fire_cone_min
       :type: float

       (Not yet documented)

    .. attribute:: fire_cone_max:´
       :type: float

       (Not yet documented)

    .. attribute:: fire_rate_ms
       :type: int

       (Not yet documented)

    .. attribute:: fire_rate_ms_min
       :type: int

       (Not yet documented)

    .. attribute:: fire_rate_mx_max
       :type: int

       (Not yet documented)

    .. attribute:: reload_ms
       :type: int

       (Not yet documented)

    .. attribute:: reload_ms_min
       :type: int

       (Not yet documented)

    .. attribute:: reload_ms_max
       :type: int

       (Not yet documented)

    .. attribute:: clip_size
       :type: int

       The clip size for the default ammo type.

    .. attribute:: capacity
       :type: int

       The total ammo capacity for the default ammo type.

    .. attribute:: range
       :type: auraxium.types.LocaleData

       The localised description of the weapon range (i.e. "Medium",
       "Long", etc.).

    .. attribute:: show_clip_size
       :type: bool

       Whether to display the clip size data to the user.

    .. attribute:: show_fire_modes
       :type: bool

       Whether to display the list of fire modes to the user.

    .. attribute:: show_range
       :type: bool

       Whether to display the :attr:`range` data to the user.
    """

    item_id: int
    direct_damage: Optional[int] = None
    indirect_damage: Optional[int] = None
    damage: int
    damage_min: int
    damage_max: int
    fire_cone: float
    fire_cone_min: float
    fire_cone_max: float
    fire_rate_ms: int
    fire_rate_ms_min: int
    fire_rate_mx_max: int
    reload_ms: int
    reload_ms_min: int
    reload_ms_max: int
    clip_size: int
    capacity: int
    range: LocaleData
    show_clip_size: bool
    show_fire_modes: bool
    show_range: bool
