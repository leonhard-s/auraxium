"""Defines weapon-related data types for PlanetSide 2."""

from ...base_api import Query
from ..datatypes import DataType
from .item import Item
from .projectile import Projectile
from .ability import Ability
from .effect import Effect
from .playerstate import PlayerStateGroup
from ..misc import LocalizedString
from ..exceptions import NoMatchesFoundError


class AmmoSlot():  # pylint: disable=too-few-public-methods
    """Represents an ammo slot for a weapon.

    A weapon's ammo slot is a type of ammunition this weapon can fire. This
    mainly concerns underbarrel attachments like grenade launchers or shotguns.

    """

    def __init__(self, data_dict):
        # Set attribute values
        self.capacity = data_dict['capacity']
        self.clip_size = data_dict['clip_size']
        self.refill_ammo_delay = data_dict.get('refill_ammo_delay_ms')
        self.refill_ammo_rate = data_dict.get('refill_ammo_rate')
        self.weapon_slot_index = data_dict['weapon_slot_index']


class FireGroup(DataType):
    """The fire group for a weapon.

    A fire group groups represents a fire mode available to a given weapon.
    Some weapons, like the VS Equinox VE2, have multiple ones.

    """

    _collection = 'fire_group'

    def __init__(self, id_):
        self.id_ = id_

        # Set default values
        self.chamber_duration = None
        self._fire_modes = None  # Internal (See properties)
        self.transition_duration = None
        self.spool_up = None
        self.spool_up_initial_refire = None
        self.can_chamber_ironsights = None

    # Define properties
    @property
    def fire_modes(self):
        """A list of fire modes in this fire group."""
        try:
            return self._fire_modes
        except AttributeError:
            data = Query(collection='fire_group_to_fire_mode', fire_group_id=self.id_).get()
            self._fire_modes = FireMode.list(ids=[i['fire_mode_id'] for i in data])
            return self._fire_modes

    def populate(self, data=None):
        data_dict = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self.chamber_duration = float(data_dict.get(
            'chamber_duration_ms')) / 1000.0 if data_dict.get(
                'chamber_duration_ms') is not None else None
        self.transition_duration = float(data_dict.get(
            'transition_duration_ms')) / 1000.0 if data_dict.get(
                'transition_duration_ms') is not None else None
        self.spool_up = float(data_dict.get('spool_up_ms')) / \
            1000.0 if data_dict.get('spool_up_ms') is not None else None
        self.spool_up_initial_refire = float(data_dict.get(
            'spool_up_initial_refire_ms')) / 1000 if data_dict.get(
                'spool_up_initial_refire_ms') is not None else None
        self.can_chamber_ironsights = data_dict.get('can_chamber_ironsights')


