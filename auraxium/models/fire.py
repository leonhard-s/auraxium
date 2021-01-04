"""Data classes for :mod:`auraxium.ps2.fire`."""

from typing import Optional

from ..base import Ps2Data
from ..types import LocaleData

__all__ = [
    'FireModeData',
    'FireGroupData'
]

# pylint: disable=too-few-public-methods


class FireModeData(Ps2Data):
    """Data class for :class:`auraxium.ps2.ability.FireMode`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        fire_mode_id: The unique ID of this fire mode.
        fire_mode_type_id: The type of fire mode as a value of the
            :class:`FireModeType` enumerator.
        ability_id: (Not yet documented)
        ammo_slot: The ammo slot used by this fire mode.
        automatic: Whether the fire mode is automatic or not.
        grief_immune: Whether this fire mode is excluded from friendly
            fire.
        iron_sights: Whether this weapon comes with iron sights.
        laser_guided: Whether this weapon is laser guided.
        move_modifier: (Not yet documented)
        projectile_speed_override: A fire mode specific override used
            to override the fire mode's projectile's speed.
        sprint_fire: Whether the fire mode allows firing and sprinting.
        turn_modifier: (Not yet documented)
        use_in_water: Unused.
        zoom_default: The iron-sight zoom level of the fire mode.
        cof_override: (Not yet documented)
        cof_pellet_spread: The pellet spread used for multi-projectile
            weapons (such as non-slug shotguns or the NSX Tengu).
        cof_range: The distance the projectile may travel before
            being destroyed.
        cof_recoil: The cone-of-fire bloom per shot.
        cof_scalar: The starting cone-of-fire scalar. This exists so it
            can be modified by attachments.
        cof_scalar_moving: The starting cone-of-fire scalar
            while moving. This exists so it can be modified by
            attachments.
        player_state_group_id: The state group associated with this
            fire mode. State groups contain the state-dependent values
            for a weapon, such as accuracy changes from sprinting,
            crouching, etc.
        damage_direct_effect_id: The damage effect used on direct hits.
        damage_head_multiplier: The headshot multiplier for the fire
            mode.
        damage_indirect_effect_id: The splash damage effect used on
            indirect hits.
        damage_legs_multiplier: The leg shot multiplier for the fire
            mode.
        fire_ammo_per_shot: The amount of ammo consumed per shot. Some
            weapons, like the VS Lancer, may consume more than 1 bullet
            per shot.
        fire_auto_fire_ms: The time in-between shots during automatic
            fire.
        fire_burst_count: The burst size of the fire mode.
        fire_charge_up_ms: The time it takes the weapon to charge up,
            used in the VS Lancer rocket launcher.
        fire_delay_ms: The delay between pulling the trigger and
            the weapon actually firing, used in the NXS Yumi.
        fire_detect_range: (Not yet documented)
        fire_duration_ms: The firing duration of a weapon. Used for
            grenade throwing and knifing animations.
        fire_refire_ms: The re-fire delay used for semi-automatic
            weapons.
        fire_pellets_per_shot: The number of pellets fired by non-slug
            shotguns or the NSX Tengu.
        heat_per_shot: The weapon heat applied per shot.
        heat_recovery_delay_ms: The duration after which weapon heat
            will start to dissipate.
        heat_threshold: The overheating threshold of the weapon. This
            is comparable to the magazine size for heat-based weapons,
            with the number of shots available without overheating
            being equal to the floor of
            :attr:`heat_threshold` divided :attr:`heat_per_shot`.
        lockon_acquire_close_ms: The minimum distance from the target
            to establish a lock-on.
        lockon_acquire_far_ms: The maximum distance from the target to
            establish a lock-on.
        lockon_acquire_ms: The lock-on time.
        lockon_angle: The maximum error allowed while locking on, you
            can think of this like a cone of fire.
        lockon_lose_ms: (Not yet documented)
        lockon_maintain: (Not yet documented)
        lockon_radius: Not used as of June 2020, use
            :attr:`lockon_range` instead.
        lockon_range: The maximum lock-on range.
        lockon_range_close: (Not yet documented)
        lockon_range_far: (Not yet documented)
        lockon_required: Whether this weapon can be fired without
            being locked on (True for the NS Annihilator, False for
            faction-specific lock-on launchers).
        recoil_angle_max: The maximum recoil angle, used to randomise
            recoil angle.
        recoil_angle_min: The minimum recoil angle, used to randomise
            recoil angle.
        recoil_first_shot_modifier: The first shot multiplier for the
            weapon.
        recoil_horizontal_max: The maximum horizontal recoil per shot.
        recoil_horizontal_max_increase: The maximum horizontal recoil
            jump per shot.
        recoil_horizontal_min: The minimum horizontal recoil per shot.
        recoil_horizontal_min_increase: The minimum horizontal recoil
            jump per shot.
        recoil_horizontal_tolerance: (Not yet documented)
        recoil_increase: The base vertical recoil while standing.
        recoil_increase_crouched: The base vertical recoil while
            crouching.
        recoil_magnitude_max: The maximum vertical recoil per shot.
        recoil_magnitude_min: The minimum vertical recoil per shot.
        recoil_max_total_magnitude: The total maximum recoil, including
            both horizontal and vertical offsets.
        recoil_recovery_acceleration: (Not yet documented)
        recoil_recovery_delay_ms: The delay before the weapon will
            reset after the player stopped firing.
        recoil_recovery_rate: The speed at which the weapon will reset
            after the players topped firing.
        recoil_shots_at_min_magnitude: (Not yet documented)
        reload_block_auto: (Not yet documented)
        reload_continuous: (Unused, always False or not set.)
        reload_ammo_fill_ms: The time between ammo refill ticks.
        reload_chamber_ms: The chamber time for bolt-action weapons.
        reload_loop_start_ms: The initial loop time for reloading with
            looped reload weapons (such as pump action shotguns).
        reload_loop_end_ms: The final delay after reloading a looped
            reload weapon is completed.
        reload_time_ms: The reload time of the weapon.
        sway_amplitude_x: Sway amplitude in X direction.
        sway_amplitude_y: Sway amplitude in Y direction.
        sway_can_steady: Whether the player can hold their breath to
            stop camera sway.
        sway_period_x: Sway period in X direction.
        sway_period_y: Sway period in Y direction.
        armor_penetration: (Unused as of June 2020)
        max_damage: Maximum direct damage of the weapon.
        max_damage_ind: Maximum indirect damage of the weapon.
        max_damage_ind_radius: The radius over which maximum indirect
            damage of the weapon will fall off.
        max_damage_range: The range up to which the weapon will deal
            its maximum damage.
        min_damage: The minimum direct damage of the weapon.
        min_damage_ind: The minimum indirect damage of the weapon.
        min_damage_ind_radius: The radius over which the minimum
            indirect damage of the weapon will fall off.
        min_damage_range: The range at which the weapon deals its
            minimum damage.
        shield_bypass_pct: The percentage of damage that will bypass
            shields and always affect the raw health pool.
        description: Localised description of the fire mode (e.g.
            "Automatic").

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


class FireGroupData(Ps2Data):
    """Data class for :class:`auraxium.ps2.ability.FireGroup`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        fire_group_id: The unique ID of this fire group.
        chamber_duration_ms: The rechamber time for weapons in this
            group.
        transition_duration_ms: (Not yet documented)
        spool_up_ms: The duration of the spool-up period for this
            weapon group.
        spool_up_initial_refire_ms: The initial fire speed (rounds
            per minute) of the weapon group. The weapon starts out at
            this value when firing, then tapers to the regular value
            after :attr:`spool_up_ms` milliseconds.
        can_chamber_ironsights: Whether a bolt-action weapon can be
            rechambered while in ADS.

    """

    fire_group_id: int
    chamber_duration_ms: Optional[int] = None
    transition_duration_ms: Optional[int] = None
    spool_up_ms: Optional[int] = None
    spool_up_initial_refire_ms: Optional[int] = None
    can_chamber_ironsights: Optional[bool] = None
