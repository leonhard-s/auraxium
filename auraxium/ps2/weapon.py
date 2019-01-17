from ..census import Query
from ..datatypes import CachableDataType, EnumeratedDataType
from .item import Item
from .projectile import Projectile
from .ability import Ability
from .effect import Effect
from .playerstate import PlayerStateGroup
from ..misc import LocalizedString
from ..exceptions import NoMatchesFoundError


class AmmoSlot(object):
    """Represents an ammo slot for a weapon.

    A weapon's ammo slot is a type of ammunition this weapon can fire. This
    mainly concerns underbarrel attachments like grenade launchers or shotguns.

    """

    def __init__(self, d):
        # Set attribute values
        self.capacity = d['capacity']
        self.clip_size = d['clip_size']
        self.refill_ammo_delay = d.get('refill_ammo_delay_ms')
        self.refill_ammo_rate = d.get('refill_ammo_rate')
        self.weapon_slot_index = d['weapon_slot_index']


class FireGroup(CachableDataType):
    """The fire group for a weapon.

    A fire group groups represents a fire mode available to a given weapon.
    Some weapons, like the VS Equinox VE2, have multiple ones.

    """

    _collection = 'fire_group'

    def __init__(self, id):
        self.id = id

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
        try:
            return self._fire_modes
        except AttributeError:
            q = Query(type='fire_group_to_fire_mode')
            d = q.add_filter(field='fire_group_id', value=self.id).get()
            self._fire_modes = FireMode.list(
                ids=[i['fire_mode_id'] for i in d])
            return self._fire_modes

    def _populate(self, data=None):
        d = data if data is not None else super()._get_data(self.id)

        # Set attribute values
        self.chamber_duration = float(d.get(
            'chamber_duration_ms')) / 1000.0 if d.get('chamber_duration_ms') is not None else None
        self.transition_duration = float(d.get(
            'transition_duration_ms')) / 1000.0 if d.get(
                'transition_duration_ms') is not None else None
        self.spool_up = float(d.get('spool_up_ms')) / \
            1000.0 if d.get('spool_up_ms') is not None else None
        self.spool_up_initial_refire = float(d.get(
            'spool_up_initial_refire_ms')) / 1000 if d.get(
                'spool_up_initial_refire_ms') is not None else None
        self.can_chamber_ironsights = d.get('can_chamber_ironsights')