class FireMode(DataType):  # pylint: disable=too-many-instance-attributes
    """A weapon fire mode.

    A fire mode contains detailed information about the how the firing
    mechanics of the weapons using it operate.
    This object only contains information from the "fire_mode_2" collection.

    """

    _collection = 'fire_mode_2'
    _id_field = 'fire_mode_id'

    def __init__(self, id_):  # pylint: disable=too-many-statements
        self.id_ = id_

        # Set default values
        self._ability_id = None
        # self.ammo_slot = None
        self.armor_penetration = None
        self.automatic = None
        self.cof_override = None
        self.cof_pellet_spread = None
        self.cof_range = None
        self.cof_recoil = None
        self.cof_scalar = None
        self.cof_scalar_moving = None
        self._damage_direct_effect_id = None
        self.damage_head_multiplier = None
        self._damage_indirect_effect_id = None
        self.damage_legs_multiplier = None
        self.description = None
        self.fire_ammo_per_shot = None
        self.fire_auto_fire = None
        self.fire_burst_count = None
        self.fire_charge_up = None
        self.fire_delay = None
        self.fire_detect_range = None
        self.fire_duration = None
        self._fire_mode_type_id = None
        self.fire_pellets_per_shot = None
        self.fire_refire = None
        self.grief_immune = None
        self.heat_per_shot = None
        self.heat_recovery_delay = None
        self.heat_threshold = None
        self.iron_sights = None
        self.laser_guided = None
        self.lockon_acquire_close = None
        self.lockon_acquire_far = None
        self.lockon_acquire = None
        self.lockon_angle = None
        self.lockon_lose = None
        self.lockon_maintain = None
        self.lockon_radius = None
        self.lockon_range = None
        self.lockon_range_close = None
        self.lockon_range_far = None
        self.lockon_required = None
        self.max_damage = None
        self.max_damage_ind = None
        self.max_damage_ind_radius = None
        self.max_damage_range = None
        self.min_damage = None
        self.min_damage_ind = None
        self.min_damage_ind_radius = None
        self.min_damage_range = None
        self.move_modifier = None
        self._player_state_group_id = None
        self._projectile = None  # Internal (See properties)
        self.projectile_speed_override = None
        self.recoil_angle_max = None
        self.recoil_angle_min = None
        self.recoil_first_shot_modifier = None
        self.recoil_horizontal_max = None
        self.recoil_horizontal_max_increase = None
        self.recoil_horizontal_min = None
        self.recoil_horizontal_min_increase = None
        self.recoil_horizontal_tolerance = None
        self.recoil_increase = None
        self.recoil_increase_crouched = None
        self.recoil_magnitude_max = None
        self.recoil_magnitude_min = None
        self.recoil_max_total_magnitude = None
        self.recoil_recovery_acceleration = None
        self.recoil_recovery_delay = None
        self.recoil_recovery_rate = None
        self.recoil_shots_at_min_magnitude = None
        self.reload_ammo_fill = None
        self.reload_block_auto = None
        self.reload_chamber = None
        self.reload_continuous = None
        self.reload_loop_end = None
        self.reload_loop_start = None
        self.reload_time = None
        self.shield_bypass_pct = None
        self.sprint_fire = None
        self.sway_amplitude_x = None
        self.sway_amplitude_y = None
        self.sway_can_steady = None
        self.sway_period_x = None
        self.sway_period_y = None
        self.turn_modifier = None
        self.use_in_water = None
        self.zoom_default = None

    # Define properties
    @property
    def ability(self):
        """The ability linked to this fire mode."""
        return Ability.get(id_=self._ability_id)

    @property
    def damage_direct_effect(self):
        """The direct damage effect of the fire mode."""
        return Effect.get(id_=self._damage_direct_effect_id)

    @property
    def damage_indirect_effect(self):
        """The indirect damage effect of the fire mode."""
        return Effect.get(id_=self._damage_indirect_effect_id)

    @property
    def fire_mode_type(self):
        """The type of fire mode."""
        return FireModeType.get(id_=self._fire_mode_type_id)

    @property
    def player_state_group(self):
        """The player state group for this fire mode."""
        return PlayerStateGroup.get(id_=self._player_state_group_id)

    @property
    def projectile(self):
        """Lists the attachments available for this weapon."""
        try:
            return self._projectile
        except AttributeError:
            query = Query(collection='fire_mode_to_projectile', fire_mode_id=self.id_)
            query.join(type='projectile', inject_at='projectile')
            data = query.get(single=True)
            self._projectile = Projectile.get(id_=data['projectile_id'], data=data['projectile'])
            return self._projectile

    def populate(self, data=None):  # pylint: disable=too-many-statements
        data_dict = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self._ability_id = data_dict.get('ability_id')
        # self.ammo_slot = data_dict.get('ammo_slot')
        self.armor_penetration = data_dict.get('armor_penetration')
        self.automatic = data_dict.get('automatic')
        self.cof_override = data_dict.get('cof_override')
        self.cof_pellet_spread = data_dict.get('cof_pellet_spread')
        self.cof_range = data_dict.get('cof_range')
        self.cof_recoil = data_dict.get('cof_recoil')
        self.cof_scalar = data_dict.get('cof_scalar')
        self.cof_scalar_moving = data_dict.get('cof_scalar_moving')
        self._damage_direct_effect_id = data_dict.get('damage_direct_effect_id')
        self.damage_head_multiplier = data_dict.get('damage_head_multiplier')
        self._damage_indirect_effect_id = data_dict.get('damage_indirect_effect_id')
        self.damage_legs_multiplier = data_dict.get('damage_legs_multiplier')
        self.description = LocalizedString(data_dict.get('description'))
        self.fire_ammo_per_shot = data_dict.get('fire_ammo_per_shot')
        self.fire_auto_fire = data_dict.get('fire_auto_fire_ms')
        self.fire_burst_count = data_dict.get('fire_burst_count')
        self.fire_charge_up = data_dict.get('fire_charge_up_ms')
        self.fire_delay = data_dict.get('fire_delay_ms')
        self.fire_detect_range = data_dict.get('fire_detect_range')
        self.fire_duration = data_dict.get('fire_duration_ms')
        self._fire_mode_type_id = data_dict.get('fire_mode_type_id')
        self.fire_pellets_per_shot = data_dict.get('fire_pellets_per_shot')
        self.fire_refire = data_dict.get('fire_refire_ms')
        self.grief_immune = data_dict.get('grief_immune')
        self.heat_per_shot = data_dict.get('heat_per_shot')
        self.heat_recovery_delay = data_dict.get('heat_recovery_delay_ms')
        self.heat_threshold = data_dict.get('heat_threshold')
        self.iron_sights = data_dict.get('iron_sights')
        self.laser_guided = data_dict.get('laser_guided')
        self.lockon_acquire_close = data_dict.get('lockon_acquire_close_ms')
        self.lockon_acquire_far = data_dict.get('lockon_acquire_far_ms')
        self.lockon_acquire = data_dict.get('lockon_acquire_ms')
        self.lockon_angle = data_dict.get('lockon_angle')
        self.lockon_lose = data_dict.get('lockon_lose_ms')
        self.lockon_maintain = data_dict.get('lockon_maintain')
        self.lockon_radius = data_dict.get('lockon_radius')
        self.lockon_range = data_dict.get('lockon_range')
        self.lockon_range_close = data_dict.get('lockon_range_close')
        self.lockon_range_far = data_dict.get('lockon_range_far')
        self.lockon_required = data_dict.get('lockon_required')
        self.max_damage = data_dict.get('max_damage')
        self.max_damage_ind = data_dict.get('max_damage_ind')
        self.max_damage_ind_radius = data_dict.get('max_damage_ind_radius')
        self.max_damage_range = data_dict.get('max_damage_range')
        self.min_damage = data_dict.get('min_damage')
        self.min_damage_ind = data_dict.get('min_damage_ind')
        self.min_damage_ind_radius = data_dict.get('min_damage_ind_radius')
        self.min_damage_range = data_dict.get('min_damage_range')
        self.move_modifier = data_dict.get('move_modifier')
        self._player_state_group_id = data_dict.get('player_state_group_id')
        self.projectile_speed_override = data_dict.get('projectile_speed_override')
        self.recoil_angle_max = data_dict.get('recoil_angle_max')
        self.recoil_angle_min = data_dict.get('recoil_angle_min')
        self.recoil_first_shot_modifier = data_dict.get('recoil_first_shot_modifier')
        self.recoil_horizontal_max = data_dict.get('recoil_horizontal_max')
        self.recoil_horizontal_max_increase = data_dict.get('recoil_horizontal_max_increase')
        self.recoil_horizontal_min = data_dict.get('recoil_horizontal_min')
        self.recoil_horizontal_min_increase = data_dict.get('recoil_horizontal_min_increase')
        self.recoil_horizontal_tolerance = data_dict.get('recoil_horizontal_tolerance')
        self.recoil_increase = data_dict.get('recoil_increase')
        self.recoil_increase_crouched = data_dict.get('recoil_increase_crouched')
        self.recoil_magnitude_max = data_dict.get('recoil_magnitude_max')
        self.recoil_magnitude_min = data_dict.get('recoil_magnitude_min')
        self.recoil_max_total_magnitude = data_dict.get('recoil_max_total_magnitude')
        self.recoil_recovery_acceleration = data_dict.get('recoil_recovery_acceleration')
        self.recoil_recovery_delay = data_dict.get('recoil_recovery_delay_ms')
        self.recoil_recovery_rate = data_dict.get('recoil_recovery_rate')
        self.recoil_shots_at_min_magnitude = data_dict.get('recoil_shots_at_min_magnitude')
        self.reload_ammo_fill = data_dict.get('reload_ammo_fill_ms')
        self.reload_block_auto = data_dict.get('reload_block_auto')
        self.reload_chamber = data_dict.get('reload_chamber_ms')
        self.reload_continuous = data_dict.get('reload_continuous')
        self.reload_loop_end = data_dict.get('reload_loop_end_ms')
        self.reload_loop_start = data_dict.get('reload_loop_start_ms')
        self.reload_time = data_dict.get('reload_time_ms')
        self.shield_bypass_pct = data_dict.get('shield_bypass_pct')
        self.sprint_fire = data_dict.get('sprint_fire')
        self.sway_amplitude_x = data_dict.get('sway_amplitude_x')
        self.sway_amplitude_y = data_dict.get('sway_amplitude_y')
        self.sway_can_steady = data_dict.get('sway_can_steady')
        self.sway_period_x = data_dict.get('sway_period_x')
        self.sway_period_y = data_dict.get('sway_period_y')
        self.turn_modifier = float(data_dict.get('turn_modifier'))
        self.use_in_water = data_dict.get('zoom_default')
        self.zoom_default = data_dict.get('zoom_default')


