from ..census import Query
from ..datatypes import CachableDataType, EnumeratedDataType
from .item import Item
from .projectile import Projectile


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

    def __init__(self, id):
        self.id = id

        # Set default values
        self.chamber_duration = None
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
            self._fire_modes = FireMode.list(ids=[i['fire_mode_id'] for i in d])
            return self._fire_modes

    def _populate(self, data=None):
        d = data if data != None else super()._get_data(self.id)

        # Set attribute values
        self.chamber_duration = float(d.get(
            'chamber_duration_ms')) / 1000.0 if d.get('chamber_duration_ms') is not None else None
        self.transition_duration = d.get('transition_duration_ms') / 100
        self.spool_up = float(d.get('spool_up_ms')) / \
            1000.0 if d.get('spool_up_ms') is not None else None
        self.spool_up_initial_refire = d.get(
            'spool_up_initial_refire_ms') / 1000
        self.can_chamber_ironsights = d.get('can_chamber_ironsights')


class FireMode(CachableDataType):
    """A weapon fire mode.

    A fire mode contains detailed information about the how the firing
    mechanics of the weapons using it operate.
    This object contains the merged information from the "fire_mode" and
    "fire_mode_2" collections.

    """

    def __init__(self, id, data=None):
        self.id = id

        # Set default values

        # "item_id": "2"
        self.type = None
        self.description = None
        self.player_state_group_id = None  # property
        self.cof_recoil = None
        self.reload_time = None  # reload_time_ms
        self.reload_chamber_time = None  # reload_chamber_time_ms
        self.pellets_per_shot = None
        self.pellets_spread = None
        self.iron_sight_zoom = None  # default_zoom
        # "muzzle_velocity": "375",
        # "speed": "375",
        # "max_speed": "0",
        # "damage_radius": "0",
        # "projectile_description": "NC Pistol: Mid",
        # "damage_type": "DamageFalloff",
        # "damage": "NULL",
        # "damage_min": "112",
        # "damage_max": "200",
        # "damage_min_range": "60",
        # "damage_max_range": "10",
        # "damage_target_type": "2",
        # "damage_resist_type": "2",
        # "indirect_damage_max": "NULL",
        # "indirect_damage_max_range": "NULL",
        # "indirect_damage_min": "NULL",
        # "indirect_damage_min_range": "NULL",
        # "indirect_damage_target_type": "NULL",
        # "indirect_damage_resist_type": "NULL""fire_mode_id": "102",
        self.fire_mode_type_id = None  # fire_mode_type_id
        self.ability_id = None  # ability_id
        # self.ammo_slot
        # "automatic": "0",
        # "grief_immune": "0",
        # "iron_sights": "1",
        self.laser_guided = None
        # self.mode_speed_modifier = None # move_modifier
        # "projectile_speed_override": "375",
        self.can_fire_while_sprinting = None  # sprint_fire
        # "turn_modifier": "1",
        # "use_in_water": "0",
        # "zoom_default": "1.3500000000000001",
        # "cof_override": "0",
        # "cof_pellet_spread": "0",
        # "cof_range": "100",
        # "cof_recoil": "0.14",
        # "cof_scalar": "1",
        # "cof_scalar_moving": "1",
        # "damage_direct_effect_id": "13",
        self.headshot_multiplier = None
        self.damage_indirect_effect_id = None
        self.legshot_multiplier = None  # damage_legs_multiplier
        self.ammo_per_shot = None
        self.auto_fire = None
        # "fire_auto_fire_ms": "0",
        # "fire_burst_count": "1",
        # "fire_charge_up_ms": "0",
        # "fire_delay_ms": "0",
        # "fire_detect_range": "40",
        # "fire_duration_ms": "NULL",
        # "fire_refire_ms": "171",
        # "fire_pellets_per_shot": "1",
        # "heat_per_shot": "NULL",
        # "heat_recovery_delay_ms": "NULL",
        # "heat_threshold": "NULL",
        # "lockon_acquire_close_ms": "NULL",
        # "lockon_acquire_far_ms": "NULL",
        # "lockon_acquire_ms": "NULL",
        # "lockon_angle": "NULL",
        # "lockon_lose_ms": "NULL",
        # "lockon_maintain": "NULL",
        # "lockon_radius": "NULL",
        # "lockon_range": "NULL",
        # "lockon_range_close": "NULL",
        # "lockon_range_far": "NULL",
        # "lockon_required": "NULL",
        # "recoil_angle_max": "0",
        # "recoil_angle_min": "0",
        # "recoil_first_shot_modifier": "1",
        # "recoil_horizontal_max": "0.10000000000000001",
        # "recoil_horizontal_max_increase": "NULL",
        # "recoil_horizontal_min": "0.10000000000000001",
        # "recoil_horizontal_min_increase": "NULL",
        # "recoil_horizontal_tolerance": "0.29999999999999999",
        # "recoil_increase": "0",
        # "recoil_increase_crouched": "0",
        # "recoil_magnitude_max": "0.80000000000000004",
        # "recoil_magnitude_min": "0.80000000000000004",
        # "recoil_max_total_magnitude": "0",
        # "recoil_recovery_acceleration": "1000",
        # "recoil_recovery_delay_ms": "0",
        # "recoil_recovery_rate": "18",
        # "recoil_shots_at_min_magnitude": "0",
        # "reload_block_auto": "NULL",
        # "reload_continuous": "NULL",
        # "reload_ammo_fill_ms": "1425",
        # "reload_chamber_ms": "300",
        # "reload_loop_start_ms": "NULL",
        # "reload_loop_end_ms": "NULL",
        # "reload_time_ms": "1600",
        # "sway_amplitude_x": "NULL",
        # "sway_amplitude_y": "NULL",
        # "sway_can_steady": "NULL",
        # "sway_period_x": "NULL",
        # "sway_period_y": "NULL",
        # "armor_penetration": "0",
        # "max_damage": "200",
        # "max_damage_ind": "NULL",
        # "max_damage_ind_radius": "NULL",
        # "max_damage_range": "10",
        # "min_damage": "112",
        # "min_damage_ind": "NULL",
        # "min_damage_ind_radius": "NULL",
        # "min_damage_range": "60",
        # "shield_bypass_pct": "0",
        # "description"

    # Define properties
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