class FireMode(CachableDataType):
    """A weapon fire mode.

    A fire mode contains detailed information about the how the firing
    mechanics of the weapons using it operate.
    This object only contains information from the "fire_mode_2" collection.

    """

    _collection = 'fire_mode_2'
    _id_field = 'fire_mode_id'

    def __init__(self, id):
        self.id = id

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
        return Ability.get(id=self._ability_id)

    @property
    def damage_direct_effect(self):
        return Effect.get(id=self._damage_direct_effect_id)

    @property
    def damage_indirect_effect(self):
        return Effect.get(id=self._damage_indirect_effect_id)

    @property
    def fire_mode_type(self):
        return FireModeType.get(id=self._fire_mode_type_id)

    @property
    def player_state_group(self):
        return PlayerStateGroup.get(id=self._player_state_group_id)

    @property
    def projectile(self):
        """Lists the attachments available for this weapon."""
        try:
            return self._projectile
        except AttributeError:
            q = Query(type='fire_mode_to_projectile')
            q.add_filter(field='fire_mode_id', value=self.id)
            q.join(type='projectile')
            d = q.get_single()
            self._projectile = Projectile.get(id=d['projectile_id'])
            return self._projectile

    def _populate(self, data=None):
        d = data if data is not None else super()._get_data(self.id)

        # Set attribute values
        self._ability_id = d.get('ability_id')
        # self.ammo_slot = d.get('ammo_slot')
        self.armor_penetration = d.get('armor_penetration')
        self.automatic = d.get('automatic')
        self.cof_override = d.get('cof_override')
        self.cof_pellet_spread = d.get('cof_pellet_spread')
        self.cof_range = d.get('cof_range')
        self.cof_recoil = d.get('cof_recoil')
        self.cof_scalar = d.get('cof_scalar')
        self.cof_scalar_moving = d.get('cof_scalar_moving')
        self._damage_direct_effect_id = d.get('damage_direct_effect_id')
        self.damage_head_multiplier = d.get('damage_head_multiplier')
        self._damage_indirect_effect_id = d.get('damage_indirect_effect_id')
        self.damage_legs_multiplier = d.get('damage_legs_multiplier')
        self.description = LocalizedString(d.get('description'))
        self.fire_ammo_per_shot = d.get('fire_ammo_per_shot')
        self.fire_auto_fire = d.get('fire_auto_fire_ms')
        self.fire_burst_count = d.get('fire_burst_count')
        self.fire_charge_up = d.get('fire_charge_up_ms')
        self.fire_delay = d.get('fire_delay_ms')
        self.fire_detect_range = d.get('fire_detect_range')
        self.fire_duration = d.get('fire_duration_ms')
        self._fire_mode_type_id = d.get('fire_mode_type_id')
        self.fire_pellets_per_shot = d.get('fire_pellets_per_shot')
        self.fire_refire = d.get('fire_refire_ms')
        self.grief_immune = d.get('grief_immune')
        self.heat_per_shot = d.get('heat_per_shot')
        self.heat_recovery_delay = d.get('heat_recovery_delay_ms')
        self.heat_threshold = d.get('heat_threshold')
        self.iron_sights = d.get('iron_sights')
        self.laser_guided = d.get('laser_guided')
        self.lockon_acquire_close = d.get('lockon_acquire_close_ms')
        self.lockon_acquire_far = d.get('lockon_acquire_far_ms')
        self.lockon_acquire = d.get('lockon_acquire_ms')
        self.lockon_angle = d.get('lockon_angle')
        self.lockon_lose = d.get('lockon_lose_ms')
        self.lockon_maintain = d.get('lockon_maintain')
        self.lockon_radius = d.get('lockon_radius')
        self.lockon_range = d.get('lockon_range')
        self.lockon_range_close = d.get('lockon_range_close')
        self.lockon_range_far = d.get('lockon_range_far')
        self.lockon_required = d.get('lockon_required')
        self.max_damage = d.get('max_damage')
        self.max_damage_ind = d.get('max_damage_ind')
        self.max_damage_ind_radius = d.get('max_damage_ind_radius')
        self.max_damage_range = d.get('max_damage_range')
        self.min_damage = d.get('min_damage')
        self.min_damage_ind = d.get('min_damage_ind')
        self.min_damage_ind_radius = d.get('min_damage_ind_radius')
        self.min_damage_range = d.get('min_damage_range')
        self.move_modifier = d.get('move_modifier')
        self._player_state_group_id = d.get('player_state_group_id')
        self.projectile_speed_override = d.get('projectile_speed_override')
        self.recoil_angle_max = d.get('recoil_angle_max')
        self.recoil_angle_min = d.get('recoil_angle_min')
        self.recoil_first_shot_modifier = d.get('recoil_first_shot_modifier')
        self.recoil_horizontal_max = d.get('recoil_horizontal_max')
        self.recoil_horizontal_max_increase = d.get(
            'recoil_horizontal_max_increase')
        self.recoil_horizontal_min = d.get('recoil_horizontal_min')
        self.recoil_horizontal_min_increase = d.get(
            'recoil_horizontal_min_increase')
        self.recoil_horizontal_tolerance = d.get('recoil_horizontal_tolerance')
        self.recoil_increase = d.get('recoil_increase')
        self.recoil_increase_crouched = d.get('recoil_increase_crouched')
        self.recoil_magnitude_max = d.get('recoil_magnitude_max')
        self.recoil_magnitude_min = d.get('recoil_magnitude_min')
        self.recoil_max_total_magnitude = d.get('recoil_max_total_magnitude')
        self.recoil_recovery_acceleration = d.get(
            'recoil_recovery_acceleration')
        self.recoil_recovery_delay = d.get('recoil_recovery_delay_ms')
        self.recoil_recovery_rate = d.get('recoil_recovery_rate')
        self.recoil_shots_at_min_magnitude = d.get(
            'recoil_shots_at_min_magnitude')
        self.reload_ammo_fill = d.get('reload_ammo_fill_ms')
        self.reload_block_auto = d.get('reload_block_auto')
        self.reload_chamber = d.get('reload_chamber_ms')
        self.reload_continuous = d.get('reload_continuous')
        self.reload_loop_end = d.get('reload_loop_end_ms')
        self.reload_loop_start = d.get('reload_loop_start_ms')
        self.reload_time = d.get('reload_time_ms')
        self.shield_bypass_pct = d.get('shield_bypass_pct')
        self.sprint_fire = d.get('sprint_fire')
        self.sway_amplitude_x = d.get('sway_amplitude_x')
        self.sway_amplitude_y = d.get('sway_amplitude_y')
        self.sway_can_steady = d.get('sway_can_steady')
        self.sway_period_x = d.get('sway_period_x')
        self.sway_period_y = d.get('sway_period_y')
        self.turn_modifier = float(d.get('turn_modifier'))
        self.use_in_water = d.get('zoom_default')
        self.zoom_default = d.get('zoom_default')


