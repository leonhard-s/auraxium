"""Fire modes and group class definitions."""

import dataclasses
import enum
from typing import Dict, Final, Optional

from ..base import Cached, Ps2Data
from ..census import Query
from ..proxy import InstanceProxy, SequenceProxy
from ..request import extract_payload
from ..types import CensusData
from ..utils import LocaleData, optional

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


@dataclasses.dataclass(frozen=True)
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
    lockon_radius: Optional[float]  # Not used as of June 2020
    lockon_range: Optional[float]  # Maybe this replaced "lockon_radius"?
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
            optional(data, 'lockon_range', float),
            optional(data, 'lockon_range_close', float),
            optional(data, 'lockon_range_far', float),
            optional(data, 'lockon_required', bool),
            optional(data, 'recoil_angle_max', float),
            optional(data, 'recoil_angle_min', float),
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

    @staticmethod
    def _build_dataclass(data: CensusData) -> FireModeData:
        return FireModeData.from_census(data)

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
            group = PlayerStateGroup.from_census(group_data)
            state = PlayerState(group.player_state_id)
            states[state] = group
        return states

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

    @staticmethod
    def _build_dataclass(data: CensusData) -> FireGroupData:
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