class FireModeType(EnumeratedDataType):
    """The fire mode type for a given fire mode.

    Fire mode types provide a basic classification of how a given weapon
    operates.
    Examples are "Melee", "Projectile" and "Trigger Item Ability".

    """

    def __init__(self, id):
        self.id = id

        # Set default values
        self.description = None

    def _populate(self, data=None):
        d = data if data != None else super()._get_data(self.id)

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
        self.equip_time = None
        self.group_id = None
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

    @property
    def fire_group(self):
        """The fire group used by this weapon."""
        try:
            return self._fire_group
        except AttributeError:
            q = Query(type='weapon_to_fire_group')
            d = q.add_filter(field='weapon_id', value=self.id).get()
            self._fire_group = FireGroup.list(ids=[f['fire_group_id'] for f in d])
            return self._fire_group

    def _populate(self, data=None):
        d = data if data != None else super()._get_data(self.id)

        # Set attribute values
        self.equip_time = float(d.get('equip_ms')) / \
            1000.0 if d.get('equip_ms') is not None else None
        self.group_id = d.get('weapon_group_id')
        self.heat_bleed_off_rate = d.get('heat_bleed_off_rate')  # Unit?
        self.heat_capacity = d.get('heat_capacity')
        self.heat_overheat_cooldown = float(d.get(
            'heat_overheat_penalty_ms')) / 1000.0 if d.get('heat_overheat_penalty_ms') is not None else None
        self.iron_sights_enter_ads = float(d.get(
            'to_iron_sights_ms')) / 1000.0 if d.get('to_iron_sights_ms') is not None else None
        self.iron_sights_exit_ads = float(
            d.get('from_iron_sights_ms')) / 1000.0 if d.get('from_iron_sights_ms') is not None else None
        self.melee_detect_height = d.get('melee_detect_height')
        self.melee_detect_width = d.get('melee_detect_width')
        self.move_speed_modifier = d.get('move_modifier')
        self.sprint_recovery = float(d.get(
            'sprint_recovery_ms')) / 1000.0 if d.get('sprint_recovery_ms') is not None else None
        self.turn_speed_modifier = d.get('turn_modifier')
        self.unequip_time = float(
            d.get('unequip_ms')) / 1000.0 if d.get('unequip_ms') is not None else None
