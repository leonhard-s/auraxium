"""Fire modes and group class definitions."""

import enum
from typing import Any, Dict, Final, cast

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
    """Specifies the type of action taken when a weapon is fired.

    The default fire mode type, ``PROJECTILE``, is used for hipfired or
    otherwise unaimed weapons. ``IRON_SIGHT`` is used when aiming down
    sights (ADS).

    ``MELEE`` is used for both quick knifing and equipped knives.
    ``THROWN`` is responsible for grenades and mines, and
    ``TRIGGER_ITEM_ABILITY`` is a hook used to place turrets and other
    constructable items.

    Values:::

       PROJECTILE           =  0  # Hipfire
       IRON_SIGHT           =  1  # Aim down sights
       MELEE                =  3
       TRIGGER_ITEM_ABILITY =  8
       THROWN               = 12
    """

    PROJECTILE = 0
    IRON_SIGHT = 1
    MELEE = 3
    TRIGGER_ITEM_ABILITY = 8
    THROWN = 12

    def __str__(self) -> str:
        literals = ['Projectile', 'Iron Sight', 'Melee',
                    'Trigger Item Ability', 'Thrown']
        return literals[int(self.value)]


class FireMode(Cached, cache_size=10, cache_ttu=3600.0):
    """A fire mode of a weapon.

    An API fire mode defines the bulk of a weapon's stats, such as
    reload times, default accuracy and cone-of-fire characteristics.

    .. note::

       Do not confuse this with in-game fire modes (automatic, triple
       burst, etc.). Those are represented by the :class:`FireGroup`
       class instead.

    Most infantry weapons have two fire modes, one for being hipfired
    and another used when aiming down sights. For more information on
    fire mode types, see the :class:`FireModeType` class.

    Keep in mind that most accuracy-related stats can be overwritten by
    the current :class:`~auraxium.ps2.PlayerState`, i.e. whether the
    player is jumping, crouching, etc.

    See the :meth:`state_groups` method for a mapping of player states
    to the state group entries for this fire mode.

    .. attribute:: id
       :type: int

       The unique ID of this fire mode. In the API payload, this field
       is called ``fire_mode_id``.

    .. attribute:: fire_mode_type_id
       :type: int | None

       The ID of the :class:`~auraxium.ps2.FireModeType` of the fire
       mode.

       .. seealso::

          :meth:`type` -- The type of this fire mode.

    .. attribute:: ability_id
       :type: int | None

       The item ability ID to trigger when the weapon is fired. Only
       valid for fire modes of type ``TRIGGER_ITEM_ABILITY``.

    .. attribute:: ammo_slot
       :type: int | None

       The index of the ammo slot used by this fire mode. This field is
       used to select the ammo reservoir to use for this fire mode.

    .. attribute:: automatic
       :type: bool

       Whether the fire mode is fully automatic or not.

    .. attribute:: grief_immune
       :type: bool | None

       Whether friendly fire is disabled for this fire mode.

    .. attribute:: iron_sights
       :type: bool | None

       Whether this fire mode is using iron sights. This is generally
       true is :attr:`fire_mode_type_id` is set to ``IRON_SIGHTS``.

    .. attribute:: laser_guided
       :type: bool | None

       Whether this weapon is laser guided (such as the Hornet Missles
       on empire-specific fighter aircraft).

    .. attribute:: move_modifier
       :type: float

       The movement speed modifier applied while in this fire mode.
       Higher values provide increased mobility, particularly while
       aiming down sights.

    .. attribute:: projectile_speed_override
       :type: int | None

       A fire mode specific override used to override the default
       :class:`Projectile` 's speed for this fire mode.

       It is recommended to use this value over the projectile's if
       available.

    .. attribute:: sprint_fire
       :type: bool | None

       Whether the fire mode allows firing and sprinting. This is
       generally only true for quick knife fire modes.

    .. attribute:: turn_modifier
       :type: float

       A turn speed modifier applied while in this fire mode.

       This is how MAXes turn speed is limited; all MAX weapons use a
       0.75 turn rate modifier.

    .. attribute:: use_in_water
       :type: bool | None

       Whether the weapon can be used in water.

       This is true for knives and false for all other weapons. Since
       most bodies of water instantly kill players touching them, this
       value has no real effect.

    .. attribute:: zoom_default
       :type: float

       The default zoom level of the fire mode (i.e. without any scopes
       attached).

    .. attribute:: cof_override
       :type: float | None

       Unused.

    .. attribute:: cof_pellet_spread
       :type: float | None

       The pellet spread used for multi-projectile weapons (such as
       non-slug shotguns or the NSX Tengu).

    .. attribute:: cof_range
       :type: float

       Potentially unused? More testing needed.

    .. attribute:: cof_recoil
       :type: float | None

       Cone of fire bloom per shot fired in degrees.

    .. attribute:: cof_scalar
       :type: float

       The starting cone of fire scalar. This mainly exists so it can
       be modified by attachments like laser sights.

       .. note::

          The VS's Spiker is the only item with a base cof scalar of
          0.5. All other items use 1.0.

    .. attribute:: cof_scalar_moving
       :type: float

       The starting cone-of-fire scalar while moving. This exists so it
       can be modified by attachments. Always 1.0.

    .. attribute:: player_state_group_id
       :type: int

       The ID of the :class:`~auraxium.models.PlayerStateGroup` for
       this fire mode. State groups are used to modify weapon accuracy
       depending on the current :class:`~auraxium.ps2.PlayerState`,
       i.e. whether the player is standing, crouching, etc.

    .. attribute:: damage_direct_effect_id
       :type: int | None

       The damage :class:`~auraxium.ps2.Effect` created on direct hits.

    .. attribute:: damage_head_multiplier
       :type: float | None

       The headshot multiplier for the fire mode.

    .. attribute:: damage_indirect_effect_id
       :type: int | None

       The damage :class:`~auraxium.ps2.Effect` created on indirect
       hits.

    .. attribute:: damage_legs_multiplier
       :type: float | None

       The leg shot multiplier for the fire mode.

    .. attribute:: fire_ammo_per_shot
       :type: int | None

       The amount of ammo consumed per shot. Some weapons, like the VS
       Lancer, may consume more than 1 bullet per shot.

    .. attribute:: fire_auto_fire_ms
       :type: int | None

       The weapon's refire rate in fixed burst fire modes, such as the
       NSX Yumi's five shot burst.

    .. attribute:: fire_burst_count
       :type: int | None

       The burst size of fixed burst fire modes.

    .. attribute:: fire_charge_up_ms
       :type: int | None

       The maximum amount of time the weapon can be charged before
       firing automatically. Used in the VS's Lancer rocket launcher.

    .. attribute:: fire_delay_ms
       :type: int | None

       The delay between pulling the trigger and the weapon actually
       firing. Used in the NXS Yumi.

    .. attribute:: fire_detect_range
       :type: float | None

       The base minimap detection range when firing this weapon. Can be
       modified by silencers or other barrel attachments.

    .. attribute:: fire_duration_ms
       :type: int | None

       The firing duration of a weapon. Used for the ``MELEE`` and
       ``THROWN`` :class:`FireModeType` 's to sync the damage/throwable
       release with the player model's animation.

    .. attribute:: fire_refire_ms
       :type: int | None

       The amount of time between shots.

       For automatic weapons, this is directly related to the rate of
       fire:::

          rounds-per-minute = 60'000 / refire_time_ms

          rate-of-fire      = 1'000 / refire_time_ms

    .. attribute:: fire_pellets_per_shot
       :type: int | None

       The number of pellets fired by non-slug shotguns or the NSX
       Tengu per shot.

    .. attribute:: heat_per_shot
       :type: int | None

       The amount of heat generated per shot.

    .. attribute:: heat_recovery_delay_ms
       :type: int | None

       The duration after which weapon heat will start to dissipate.

    .. attribute:: heat_threshold
       :type: int | None

       The overheating threshold of the weapon. This is comparable to
       the magazine size for heat-based weapons, with the number of
       shots available without overheating being equal to the floor of
       :attr:`heat_threshold` divided :attr:`heat_per_shot`:::

          heat-magazine-size = heat_threshold // heat_per_shot + 1

    .. attribute:: lockon_acquire_close_ms
       :type: int | None

       The time required to establish a lock at the launcher's minimum
       lock-on distance.

       This value is used for fire modes whose acquire time depends on
       the distance from the target.

       .. seealso::

          :attr:`lockon_acquire_ms` -- Lock-on acquire time for fire
          modes with constant acquire times.

    .. attribute:: lockon_acquire_far_ms
       :type: int | None

       The time required to establish a lock at the launcher's maximum
       lock-on distance.

       This value is used for fire modes whose acquire time depends on
       the distance from the target.

       .. seealso::

          :attr:`lockon_acquire_ms` -- Lock-on acquire time for fire
          modes with constant acquire times.

    .. attribute:: lockon_acquire_ms
       :type: int | None

       The time required to establish a lock at the target.

       This value is used for fire modes whose acquire time does not
       change with distance from the target.

       .. seealso::

          :attr:`lockon_acquire_close_ms` -- Minimum acquire time for
          fire modes whose acquire time depends on the distance from
          the target.

          :attr:`lockon_acquire_far_ms` -- Maximum acquire time for
          fire modes whose acquire time depends on the distance from
          the target.

    .. attribute:: lockon_angle
       :type: float | None

       The maximum error allowed while locking on. As long as the
       target is within this cone, lock-on acquisition will continue.

    .. attribute:: lockon_lose_ms
       :type: int | None

       The amount of time over which an establish lock will be lost.
       Re-acquiring a lock within this time will not reset the lock-on
       acquisition timer.

    .. attribute:: lockon_maintain
       :type: bool | None

       Whether a lock must be maintained until impact (like for A2A
       lock-ons) or whether the projetile will continue tracking its
       target on its own (as for most infantry launchers).

    .. attribute:: lockon_radius
       :type: float | None

       Not used as of June 2020, use :attr:`lockon_range` instead.

    .. attribute:: lockon_range
       :type: float | None

       The maximum range at which a lock can be maintained. If the
       target moves beyond this range, an existing lock is lost.

    .. attribute:: lockon_range_close
       :type: float | None

       The minimum lock-on distance. Used for launchers whose lock-on
       acquisition time depends on distance from the target.

       .. seealso::

          :attr:`lockon_acquire_close_ms` -- The time required to
          establish a lock at minimum lock-on distance.

    .. attribute:: lockon_range_far
       :type: float | None

       The maximum lock-on distance. Used for launchers whose lock-on
       acquisition time depends on distance from the target.

       .. seealso::

          :attr:`lockon_acquire_far_ms` -- The time required to
          establish a lock at maximum lock-on distance.

    .. attribute:: lockon_required
       :type: bool | None

       Whether this weapon can be fired without being locked on (true
       for the NS Annihilator, false for most faction-specific lock-on
       launchers).

    .. attribute:: recoil_angle_max
       :type: float | None

       The maximum recoil angle, used to randomise recoil angle.

       After every shot, the weapon will kick in a random direction
       between :attr:`recoil_angle_min` and this value.

    .. attribute:: recoil_angle_min
       :type: float | None

       The minimum recoil angle, used to randomise recoil angle.

       After every shot, the weapon will kick in a random direction
       between this value and :attr:`recoil_angle_max`.

    .. attribute:: recoil_first_shot_modifier
       :type: float | None

       A recoil multiplier override for the first shot fired in
       automatic mode. When single-shot bursting, this override is
       applied to every shot.

       For fixed-size bursts (e.g. triple burst fire modes), this will
       only be applied to the first shot of every burst.

    .. attribute:: recoil_horizontal_max
       :type: float | None

       The maximum horizontal recoil per shot. After every shot, the
       weapon will kick up by a random angle between
       :attr:`recoil_horizontal_min` and this value.

    .. attribute:: recoil_horizontal_max_increase
       :type: float | None

       Some weapons' recoil increases or decreases with consecutive
       shots. This value denotes by how much the maximum horizontal
       recoil will change with each shot fired.

    .. attribute:: recoil_horizontal_min
       :type: float | None

       The maximum horizontal recoil per shot. After every shot, the
       weapon will kick up by a random angle between this value and
       :attr:`recoil_horizontal_max`.

    .. attribute:: recoil_horizontal_min_increase
       :type: float | None

       Some weapons' recoil increases or decreases with consecutive
       shots. This value denotes by how much the minimum horizontal
       recoil will change with each shot fired.

    .. attribute:: recoil_horizontal_tolerance
       :type: float | None

       The maximum horizontal deviation of the recoil from the initial
       aiming position before it must kick back towards the other
       direction.

    .. attribute:: recoil_increase
       :type: float | None

       Some weapons' recoil increases or decreases with consecutive
       shots. This value denotes by how much the vertical recoil will
       change with each shot fired.

       For negative values, the maximum recoil will go down until it
       meets the minimum, for positive values the minimum recoil will
       climb until it equals the maximum recoil.

       The base vertical recoil while standing.

    .. attribute:: recoil_increase_crouched
       :type: float | None

       Same as :attr:`recoil_increase` but only affects the crouched
       :class:`~auraxium.ps2.PlayerState`.

    .. attribute:: recoil_magnitude_max
       :type: float | None

       The maximum vertical recoil per shot. After every shot, the
       weapon will kick up by a random angle between
       :attr:`recoil_magnitude_min` and this value.

    .. attribute:: recoil_magnitude_min
       :type: float | None

       The minimum vertical recoil per shot. After every shot, the
       weapon will kick up by a random angle between this value and
       :attr:`recoil_magnitude_max`.

    .. attribute:: recoil_max_total_magnitude
       :type: float | None

       The total maximum recoil, including both the horizontal and
       vertical component.

    .. attribute:: recoil_recovery_acceleration
       :type: int | None

       The acceleration at which the recoil recovery will reach its
       full recovery rate. Lower values lead to a more progressive
       recovery rate, where the initial recoil recovery window is less
       effective than they would be with a linear recovery rate.

       .. note::

          No conclusive tests regarding this field yet.

    .. attribute:: recoil_recovery_delay_ms
       :type: int | None

       The delay in milliseconds before the weapon will start to reset
       to its default cone of fire after the player stopped firing.

    .. attribute:: recoil_recovery_rate
       :type: int | None

       The speed at which the weapon will reset to its original cone of
       fire after the player stopped firing.

    .. attribute:: recoil_shots_at_min_magnitude
       :type: int | None

       The number of shots before which the recoil penalties will take
       effect. This is 0 or 1 for most weapons, some vehicle weapons
       like the G40-F Ranger get 3 or more high accuracy shots before
       recoil penalties starts taking effect.

    .. attribute:: reload_block_auto
       :type: bool | None

       Untested: this value seems to correlate with a weapon's ability
       to reload while aiming down sights.

    .. attribute:: reload_continuous
       :type: bool | None

       Whether the weapon uses a continuous reload system where shots
       are reloaded bullet by bullet (as pump action shotguns do).

    .. attribute:: reload_ammo_fill_ms
       :type: int | None

       The delay between ammo pack refill ticks.

    .. attribute:: reload_chamber_ms
       :type: int | None

       The per-chamber reload time for weapons that are reloaded
       sequentially (such as pump action shotguns).

    .. attribute:: reload_loop_start_ms
       :type: int | None

       The initial loop time for reloading with looped reload weapons
       (such as pump action shotguns).

       Used to sync up the reload with the character model's animation.

    .. attribute:: reload_loop_end_ms
       :type: int | None

       The final delay after reloading a looped reload weapon is
       completed.

       Used to sync up the reload with the character model's animation.

    .. attribute:: reload_time_ms
       :type: int | None

       The reload time of the weapon.

    .. attribute:: sway_amplitude_x
       :type: float | None

       Sway amplitude in X direction.

    .. attribute:: sway_amplitude_y
       :type: float | None

       Sway amplitude in Y direction.

    .. attribute:: sway_can_steady
       :type: bool | None

       Whether the player can hold their breath to stop camera sway.

    .. attribute:: sway_period_x
       :type: int | None

       Sway period in X direction in milliseconds.

    .. attribute:: sway_period_y
       :type: int | None

       Sway period in Y direction in milliseconds.

    .. attribute:: armor_penetration
       :type: float | None

       Unused as of June 2020.

    .. attribute:: max_damage
       :type: int | None

       Maximum direct damage of the weapon.

       For constant damage effects or damage fall off effects (effect
       type ID 36 or 45), this field is a direct link to the direct
       damage :class:`~auraxium.ps2.Effect` 's ``param1`` field.

       As of April 2021, this link is confirmed to be without errors
       for all fire modes that have a direct damage effect.

    .. attribute:: max_damage_ind
       :type: int | None

       Maximum indirect damage of the weapon.

       For indirect damage effects (effect type ID 40), this field is a
       direct link to the direct damage :class:`~auraxium.ps2.Effect` 's
       ``param1`` field.

       As of April 2021, this link is confirmed to be without errors
       for all fire modes that have a direct damage effect.

    .. attribute:: max_damage_ind_radius
       :type: float | None

       The radius over which maximum indirect damage of the weapon will
       be applied (aka. "inner splash").

       For indirect damage effects (effect type ID 40), this field is a
       direct link to the direct damage :class:`~auraxium.ps2.Effect` 's
       ``param2`` field.

       As of April 2021, this link is confirmed to be without errors
       for all fire modes that have a direct damage effect.

    .. attribute:: max_damage_range
       :type: float | None

       The range up to which the weapon will deal its maximum direct
       damage.

       For damage fall off effects (effect type ID 45), this field is a
       direct link to the direct damage :class:`~auraxium.ps2.Effect` 's
       ``param2`` field.

       As of April 2021, this link is confirmed to be without errors
       for all fire modes that have a direct damage effect.

    .. attribute:: min_damage
       :type: int | None

       The minimum direct damage of the weapon.

       For damage fall off effects (effect type ID 45), this field is a
       direct link to the direct damage :class:`~auraxium.ps2.Effect` 's
       ``param3`` field.

       As of April 2021, this link is confirmed to be without errors
       for all fire modes that have a direct damage effect.

    .. attribute:: min_damage_ind
       :type: int | None

       Minimum indirect damage of the weapon.

       For indirect damage effects (effect type ID 40), this field is a
       direct link to the direct damage :class:`~auraxium.ps2.Effect` 's
       ``param3`` field.

    .. attribute:: min_damage_ind_radius
       :type: float | None

       The outer limit of the splash radius. Beyond this distance, no
       damage will be dealt.

       For indirect damage effects (effect type ID 40), this field is a
       direct link to the direct damage :class:`~auraxium.ps2.Effect` 's
       ``param5`` field.

       As of April 2021, this link is confirmed to be without errors
       for all fire modes that have a direct damage effect.

    .. attribute:: min_damage_range
       :type: float | None

       The range at which the weapon deals its minimum damage.

       For damage fall off effects (effect type ID 45), this field is a
       direct link to the direct damage :class:`~auraxium.ps2.Effect` 's
       ``param5`` field.

       As of April 2021, this link is confirmed to be without errors
       for all fire modes that have a direct damage effect.

    .. attribute:: shield_bypass_pct
       :type: int | None

       The percentage of damage that will bypass shields and always
       affect the raw health pool.

       As of April 2021, this field is set to 130 for the default
       faction-speficic launchers, but no such mechanic is observed
       in-game.

    .. attribute:: description
       :type: auraxium.types.LocaleData | None

       Localised description of the fire mode (e.g. "Automatic").
    """

    collection = 'fire_mode_2'
    data: FireModeData
    id_field = 'fire_mode_id'
    _model = FireModeData

    # Type hints for data class fallback attributes
    id: int
    fire_mode_type_id: int | None
    ability_id: int | None
    ammo_slot: int | None
    automatic: bool
    grief_immune: bool | None
    iron_sights: bool | None
    laser_guided: bool | None
    move_modifier: float
    projectile_speed_override: int | None
    sprint_fire: bool | None
    turn_modifier: float
    use_in_water: bool | None
    zoom_default: float
    cof_override: float | None
    cof_pellet_spread: float | None
    cof_range: float
    cof_recoil: float | None
    cof_scalar: float
    cof_scalar_moving: float
    player_state_group_id: int
    damage_direct_effect_id: int | None
    damage_head_multiplier: float | None
    damage_indirect_effect_id: int | None
    damage_legs_multiplier: float | None
    fire_ammo_per_shot: int | None
    fire_auto_fire_ms: int | None
    fire_burst_count: int | None
    fire_charge_up_ms: int | None
    fire_delay_ms: int | None
    fire_detect_range: float | None
    fire_duration_ms: int | None
    fire_refire_ms: int | None
    fire_pellets_per_shot: int | None
    heat_per_shot: int | None
    heat_recovery_delay_ms: int | None
    heat_threshold: int | None
    lockon_acquire_close_ms: int | None
    lockon_acquire_far_ms: int | None
    lockon_acquire_ms: int | None
    lockon_angle: float | None
    lockon_lose_ms: int | None
    lockon_maintain: bool | None
    lockon_range: float | None
    lockon_range_close: float | None
    lockon_range_far: float | None
    lockon_required: bool | None
    recoil_angle_max: float | None
    recoil_angle_min: float | None
    recoil_first_shot_modifier: float | None
    recoil_horizontal_max: float | None
    recoil_horizontal_max_increase: float | None
    recoil_horizontal_min: float | None
    recoil_horizontal_min_increase: float | None
    recoil_horizontal_tolerance: float | None
    recoil_increase: float | None
    recoil_increase_crouched: float | None
    recoil_magnitude_max: float | None
    recoil_magnitude_min: float | None
    recoil_max_total_magnitude: float | None
    recoil_recovery_acceleration: int | None
    recoil_recovery_delay_ms: int | None
    recoil_recovery_rate: int | None
    recoil_shots_at_min_magnitude: int | None
    reload_block_auto: bool | None
    reload_continuous: bool | None
    reload_ammo_fill_ms: int | None
    reload_chamber_ms: int | None
    reload_loop_start_ms: int | None
    reload_loop_end_ms: int | None
    reload_time_ms: int | None
    sway_amplitude_x: float | None
    sway_amplitude_y: float | None
    sway_can_steady: bool | None
    sway_period_x: int | None
    sway_period_y: int | None
    armor_penetration: float | None
    max_damage: int | None
    max_damage_ind: int | None
    max_damage_ind_radius: float | None
    max_damage_range: float | None
    min_damage: int | None
    min_damage_ind: int | None
    min_damage_ind_radius: float | None
    min_damage_range: float | None
    shield_bypass_pct: int | None
    description: LocaleData

    @property
    def type(self) -> FireModeType | None:
        """Return the type of fire mode as an enum."""
        if self.data.fire_mode_type_id is None:
            return None
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
            group = PlayerStateGroup(**cast(Any, group_data))
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
    """A fire group of a weapon.

    Fire groups are comparable to the in-game fire modes, such as fixed
    burst, semi auto or fully automatic. They are also used to
    implement auxiliary fire modes such as under-barrel launchers.

    .. attribute:: id
       :type: int

       The unique ID of this fire group. In the API payload, this field
       is called ``fire_group_id``.

    .. attribute:: chamber_duration_ms
       :type: int | None

       The amount of time required to rechamber after firing. This is
       used for pump action shotguns and bolt action sniper rifles and
       must be added to their respective refire time for fire rate
       calculation.

    .. attribute:: transition_duration_ms
       :type: int | None

       The time required to transition to this fire group. This defines
       the delay between equipping an underbarrel shotgun and being
       able to fire it.

    .. attribute:: spool_up_ms
       :type: int | None

       The duration of the spool-up period for this fire group.

    .. attribute:: spool_up_initial_refire_ms
       :type: int | None

       The initial fire speed (rounds per minute) of the fire group.
       The weapon starts out at this value when firing, then tapers to
       the regular value after :attr:`spool_up_ms` milliseconds.

    .. attribute:: can_chamber_ironsights
       :type: bool | None

       Whether a bolt-action weapon can be rechambered while in ADS.
    """

    collection = 'fire_group'
    data: FireGroupData
    id_field = 'fire_group_id'
    _model = FireGroupData

    # Type hints for data class fallback attributes
    id: int
    chamber_duration_ms: int | None
    transition_duration_ms: int | None
    spool_up_ms: int | None
    spool_up_initial_refire_ms: int | None
    can_chamber_ironsights: bool | None

    def fire_modes(self) -> SequenceProxy[FireMode]:
        """Return the fire modes in the fire group."""
        collection: Final[str] = 'fire_group_to_fire_mode'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        query.limit(20)
        join = query.create_join(FireMode.collection)
        join.set_fields(FireMode.id_field)
        return SequenceProxy(FireMode, query, client=self._client)
