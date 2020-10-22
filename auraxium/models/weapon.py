"""Data classes for :mod:`auraxium.ps2.weapon`."""

import dataclasses
from typing import Optional

from ..base import Ps2Data
from ..types import CensusData, LocaleData, optional

__all__ = [
    'WeaponAmmoSlot',
    'WeaponData',
    'WeaponDatasheet'
]


@dataclasses.dataclass(frozen=True)
class WeaponAmmoSlot(Ps2Data):
    """Data class for weapon ammo slot data.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        weapon_id: The ID of the associated :class:`Weapon`.
        weapon_slot_index: The position of the ammo type in the list of
            ammo types.
        clip_size: The clip size for this ammo type.
        capacity: The maximum amount of ammo that can be held with this
            ammo type.
        refill_ammo_rate: The amount of ammo being replenished every
            ammo refill tick.
        refill_ammo_delay_ms: The time between two ammo replenishment
            ticks.

    """

    weapon_id: int
    weapon_slot_index: int
    clip_size: int
    capacity: int
    refill_ammo_rate: Optional[int]
    refill_ammo_delay_ms: Optional[int]

    @classmethod
    def from_census(cls, data: CensusData) -> 'WeaponAmmoSlot':
        return cls(
            int(data.pop('weapon_id')),
            int(data.pop('weapon_slot_index')),
            int(data.pop('clip_size')),
            int(data.pop('capacity')),
            optional(data, 'refill_ammo_rate', int),
            optional(data, 'refill_ammo_delay_ms', int))


@dataclasses.dataclass(frozen=True)
class WeaponData(Ps2Data):
    """Data class for :class:`auraxium.ps2.ability.Weapon`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        weapon_id: The unique ID of this weapon.
        weapon_group_id: Used to group upgradable weapons together and
            track them as a single entity, such as the Infiltrator's
            Recon Dart Device or the Engineer's Repair Tool.
        turn_modifier: Turn speed modifier to apply while the weapon is
            equipped.
        move_modifier: Move speed modifier to apply while the weapon is
            equipped.
        sprint_recovery_ms: Recovery time to allow firing or ADS after
            the player stopped sprinting.
        equip_ms: The weapon equip time in milliseconds.
        unequip_ms: The weapon unequip time in milliseconds.
        to_iron_sights_ms: The ADS enter time in milliseconds.
        from_iron_sights_ms: The ADS exit time in milliseconds.
        heat_capacity: The heat capacity of the weapon. Generally
            identical to :attr:`~auraxium.ps2.FireMode.heat_threshold`,
            but this only uses the first fire mode of the weapon.
        heat_bleed_off_rate: The rate at which the weapon will cool
            down after firing stops.
        heat_overheat_penalty_ms: The overheat penalty imposed if the
            user overheats the weapon.
        melee_detect_width: The hitbox width for melee weapons.
        melee_detect_height: The hitbox height for melee weapons.

    """

    weapon_id: int
    weapon_group_id: Optional[int]
    turn_modifier: float
    move_modifier: float
    sprint_recovery_ms: Optional[int]
    equip_ms: Optional[int]
    unequip_ms: Optional[int]
    to_iron_sights_ms: Optional[int]
    from_iron_sights_ms: Optional[int]
    heat_capacity: Optional[int] = None
    heat_bleed_off_rate: Optional[float] = None
    heat_overheat_penalty_ms: Optional[int] = None
    melee_detect_width: Optional[float] = None
    melee_detect_height: Optional[float] = None

    @classmethod
    def from_census(cls, data: CensusData) -> 'WeaponData':
        return cls(
            int(data.pop('weapon_id')),
            optional(data, 'weapon_group_id', int),
            float(data.pop('turn_modifier')),
            float(data.pop('move_modifier')),
            optional(data, 'sprint_recovery_ms', int),
            optional(data, 'equip_ms', int),
            optional(data, 'unequip_ms', int),
            optional(data, 'to_iron_sights_ms', int),
            optional(data, 'from_iron_sights_ms', int),
            optional(data, 'heat_capacity', int),
            optional(data, 'heat_bleed_off_rate_ms', int),
            optional(data, 'heat_overhead_penalty_ms', int),
            optional(data, 'melee_detect_width', float),
            optional(data, 'melee_detect_height', float))


@dataclasses.dataclass(frozen=True)
class WeaponDatasheet(Ps2Data):
    """Data class for weapon datasheets.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    .. note::
        The data found herein is generally less reliable than the
        sources it was collected from, such as
        :class:`~auraxium.ps2.FireMode` or
        :class:`~auraxium.ps2.Projectile`.

        This data is mostly used for display in the depot and may not
        be inaccurate.

    Attributes:
        item_id: The item the datasheet is for.
        direct_damage: The direct damage amount.
        indirect_damage: The indirect damage amount.
        damage: (Not yet documented)
        damage_min: (Not yet documented)
        damage_max: (Not yet documented)
        fire_cone: (Not yet documented)
        fire_cone_min: (Not yet documented)
        fire_cone_max: (Not yet documented)
        fire_rate_ms: (Not yet documented)
        fire_rate_ms_min: (Not yet documented)
        fire_rate_mx_max: (Not yet documented)
        reload_ms: (Not yet documented)
        reload_ms_min: (Not yet documented)
        reload_ms_max: (Not yet documented)
        clip_size: The clip size for the default ammo type
        capacity: The total ammo capacity for the default ammo type
        range: The localised description of the weapon range (i.e.
            "Medium", "Long", etc.).
        show_clip_size: Whether to display the clip size data to the
            user.
        show_fire_modes: Whether to display the list of fire modes to
            the user.
        show_range: Whether to display the :attr:`range` data to the
            user.

    """

    item_id: int
    direct_damage: Optional[int]
    indirect_damage: Optional[int]
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

    @classmethod
    def from_census(cls, data: CensusData) -> 'WeaponDatasheet':
        return cls(
            int(data.pop('item_id')),
            optional(data, 'direct_damage', int),
            optional(data, 'indirect_damage', int),
            int(data.pop('damage')),
            int(data.pop('damage_min')),
            int(data.pop('damage_max')),
            float(data.pop('fire_cone')),
            float(data.pop('fire_cone_min')),
            float(data.pop('fire_cone_max')),
            int(data.pop('fire_rate_ms')),
            int(data.pop('fire_rate_ms_min')),
            # The "mx" is not a typo - not mine
            int(data.pop('fire_rate_mx_max')),
            int(data.pop('reload_ms')),
            int(data.pop('reload_ms_min')),
            int(data.pop('reload_ms_max')),
            int(data.pop('clip_size')),
            int(data.pop('capacity')),
            LocaleData.from_census(data.pop('range')),
            bool(int(data.pop('show_clip_size'))),
            bool(int(data.pop('show_fire_modes'))),
            bool(int(data.pop('show_range'))))