class FireModeType(EnumeratedDataType):
    """The fire mode type for a given fire mode.

    Fire mode types provide a basic classification of how a given weapon
    operates.
    Examples are "Melee", "Projectile" and "Trigger Item Ability".

    """

    _collection = 'fire_mode_type'

    def __init__(self, id):
        self.id = id

        # Set default values
        self.description = None

    def _populate(self, data=None):
        d = data if data is not None else super()._get_data(self.id)

        # Set attribute values
        self.description = d.get('description')


class Weapon(CachableDataType):
    """Contains information about a weapon.

    This d type can be seen as an extension to the corresponding `item`
    object. It contains weapon-specific information and connects the item with
    internal mechanics like fire modes or projectiles.

    """

    _collection = 'weapon'

    def __init__(self, id):
        self.id = id

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
            q = Query(type='weapon_ammo_slot')
            d = q.add_filter(field='weapon_id', value=self.id).get()
            # The following line is not an error, AmmoSlot does not have a
            # list() method as it does not generate any network traffic.
            self._ammo_slot = [AmmoSlot(a) for a in d]
            return self._ammo_slot

    @property
    def attachments(self):
        """Lists the attachments available for this weapon."""
        try:
            return self._attachments
        except AttributeError:
            q = Query(type='weapon_to_attachment')
            d = q.add_filter(field='weapon_id', value=self.id).get()
            self._attachments = Item.list(ids=[i['item_id'] for i in d])
            return self._attachments

    @property
    def fire_groups(self):
        """The fire group used by this weapon."""
        try:
            return self._fire_groups
        except AttributeError:
            q = Query(type='weapon_to_fire_group')
            d = q.add_filter(field='weapon_id', value=self.id).get()
            self._fire_groups = FireGroup.list(
                ids=[f['fire_group_id'] for f in d])
            return self._fire_groups

    @property
    def item(self):
        """Links a weapon to its item."""
        try:
            return self._item
        except AttributeError:
            q = Query(type='item_to_weapon')
            q.add_filter(field='weapon_id', value=self.id)
            q.join(type='item')
            d = q.get_single()
            self._item = Item.get(id=d['item_id'])
            return self._item

    @staticmethod
    def get_by_name(name, locale, ignore_case=True):
        """Allows retrieval of a weapon by its item's name."""
        # Generate request
        if ignore_case:
            q = Query(type='item', check_case=False)
        else:
            q = Query(type='item')
        q.add_filter(field='name.' + locale, value=name)
        q.join(type='item_to_weapon', match='item_id').join(type='weapon',
                                                            match='weapon_id')
        try:
            d = q.get_single()['item_to_weapon']['weapon']
        except TypeError:
            raise NoMatchesFoundError
        # Retrieve and return the object
        instance = Weapon.get(id=d['weapon_id'], data=d)
        return instance

    def _populate(self, data=None):
        d = data if data is not None else super()._get_data(self.id)

        # Set attribute values
        self.equip_time = float(d.get('equip_ms')) / \
            1000.0 if d.get('equip_ms') is not None else None
        self.group_id = d.get('weapon_group_id')
        self.heat_bleed_off_rate = d.get('heat_bleed_off_rate')  # Unit?
        self.heat_capacity = d.get('heat_capacity')
        self.heat_overheat_cooldown = float(d.get(
            'heat_overheat_penalty_ms')) / 1000.0 if d.get(
                'heat_overheat_penalty_ms') is not None else None
        self.iron_sights_enter_ads = float(d.get(
            'to_iron_sights_ms')) / 1000.0 if d.get('to_iron_sights_ms') is not None else None
        self.iron_sights_exit_ads = float(
            d.get('from_iron_sights_ms')) / 1000.0 if d.get(
                'from_iron_sights_ms') is not None else None
        self.melee_detect_height = d.get('melee_detect_height')
        self.melee_detect_width = d.get('melee_detect_width')
        self.move_speed_modifier = d.get('move_modifier')
        self.sprint_recovery = float(d.get(
            'sprint_recovery_ms')) / 1000.0 if d.get('sprint_recovery_ms') is not None else None
        self.turn_speed_modifier = d.get('turn_modifier')
        self.unequip_time = float(
            d.get('unequip_ms')) / 1000.0 if d.get('unequip_ms') is not None else None