class FireModeType(DataType):
    """The fire mode type for a given fire mode.

    Fire mode types provide a basic classification of how a given weapon
    operates.
    Examples are "Melee", "Projectile" and "Trigger Item Ability".

    """

    _collection = 'fire_mode_type'

    def __init__(self, id_):
        self.id_ = id_

        # Set default values
        self.description = None

    def populate(self, data=None):
        data_dict = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self.description = data_dict.get('description')


class Weapon(DataType):  # pylint: disable=too-many-instance-attributes
    """Contains information about a weapon.

    This data_dict type can be seen as an extension to the corresponding `item`
    object. It contains weapon-specific information and connects the item with
    internal mechanics like fire modes or projectiles.

    """

    _collection = 'weapon'

    def __init__(self, id_):
        self.id_ = id_

        # Set default values
        self._ammo_slot = None  # Internal (See properties)
        self._attachments = None  # Internal (See properties)
        self.equip_time = None
        self._fire_groups = None  # Internal (See properties)
        self.group_id = None
        self._item = None  # Internal (See properties)
        self.heat_bleed_off_rate = None
        self.heat_capacity = None
        self.heat_overheat_cooldown = None
        self.iron_sights_enter_ads = None
        self.iron_sights_exit_ads = None
        self.melee_detect_height = None
        self.melee_detect_width = None
        self.move_speed_modifier = None
        self.sprint_recovery = None
        self.turn_speed_modifier = None
        self.unequip_time = None

    # Define properties
    @property
    def ammo_slot(self):
        """Lists the attachments available for this weapon."""
        try:
            return self._ammo_slot
        except AttributeError:
            data = Query(collection='weapon_ammo_slot', weapon_id=self.id_).get()
            # NOTE: The following line is not an error, AmmoSlot does not have a list() method as
            # it does not generate any network traffic.
            self._ammo_slot = [AmmoSlot(a) for a in data]
            return self._ammo_slot

    @property
    def attachments(self):
        """Lists the attachments available for this weapon."""
        try:
            return self._attachments
        except AttributeError:
            data = Query(collection='weapon_to_attachment', weapon_id=self.id_).get()
            self._attachments = Item.list(ids=[i['item_id'] for i in data])
            return self._attachments

    @property
    def fire_groups(self):
        """The fire group used by this weapon."""
        try:
            return self._fire_groups
        except AttributeError:
            data = Query(collection='weapon_to_fire_group', weapon_id=self.id_).get()
            self._fire_groups = FireGroup.list(ids=[f['fire_group_id'] for f in data])
            return self._fire_groups

    @property
    def item(self):
        """Links a weapon to its item."""
        try:
            return self._item
        except AttributeError:
            query = Query(collection='item_to_weapon', weapon_id=self.id_)
            query.join(collection='item', inject_at='item_to_weapon')
            data_dict = query.get(single=True)
            self._item = Item.get(id_=data_dict['item_id'])
            return self._item

    @staticmethod
    def get_by_name(name, locale, ignore_case=True):
        """Allows retrieval of a weapon by its item's name."""
        # Generate request
        query = Query(collection='item').case(not ignore_case)
        query.add_term(field='name.' + locale, value=name)
        join = query.join(collection='item_to_weapon', inject_at='item_to_weapon',
                          on='item_id', to='item_id')
        join.join(collection='weapon', inject_at='weapon', on='weapon_id', to='weapon_id')
        try:
            data = query.get(single=True)['item_to_weapon']['weapon']
        except TypeError:
            raise NoMatchesFoundError
        # Retrieve and return the object
        instance = Weapon.get(id_=data['weapon_id'], data=data)
        return instance

    def populate(self, data=None):
        data_dict = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self.equip_time = float(data_dict.get('equip_ms')) / \
            1000.0 if data_dict.get('equip_ms') is not None else None
        self.group_id = data_dict.get('weapon_group_id')
        self.heat_bleed_off_rate = data_dict.get('heat_bleed_off_rate')  # Unit?
        self.heat_capacity = data_dict.get('heat_capacity')
        self.heat_overheat_cooldown = float(data_dict.get(
            'heat_overheat_penalty_ms')) / 1000.0 if data_dict.get(
                'heat_overheat_penalty_ms') is not None else None
        self.iron_sights_enter_ads = float(data_dict.get(
            'to_iron_sights_ms')) / 1000.0 if data_dict.get(
                'to_iron_sights_ms') is not None else None
        self.iron_sights_exit_ads = float(
            data_dict.get('from_iron_sights_ms')) / 1000.0 if data_dict.get(
                'from_iron_sights_ms') is not None else None
        self.melee_detect_height = data_dict.get('melee_detect_height')
        self.melee_detect_width = data_dict.get('melee_detect_width')
        self.move_speed_modifier = data_dict.get('move_modifier')
        self.sprint_recovery = float(data_dict.get(
            'sprint_recovery_ms')) / 1000.0 if data_dict.get(
                'sprint_recovery_ms') is not None else None
        self.turn_speed_modifier = data_dict.get('turn_modifier')
        self.unequip_time = float(
            data_dict.get('unequip_ms')) / 1000.0 if data_dict.get(
                'unequip_ms') is not None else None
