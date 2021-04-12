"""Fire modes and group class definitions."""

import enum
from typing import Dict, Final, Optional

from ..base import Cached
from ..census import Query
from ..models import FireGroupData, FireModeData
from .._proxy import InstanceProxy, SequenceProxy
from .._rest import extract_payload
from ..types import LocaleData

from ._projectile import Projectile
from ._states import PlayerState, PlayerStateGroup

__all__ = [
    'FireGroup',
    'FireMode',
    'FireModeType'
]


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

    .. attribute:: id
       :type: int

       The unique ID of this fire mode.

    .. attribute:: fire_mode_type_id
       :type: int

       The type of fire mode as a value of the
       :class:`~auraxium.ps2.FireModeType` enumerator.

    .. attribute:: ability_id
       :type: int | None

       (Not yet documented)

    .. attribute:: ammo_slot
       :type: int | None

       The ammo slot used by this fire mode.

    .. attribute:: automatic
       :type: bool

       Whether the fire mode is automatic or not.

    .. attribute:: grief_immune
       :type: bool | None

       Whether this fire mode is excluded from friendly fire.

    .. attribute:: iron_sights
       :type: bool | None

       Whether this weapon comes with iron sights.

    .. attribute:: laser_guided
       :type: bool | None

       Whether this weapon is laser guided.

    .. attribute:: move_modifier
       :type: float

       (Not yet documented)

    .. attribute:: projectile_speed_override
       :type: int | None

       A fire mode specific override used
            to override the fire mode's projectile's speed.

    .. attribute:: sprint_fire
       :type: bool | None

       Whether the fire mode allows firing and sprinting.

    .. attribute:: turn_modifier
       :type: float

       (Not yet documented)

    .. attribute:: use_in_water
       :type: bool | None

       Unused.

    .. attribute:: zoom_default
       :type: float

       The iron-sight zoom level of the fire mode.

    .. attribute:: cof_override
       :type: float | None

       (Not yet documented)

    .. attribute:: cof_pellet_spread
       :type: float | None

       The pellet spread used for multi-projectile weapons (such as
       non-slug shotguns or the NSX Tengu).

    .. attribute:: cof_range
       :type: float

       (Not yet documented)

    .. attribute:: cof_recoil
       :type: float | None

       (Not yet documented)

    .. attribute:: cof_scalar
       :type: float

       The starting cone-of-fire scalar. This exists so it
            can be modified by attachments.

    .. attribute:: cof_scalar_moving
       :type: float

       The starting cone-of-fire scalar while moving. This exists so it
       can be modified by attachments.

    .. attribute:: player_state_group_id
       :type: int

       The state group associated with this fire mode. State groups
       contain the state-dependent values for a weapon, such as
       accuracy changes from sprinting, crouching, etc.

    .. attribute:: damage_direct_effect_id
       :type: int | None

       The damage effect used on direct hits.

    .. attribute:: damage_head_multiplier
       :type: float | None

       The headshot multiplier for the fire
            mode.

    .. attribute:: damage_indirect_effect_id
       :type: int | None

       The splash damage effect used on indirect hits.

    .. attribute:: damage_legs_multiplier
       :type: float | None

       The leg shot multiplier for the fire mode.

    .. attribute:: fire_ammo_per_shot
       :type: int

       The amount of ammo consumed per shot. Some weapons, like the VS
       Lancer, may consume more than 1 bullet per shot.

    .. attribute:: fire_auto_fire_ms
       :type: int | None

       The time in-between shots during automatic fire.

    .. attribute:: fire_burst_count
       :type: int

       The burst size of the fire mode.

    .. attribute:: fire_charge_up_ms
       :type: int | None

       The time it takes the weapon to charge up, used in the VS Lancer
       rocket launcher.

    .. attribute:: fire_delay_ms
       :type: int | None

       The delay between pulling the trigger and the weapon actually
       firing, used in the NXS Yumi.

    .. attribute:: fire_detect_range
       :type: float

       (Not yet documented)

    .. attribute:: fire_duration_ms
       :type: int | None

       The firing duration of a weapon. Used for grenade throwing and
       knifing animations.

    .. attribute:: fire_refire_ms
       :type: int

       The re-fire delay used for semi-automatic weapons.

    .. attribute:: fire_pellets_per_shot
       :type: int | None

       The number of pellets fired by non-slug shotguns or the NSX
       Tengu.

    .. attribute:: heat_per_shot
       :type: int | None

       The weapon heat applied per shot.

    .. attribute:: heat_recovery_delay_ms
       :type: int | None

       The duration after which weapon heat
            will start to dissipate.

    .. attribute:: heat_threshold
       :type: int | None

       The overheating threshold of the weapon. This is comparable to
       the magazine size for heat-based weapons, with the number of
       shots available without overheating being equal to the floor of
       :attr:`heat_threshold` divided :attr:`heat_per_shot`.

    .. attribute:: lockon_acquire_close_ms
       :type: int | None

       The time to establish a lock at the launcher's minimum lock-on
       distance.

    .. attribute:: lockon_acquire_far_ms
       :type: int | None

       The time to establish a lock at the launcher's maximum lock-on
       distance.

    .. attribute:: lockon_acquire_ms
       :type: int | None

       The base lock-on time.

    .. attribute:: lockon_angle
       :type: float | None

       The maximum error allowed while locking on, you can think of
       this like a cone of fire.

    .. attribute:: lockon_lose_ms
       :type: int | None

       (Not yet documented)

    .. attribute:: lockon_maintain
       :type: bool | None

       (Not yet documented)

    .. attribute:: lockon_radius
       :type: float | None

       Not used as of June 2020, use :attr:`lockon_range` instead.

    .. attribute:: lockon_range
       :type: float | None

       The maximum lock-on range.

    .. attribute:: lockon_range_close
       :type: float | None

       (Not yet documented)

    .. attribute:: lockon_range_far
       :type: float | None

       (Not yet documented)

    .. attribute:: lockon_required
       :type: bool | None

       Whether this weapon can be fired without being locked on (true
       for the NS Annihilator, false for faction-specific lock-on
       launchers).

    .. attribute:: recoil_angle_max
       :type: float | None

       The maximum recoil angle, used to randomise recoil angle.

    .. attribute:: recoil_angle_min
       :type: float | None

       The minimum recoil angle, used to randomise recoil angle.

    .. attribute:: recoil_first_shot_modifier
       :type: float

       Extra recoil to apply only to the first shot of the weapon.

    .. attribute:: recoil_horizontal_max
       :type: float | None

       The maximum horizontal recoil per shot.

    .. attribute:: recoil_horizontal_max_increase
       :type: float | None

       The maximum horizontal recoil jump per shot.

    .. attribute:: recoil_horizontal_min
       :type: float | None

       The minimum horizontal recoil per shot.

    .. attribute:: recoil_horizontal_min_increase
       :type: float | None

       The minimum horizontal recoil jump per shot.

    .. attribute:: recoil_horizontal_tolerance
       :type: float | None

       (Not yet documented)

    .. attribute:: recoil_increase
       :type: float | None

       The base vertical recoil while standing.

    .. attribute:: recoil_increase_crouched
       :type: float | None

       The base vertical recoil while crouching.

    .. attribute:: recoil_magnitude_max
       :type: float | None

       The maximum vertical recoil per shot.

    .. attribute:: recoil_magnitude_min
       :type: float | None

       The minimum vertical recoil per shot.

    .. attribute:: recoil_max_total_magnitude
       :type: float | None

       The total maximum recoil, including both horizontal and vertical
       offsets.

    .. attribute:: recoil_recovery_acceleration
       :type: int | None

       (Not yet documented)

    .. attribute:: recoil_recovery_delay_ms
       :type: int | None

       The delay in milliseconds before the weapon will reset after the
       player stopped firing.

    .. attribute:: recoil_recovery_rate
       :type: int | None

       The speed at which the weapon will reset to its original cone of
       fire after the player stopped firing.

    .. attribute:: recoil_shots_at_min_magnitude
       :type: bool | None

       (Not yet documented)

    .. attribute:: reload_block_auto
       :type: bool | None

       (Not yet documented)

    .. attribute:: reload_continuous
       :type: bool | None

       (Unused, always False or not set.)

    .. attribute:: reload_ammo_fill_ms
       :type: int | None

       The time between ammo refill ticks.

    .. attribute:: reload_chamber_ms
       :type: int | None

       The chamber time for bolt-action weapons.

    .. attribute:: reload_loop_start_ms
       :type: int | None

       The initial loop time for reloading with looped reload weapons
       (such as pump action shotguns).

    .. attribute:: reload_loop_end_ms
       :type: int | None

       The final delay after reloading a looped reload weapon is
       completed.

    .. attribute:: reload_time_ms
       :type: int

       The reload time of the weapon. For looped weapons, this is the
       inner loop delay between ticks.

    .. attribute:: sway_amplitude_x
       :type: float | None

       Sway amplitude in X direction.

    .. attribute:: sway_amplitude_y
       :type: float | None

       Sway amplitude in Y direction.

    .. attribute:: sway_can_steady
       :type: bool | None

       Whether the player can hold their breath to
            stop camera sway.

    .. attribute:: sway_period_x
       :type: int | None

       Sway period in X direction in milliseconds.

    .. attribute:: sway_period_y
       :type: int | None

       Sway period in Y direction in milliseconds.

    .. attribute:: armor_penetration
       :type: float | None

       (Unused as of June 2020)

    .. attribute:: max_damage
       :type: int | None

       Maximum direct damage of the weapon.

    .. attribute:: max_damage_ind
       :type: int | None

       Maximum indirect damage of the weapon.

    .. attribute:: max_damage_ind_radius
       :type: float | None

       The radius over which maximum indirect damage of the weapon will
       be applied (aka. "inner splash").

    .. attribute:: max_damage_range
       :type: float | None

       The range up to which the weapon will deal its maximum direct
       damage.

    .. attribute:: min_damage
       :type: int | None

       The minimum direct damage of the weapon.

    .. attribute:: min_damage_ind
       :type: int | None

       The minimum indirect damage of the weapon.

    .. attribute:: min_damage_ind_radius
       :type: float | None

       The outer distance of the splash radius.

    .. attribute:: min_damage_range
       :type: float | None

       The range at which the weapon deals its
            minimum damage.

    .. attribute:: shield_bypass_pct
       :type: int | None

       The percentage of damage that will bypass shields and always
       affect the raw health pool.

    .. attribute:: description
       :type: auraxium.types.LocaleData

       Localised description of the fire mode (e.g. "Automatic").
    """

    collection = 'fire_mode_2'
    data: FireModeData
    id_field = 'fire_mode_id'
    _model = FireModeData

    # Type hints for data class fallback attributes
    id: int
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

    .. attribute:: id
       :type:

       The unique ID of this fire group.

    .. attribute:: chamber_duration_ms
       :type:

       The rechamber time for weapons in this
            group.

    .. attribute:: transition_duration_ms
       :type:

       (Not yet documented)

    .. attribute:: spool_up_ms
       :type:

       The duration of the spool-up period for this
            weapon group.

    .. attribute:: spool_up_initial_refire_ms
       :type:

       The initial fire speed (rounds
            per minute) of the weapon group. The weapon starts out at
            this value when firing, then tapers to the regular value
            after :attr:`spool_up_ms` milliseconds.

    .. attribute:: can_chamber_ironsights
       :type:

       Whether a bolt-action weapon can be
            rechambered while in ADS.

    """

    collection = 'fire_group'
    data: FireGroupData
    id_field = 'fire_group_id'
    _model = FireGroupData

    # Type hints for data class fallback attributes
    id: int
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
