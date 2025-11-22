"""Data classes for :mod:`auraxium.ps2._fire`."""

from .base import RESTPayload
from ..types import LocaleData

__all__ = [
    'FireModeData',
    'FireGroupData'
]


class FireModeData(RESTPayload):
    """Data class for :class:`auraxium.ps2.FireMode`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    fire_mode_id: int
    fire_mode_type_id: int | None = None
    ability_id: int | None = None
    ammo_slot: int | None = None
    automatic: bool
    grief_immune: bool | None = None
    iron_sights: bool | None = None
    laser_guided: bool | None = None
    move_modifier: float
    projectile_speed_override: int | None = None
    sprint_fire: bool | None = None
    turn_modifier: float
    use_in_water: bool | None = None
    zoom_default: float
    cof_override: float | None = None
    cof_pellet_spread: float | None = None
    cof_range: float
    cof_recoil: float | None = None
    cof_scalar: float
    cof_scalar_moving: float
    player_state_group_id: int
    damage_direct_effect_id: int | None = None
    damage_head_multiplier: float | None = None
    damage_indirect_effect_id: int | None = None
    damage_legs_multiplier: float | None = None
    fire_ammo_per_shot: int | None = None
    fire_auto_fire_ms: int | None = None
    fire_burst_count: int | None = None
    fire_charge_up_ms: int | None = None
    fire_delay_ms: int | None = None
    fire_detect_range: float | None = None
    fire_duration_ms: int | None = None
    fire_refire_ms: int | None = None
    fire_pellets_per_shot: int | None = None
    heat_per_shot: int | None = None
    heat_recovery_delay_ms: int | None = None
    heat_threshold: int | None = None
    lockon_acquire_close_ms: int | None = None
    lockon_acquire_far_ms: int | None = None
    lockon_acquire_ms: int | None = None
    lockon_angle: float | None = None
    lockon_lose_ms: int | None = None
    lockon_maintain: bool | None = None
    lockon_radius: float | None = None  # Not used as of June 2020
    lockon_range: float | None = None  # Maybe this replaced "lockon_radius"
    lockon_range_close: float | None = None
    lockon_range_far: float | None = None
    lockon_required: bool | None = None
    recoil_angle_max: float | None = None
    recoil_angle_min: float | None = None
    recoil_first_shot_modifier: float | None = None
    recoil_horizontal_max: float | None = None
    recoil_horizontal_max_increase: float | None = None
    recoil_horizontal_min: float | None = None
    recoil_horizontal_min_increase: float | None = None
    recoil_horizontal_tolerance: float | None = None
    recoil_increase: float | None = None
    recoil_increase_crouched: float | None = None
    recoil_magnitude_max: float | None = None
    recoil_magnitude_min: float | None = None
    recoil_max_total_magnitude: float | None = None
    recoil_recovery_acceleration: int | None = None
    recoil_recovery_delay_ms: int | None = None
    recoil_recovery_rate: int | None = None
    recoil_shots_at_min_magnitude: int | None = None
    reload_block_auto: bool | None = None
    reload_continuous: bool | None = None  # Always False or None
    reload_ammo_fill_ms: int | None = None
    reload_chamber_ms: int | None = None
    reload_loop_start_ms: int | None = None
    reload_loop_end_ms: int | None = None
    reload_time_ms: int | None = None
    sway_amplitude_x: float | None = None
    sway_amplitude_y: float | None = None
    sway_can_steady: bool | None = None
    sway_period_x: int | None = None
    sway_period_y: int | None = None
    armor_penetration: float | None = None  # Always zero or None
    max_damage: int | None = None
    max_damage_ind: int | None = None
    max_damage_ind_radius: float | None = None
    max_damage_range: float | None = None
    min_damage: int | None = None
    min_damage_ind: int | None = None
    min_damage_ind_radius: float | None = None
    min_damage_range: float | None = None
    shield_bypass_pct: int | None = None
    description: LocaleData | None = None


class FireGroupData(RESTPayload):
    """Data class for :class:`auraxium.ps2.FireGroup`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    fire_group_id: int
    chamber_duration_ms: int | None = None
    transition_duration_ms: int | None = None
    spool_up_ms: int | None = None
    spool_up_initial_refire_ms: int | None = None
    can_chamber_ironsights: bool | None = None
