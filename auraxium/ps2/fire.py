"""Fire modes and group class definitions."""

import dataclasses
import enum
from typing import Final, Optional

from ..base import Cached, Ps2Data
from ..census import Query
from ..proxy import InstanceProxy, SequenceProxy
from ..types import CensusData
from ..utils import LocaleData, optional

from .projectile import Projectile


class FireModeType(enum.IntEnum):
    """A type of fire mode.

    This is mostly used to group similar fire modes together when
    tabulating multiple weapons.
    """

    PROJECTILE = 0
    IRON_SIGHT = 1
    MELEE = 3
    TRIGGER_ITEM_ABILITY = 8
    THROWN = 12


@dataclasses.dataclass(frozen=True)
class FireModeData(Ps2Data):
    """Data class for :class:`auraxium.ps2.ability.FireMode`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    fire_mode_id: int
    fire_mode_type_id: int
    ability_id: Optional[int]
    ammo_slot: Optional[int]
    automatic: bool
    grief_immune: Optional[bool]
    iron_sights: Optional[bool]
    laser_guided: Optional[bool]
    move_modifier: float
    projectile_speed_override: Optional[int]
    sprint_fire: Optional[bool]
    turn_modifier: float
    use_in_water: Optional[bool]
    zoom_default: float
    cof_override: Optional[float]
    cof_pellet_spread: Optional[float]
    cof_range: float
    cof_recoil: Optional[float]
    cof_scalar: float
    cof_scalar_moving: float
    player_state_group_id: int
    damage_direct_effect_id: Optional[int]
    damage_head_multiplier: Optional[float]
    damage_indirect_effect_id: Optional[int]
    damage_legs_multiplier: Optional[float]
    fire_ammo_per_shot: int
    fire_auto_fire_ms: Optional[int]
    fire_burst_count: int
    fire_charge_up_ms: Optional[int]
    fire_delay_ms: Optional[int]
    fire_detect_range: float
    fire_duration_ms: Optional[int]
    fire_refire_ms: int
    fire_pellets_per_shot: Optional[int]
    heat_per_shot: Optional[int]
    heat_recovery_delay_ms: Optional[int]
    heat_threshold: Optional[int]
    lockon_acquire_close_ms: Optional[int]
    lockon_acquire_far_ms: Optional[int]
    lockon_acquire_ms: Optional[int]
    lockon_angle: Optional[float]
    lockon_lose_ms: Optional[int]
    lockon_maintain: Optional[bool]
    lockon_radius: Optional[int]  # Not used as of June 2020
    lockon_range: Optional[int]  # Maybe this replaced "lockon_radius"?
    lockon_range_close: Optional[int]
    lockon_range_far: Optional[int]
    lockon_required: Optional[bool]
    recoil_angle_max: Optional[int]
    recoil_angle_min: Optional[int]
    recoil_first_shot_modifier: float
    recoil_horizontal_max: Optional[float]
    recoil_horizontal_max_increase: Optional[float]
    recoil_horizontal_min: Optional[float]
    recoil_horizontal_min_increase: Optional[float]
    recoil_horizontal_tolerance: Optional[float]
    recoil_increase: Optional[float]
    recoil_increase_crouched: Optional[float]
    recoil_magnitude_max: Optional[float]
    recoil_magnitude_min: Optional[float]
    recoil_max_total_magnitude: Optional[float]
    recoil_recovery_acceleration: Optional[int]
    recoil_recovery_delay_ms: Optional[int]
    recoil_recovery_rate: Optional[int]
    recoil_shots_at_min_magnitude: Optional[bool]
    reload_block_auto: Optional[bool]
    reload_continuous: Optional[bool]  # Always False or None
    reload_ammo_fill_ms: Optional[int]
    reload_chamber_ms: Optional[int]
    reload_loop_start_ms: Optional[int]
    reload_loop_end_ms: Optional[int]
    reload_time_ms: int
    sway_amplitude_x: Optional[float]
    sway_amplitude_y: Optional[float]
    sway_can_steady: Optional[bool]
    sway_period_x: Optional[int]
    sway_period_y: Optional[int]
    armor_penetration: Optional[float]  # Always zero or None
    max_damage: Optional[int]
    max_damage_ind: Optional[int]
    max_damage_ind_radius: Optional[float]
    max_damage_range: Optional[float]
    min_damage: Optional[int]
    min_damage_ind: Optional[int]
    min_damage_ind_radius: Optional[float]
    min_damage_range: Optional[float]
    shield_bypass_pct: Optional[int]
    description: Optional[LocaleData]

    @classmethod
    def from_census(cls, data: CensusData) -> 'FireModeData':
        description = data['description']
        if description['en'] != 'NULL':
            description = LocaleData.from_census(description)
        else:
            description = None
        return cls(
            int(data['fire_mode_id']),
            int(data['fire_mode_type_id']),
            optional(data, 'ability_id', int),
            optional(data, 'ammo_slot', int),
            bool(int(data['automatic'])),
            optional(data, 'grief_immune', bool),
            optional(data, 'iron_sights', bool),
            optional(data, 'laser_guided', bool),
            float(data['move_modifier']),
            optional(data, 'projectile_speed_override', int),
            optional(data, 'sprint_fire', bool),
            float(data['turn_modifier']),
            optional(data, 'use_in_water', bool),
            float(data['zoom_default']),
            optional(data, 'cof_override', float),
            optional(data, 'cof_pellet_spread', float),
            float(data['cof_range']),
            optional(data, 'cof_recoil', float),
            float(data['cof_scalar']),
            float(data['cof_scalar_moving']),
            int(data['player_state_group_id']),
            optional(data, 'damage_direct_effect_id', int),
            optional(data, 'damage_head_multiplier', float),
            optional(data, 'damage_indirect_effect_id', int),
            optional(data, 'damage_legs_multiplier', float),
            int(data['fire_ammo_per_shot']),
            optional(data, 'fire_auto_fire_ms', int),
            int(data['fire_burst_count']),
            optional(data, 'fire_charge_up_ms', int),
            optional(data, 'fire_delay_ms', int),
            float(data['fire_detect_range']),
            optional(data, 'fire_duration_ms', int),
            int(data['fire_refire_ms']),
            optional(data, 'fire_pellets_per_shot', int),
            optional(data, 'heat_per_shot', int),
            optional(data, 'heat_recovery_delay_ms', int),
            optional(data, 'heat_threshold', int),
            optional(data, 'lockon_acquire_close_ms', int),
            optional(data, 'lockon_acquire_far_ms', int),
            optional(data, 'lockon_acquire_ms', int),
            optional(data, 'lockon_angle', float),
            optional(data, 'lockon_lose_ms', int),
            optional(data, 'lockon_maintain', bool),
            optional(data, 'lockon_radius', int),
            optional(data, 'lockon_range', int),
            optional(data, 'lockon_range_close', int),
            optional(data, 'lockon_range_far', int),
            optional(data, 'lockon_required', bool),
            optional(data, 'recoil_angle_max', int),
            optional(data, 'recoil_angle_min', int),
            float(data['recoil_first_shot_modifier']),
            optional(data, 'recoil_horizontal_max', float),
            optional(data, 'recoil_horizontal_max_increase', float),
            optional(data, 'recoil_horizontal_min', float),
            optional(data, 'recoil_horizontal_min_increase', float),
            optional(data, 'recoil_horizontal_tolerance', float),
            optional(data, 'recoil_increase', float),
            optional(data, 'recoil_increase_crouched', float),
            optional(data, 'recoil_magnitude_max', float),
            optional(data, 'recoil_magnitude_min', float),
            optional(data, 'recoil_max_total_magnitude', float),
            optional(data, 'recoil_recovery_acceleration', int),
            optional(data, 'recoil_recovery_delay_ms', int),
            optional(data, 'recoil_recovery_rate', int),
            optional(data, 'recoil_shots_at_min_magnitude', bool),
            optional(data, 'reload_block_auto', bool),
            optional(data, 'reload_continuous', bool),
            optional(data, 'reload_ammo_fill_ms', int),
            optional(data, 'reload_chamber_ms', int),
            optional(data, 'reload_loop_start_ms', int),
            optional(data, 'reload_loop_end_ms', int),
            int(data['reload_time_ms']),
            optional(data, 'sway_amplitude_x', float),
            optional(data, 'sway_amplitude_y', float),
            optional(data, 'sway_can_steady', bool),
            optional(data, 'sway_period_x', int),
            optional(data, 'sway_period_y', int),
            optional(data, 'armor_penetration', float),
            optional(data, 'max_damage', int),
            optional(data, 'max_damage_ind', int),
            optional(data, 'max_damage_ind_radius', float),
            optional(data, 'max_damage_range', float),
            optional(data, 'min_damage', int),
            optional(data, 'min_damage_ind', int),
            optional(data, 'min_damage_ind_radius', float),
            optional(data, 'min_damage_range', float),
            optional(data, 'shield_bypass_pct', int),
            description)


class FireMode(Cached, cache_size=10, cache_ttu=3600.0):
    """A fire mode of a weapon.

    This class defines the bulk of a weapon's stats, such as reload
    times or accuracy.

    Note that this is not synonymous with in-game fire modes, these are
    handled by the :class:`FireGroup` class instead. Fire groups are
    also used to implement the auxiliary under-barrel fire modes.

    Implementation detail: This class wraps the ``fire_mode_2``
    collection, the regular ``fire_mode`` collection does not have a
    representation in the object model.
    """

    collection = 'fire_mode_2'
    data: FireModeData
    id_field = 'fire_mode_id'

    @property
    def type(self) -> FireModeType:
        """Return the type of fire mode as an enum."""
        return FireModeType(self.data.fire_mode_type_id)

    def _build_dataclass(self, data: CensusData) -> FireModeData:
        return FireModeData.from_census(data)

    def projectile(self) -> InstanceProxy[Projectile]:
        """Return the projectile associated with this fire mode."""
        collection: Final[str] = 'fire_mode_to_projectile'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        join = query.create_join(Projectile.collection)
        join.parent_field = join.child_field = Projectile.id_field
        return InstanceProxy(Projectile, query, client=self._client)


@dataclasses.dataclass(frozen=True)
class FireGroupData(Ps2Data):
    """Data class for :class:`auraxium.ps2.ability.FireGroup`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    fire_group_id: int
    chamber_duration_ms: Optional[int]
    transition_duration_ms: Optional[int]
    spool_up_ms: Optional[int]
    spool_up_initial_refire_ms: Optional[int]
    can_chamber_ironsights: Optional[bool]

    @classmethod
    def from_census(cls, data: CensusData) -> 'FireGroupData':
        return cls(
            int(data['fire_group_id']),
            optional(data, 'chamber_duration_ms', int),
            optional(data, 'transition_duration_ms', int),
            optional(data, 'spool_up_ms', int),
            optional(data, 'spool_up_initial_refire_ms', int),
            optional(data, 'can_chamber_ironsights', bool))


class FireGroup(Cached, cache_size=10, cache_ttu=60.0):
    """Links multiple fire modes into a group.

    Fire groups are comparable to the in-game fire modes, such as
    burst, semi auto or fully automatic. They are also used to
    implement auxiliary fire modes such as under-barrel launchers.
    """

    collection = 'fire_group'
    data: FireGroupData
    id_field = 'fire_group_id'

    def _build_dataclass(self, data: CensusData) -> FireGroupData:
        return FireGroupData.from_census(data)

    def fire_modes(self) -> SequenceProxy[FireMode]:
        """Return the fire modes in the fire group."""
        collection: Final[str] = 'fire_group_to_fire_mode'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        query.limit(20)
        join = query.create_join(FireMode.collection)
        join.parent_field = join.child_field = FireMode.id_field
        return SequenceProxy(FireMode, query, client=self._client)
