"""Data classes for :mod:`auraxium.ps2.fire`."""

from typing import Optional

from .base import RESTPayload
from ..types import LocaleData

__all__ = [
    'FireModeData',
    'FireGroupData'
]

# pylint: disable=too-few-public-methods


class FireModeData(RESTPayload):
    """Data class for :class:`auraxium.ps2.ability.FireMode`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    fire_mode_id: int
    fire_mode_type_id: int
    ability_id: Optional[int] = None
    ammo_slot: Optional[int] = None
    automatic: bool
    grief_immune: Optional[bool] = None
    iron_sights: Optional[bool] = None
    laser_guided: Optional[bool] = None
    move_modifier: float
    projectile_speed_override: Optional[int] = None
    sprint_fire: Optional[bool] = None
    turn_modifier: float
    use_in_water: Optional[bool] = None
    zoom_default: float
    cof_override: Optional[float] = None
    cof_pellet_spread: Optional[float] = None
    cof_range: float
    cof_recoil: Optional[float] = None
    cof_scalar: float
    cof_scalar_moving: float
    player_state_group_id: int
    damage_direct_effect_id: Optional[int] = None
    damage_head_multiplier: Optional[float] = None
    damage_indirect_effect_id: Optional[int] = None
    damage_legs_multiplier: Optional[float] = None
    fire_ammo_per_shot: int
    fire_auto_fire_ms: Optional[int] = None
    fire_burst_count: int
    fire_charge_up_ms: Optional[int] = None
    fire_delay_ms: Optional[int] = None
    fire_detect_range: float
    fire_duration_ms: Optional[int] = None
    fire_refire_ms: int
    fire_pellets_per_shot: Optional[int] = None
    heat_per_shot: Optional[int] = None
    heat_recovery_delay_ms: Optional[int] = None
    heat_threshold: Optional[int] = None
    lockon_acquire_close_ms: Optional[int] = None
    lockon_acquire_far_ms: Optional[int] = None
    lockon_acquire_ms: Optional[int] = None
    lockon_angle: Optional[float] = None
    lockon_lose_ms: Optional[int] = None
    lockon_maintain: Optional[bool] = None
    lockon_radius: Optional[float] = None  # Not used as of June 2020
    lockon_range: Optional[float] = None  # Maybe this replaced "lockon_radius"
    lockon_range_close: Optional[float] = None
    lockon_range_far: Optional[float] = None
    lockon_required: Optional[bool] = None
    recoil_angle_max: Optional[float] = None
    recoil_angle_min: Optional[float] = None
    recoil_first_shot_modifier: float
    recoil_horizontal_max: Optional[float] = None
    recoil_horizontal_max_increase: Optional[float] = None
    recoil_horizontal_min: Optional[float] = None
    recoil_horizontal_min_increase: Optional[float] = None
    recoil_horizontal_tolerance: Optional[float] = None
    recoil_increase: Optional[float] = None
    recoil_increase_crouched: Optional[float] = None
    recoil_magnitude_max: Optional[float] = None
    recoil_magnitude_min: Optional[float] = None
    recoil_max_total_magnitude: Optional[float] = None
    recoil_recovery_acceleration: Optional[int] = None
    recoil_recovery_delay_ms: Optional[int] = None
    recoil_recovery_rate: Optional[int] = None
    recoil_shots_at_min_magnitude: Optional[bool] = None
    reload_block_auto: Optional[bool] = None
    reload_continuous: Optional[bool] = None  # Always False or None
    reload_ammo_fill_ms: Optional[int] = None
    reload_chamber_ms: Optional[int] = None
    reload_loop_start_ms: Optional[int] = None
    reload_loop_end_ms: Optional[int] = None
    reload_time_ms: int
    sway_amplitude_x: Optional[float] = None
    sway_amplitude_y: Optional[float] = None
    sway_can_steady: Optional[bool] = None
    sway_period_x: Optional[int] = None
    sway_period_y: Optional[int] = None
    armor_penetration: Optional[float] = None  # Always zero or None
    max_damage: Optional[int] = None
    max_damage_ind: Optional[int] = None
    max_damage_ind_radius: Optional[float] = None
    max_damage_range: Optional[float] = None
    min_damage: Optional[int] = None
    min_damage_ind: Optional[int] = None
    min_damage_ind_radius: Optional[float] = None
    min_damage_range: Optional[float] = None
    shield_bypass_pct: Optional[int] = None
    description: LocaleData


class FireGroupData(RESTPayload):
    """Data class for :class:`auraxium.ps2.ability.FireGroup`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    fire_group_id: int
    chamber_duration_ms: Optional[int] = None
    transition_duration_ms: Optional[int] = None
    spool_up_ms: Optional[int] = None
    spool_up_initial_refire_ms: Optional[int] = None
    can_chamber_ironsights: Optional[bool] = None
