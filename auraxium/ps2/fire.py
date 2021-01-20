"""Fire modes and group class definitions."""

import enum
from typing import Dict, Final, Optional

from ..base import Cached
from ..census import Query
from ..models import FireGroupData, FireModeData
from ..proxy import InstanceProxy, SequenceProxy
from ..request import extract_payload
from ..types import LocaleData

from .projectile import Projectile
from .states import PlayerState, PlayerStateGroup


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
    dataclass = FireModeData
    id_field = 'fire_mode_id'

    # Type hints for data class fallback attributes
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
    lockon_range: Optional[float]
    lockon_range_close: Optional[float]
    lockon_range_far: Optional[float]
    lockon_required: Optional[bool]
    recoil_angle_max: Optional[float]
    recoil_angle_min: Optional[float]
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
    reload_continuous: Optional[bool]
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
    armor_penetration: Optional[float]
    max_damage: Optional[int]
    max_damage_ind: Optional[int]
    max_damage_ind_radius: Optional[float]
    max_damage_range: Optional[float]
    min_damage: Optional[int]
    min_damage_ind: Optional[int]
    min_damage_ind_radius: Optional[float]
    min_damage_range: Optional[float]
    shield_bypass_pct: Optional[int]
    description: LocaleData

    @property
    def type(self) -> FireModeType:
        """Return the type of fire mode as an enum."""
        return FireModeType(self.data.fire_mode_type_id)

    async def state_groups(self) -> Dict[PlayerState, PlayerStateGroup]:
        """Return the state-specific data for a fire mode."""
        collection: Final[str] = 'player_state_group_2'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field='player_state_group_id',
                       value=self.data.player_state_group_id)
        query.limit(10)
        payload = await self._client.request(query)
        data = extract_payload(payload, collection)
        states: Dict[PlayerState, PlayerStateGroup] = {}
        for group_data in data:
            group = PlayerStateGroup(**group_data)
            state = PlayerState(group.player_state_id)
            states[state] = group
        return states

    def projectile(self) -> InstanceProxy[Projectile]:
        """Return the projectile associated with this fire mode."""
        collection: Final[str] = 'fire_mode_to_projectile'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        join = query.create_join(Projectile.collection)
        join.set_fields(Projectile.id_field)
        return InstanceProxy(Projectile, query, client=self._client)


class FireGroup(Cached, cache_size=10, cache_ttu=60.0):
    """Links multiple fire modes into a group.

    Fire groups are comparable to the in-game fire modes, such as
    burst, semi auto or fully automatic. They are also used to
    implement auxiliary fire modes such as under-barrel launchers.
    """

    collection = 'fire_group'
    data: FireGroupData
    dataclass = FireGroupData
    id_field = 'fire_group_id'

    # Type hints for data class fallback attributes
    fire_group_id: int
    chamber_duration_ms: Optional[int]
    transition_duration_ms: Optional[int]
    spool_up_ms: Optional[int]
    spool_up_initial_refire_ms: Optional[int]
    can_chamber_ironsights: Optional[bool]

    def fire_modes(self) -> SequenceProxy[FireMode]:
        """Return the fire modes in the fire group."""
        collection: Final[str] = 'fire_group_to_fire_mode'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        query.limit(20)
        join = query.create_join(FireMode.collection)
        join.set_fields(FireMode.id_field)
        return SequenceProxy(FireMode, query, client=self._client)
