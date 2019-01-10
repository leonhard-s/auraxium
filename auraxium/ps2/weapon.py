from ..census import Query
from ..datatypes import InterimDatatype, StaticDatatype
from .item import Item
# from .playerstate import PlayerStateGroup
from .resist import ResistType
from .target import TargetType


class FireGroup(InterimDatatype):
    _cache_size = 100
    _collection = 'fire_group'

    def __init__(self, id):
        self.id = id
        data = super(FireGroup, self).get_data(self)

        self.chamber_duration_ms = data.get('chamber_duration_ms')
        self.transition_duration_ms = data.get('transition_duration_ms')
        self.spool_up_ms = data.get('spool_up_ms')
        self.spool_up_initial_refire_ms = data.get(
            'spool_up_initial_refire_ms')
        self.can_chamber_ironsights = data.get('can_chamber_ironsights')


class FireMode():
    _cache_size = 250
    _collection = 'fire_mode'

    def __init__(self, id):
        self.id = id
        data = super(FireGroup, self).get_data(self)

        self.item = Item(data.get('item_id'))
        self.type = FireModeType(data.get('type'))
        self.description = data.get('description')
        self.player_state_group = PlayerStateGroup(
            data.get('player_state_group_id'))
        self.cof_recoil = data.get('cof_recoil')
        self.reload_time_ms = data.get('reload_time_ms')
        self.reload_chamber_time_ms = data.get('reload_chamber_time_ms')
        self.pellets_per_shot = data.get('pellets_per_shot')
        self.pellet_spread = data.get('pellet_spread')
        self.default_zoom = data.get('default_zoom')
        self.muzzle_velocity = data.get('muzzle_velocity')
        self.speed = data.get('speed')
        self.max_speed = data.get('max_speed')
        self.damage_radius = data.get('damage_radius')
        self.projectile_description = data.get('projectile_description')
        self.damage_type = data.get('damage_type')
        self.damage = data.get('damage')
        self.damage_min = data.get('damage_min')
        self.damage_max = data.get('damage_max')
        self.damage_min_range = data.get('damage_min_range')
        self.damage_max_range = data.get('damage_max_range')
        self.damage_target_type = TargetType(data.get('damage_target_type'))
        self.damage_resist_type = ResistType(data.get('damage_resist_type'))
        self.indirect_damage_max = data.get('indirect_damage_max')
        self.indirect_damage_max_range = data.get('indirect_damage_max_range')
        self.indirect_damage_min = data.get('indirect_damage_min')
        self.indirect_damage_min_range = data.get('indirect_damage_min_range')
        self.indirect_damage_target_type = TargetType(
            data.get('indirect_damage_target_type'))
        self.indirect_damage_resist_type = ResistType(
            data.get('indirect_damage_resist_type'))


class FireModeType(StaticDatatype):
    _collection = 'fire_mode_type'

    def __init__(self, id):
        self.id = id
        data = super(FireModeType, self).get_data(self)
        self.description = data.get('description')


class Weapon(InterimDatatype):
    _cache_size = 500
    _collection = 'weapon'

    def __init__(self, id):
        self.id = id
        data = super(Weapon, self).get_data(self)

        self.ammo = WeaponAmmoSlot(data.get('weapon_ammo_slot'))
        self.turn_modifier = data.get('turn_modifier')
        self.move_modifier = data.get('move_modifier')
        self.sprint_recovery_ms = data.get('sprint_recovery_ms')
        self.equip_ms = data.get('equip_ms')
        self.unequip_ms = data.get('unequip_ms')
        self.to_iron_sights_ms = data.get('to_iron_sights_ms')
        self.from_iron_sights_ms = data.get('from_iron_sights_ms')
        self.heat_capacity = data.get('heat_capacity')
        self.heat_bleed_off_rate = data.get('heat_bleed_off_rate')
        self.heat_overheat_penalty_ms = data.get('heat_overheat_penalty_ms')
        self.melee_detect_width = data.get('melee_detect_width')
        self.melee_detect_height = data.get('melee_detect_height')

        # I was unable to find any rhyme or reason to the assignment of
        # weapon groups. I omitted them for the time being.
        # self.group = data.get('weapon_group_id')

        @property
        def attachments(self):
            pass

        @property
        def fire_group(self):
            pass


class WeaponAmmoSlot(InterimDatatype):
    _cache_size = 500
    _collection = 'weapon_ammo_slot'

    def __init__(self, id):
        self.id = id
        data = super(WeaponAmmoSlot, self).get_data(self)

        self.capacity = data.get('capacity')
        self.clip_size = data.get('clip_size')
        self.refill_ammo_rate = data.get('refill_ammo_rate')
        self.refill_ammo_delay_ms = data.get('refill_ammo_delay_ms')
        self.weapon_slot_index = data.get('weapon_slot_index')


class WeaponDatasheet(InterimDatatype):
    _cache_size = 500
    _collection = 'weapon_datasheet'

    def __init__(self, id):
        self.id = id
        data = super(WeaponDatasheet, self).get_data(self)

        self.item_id = data.get('item_id')
        self.direct_damage = data.get('direct_damage')
        self.indirect_damage = data.get('indirect_damage')
        self.damage = data.get('damage')
        self.damage_min = data.get('damage_min')
        self.damage_max = data.get('damage_max')
        self.fire_cone = data.get('fire_cone')
        self.fire_cone_min = data.get('fire_cone_min')
        self.fire_cone_max = data.get('fire_cone_max')
        self.fire_rate_ms = data.get('fire_rate_ms')
        self.fire_rate_ms_min = data.get('fire_rate_ms_min')
        self.fire_rate_mx_max = data.get('fire_rate_mx_max')
        self.reload_ms = data.get('reload_ms')
        self.reload_ms_min = data.get('reload_ms_min')
        self.reload_ms_max = data.get('reload_ms_max')
        self.clip_size = data.get('clip_size')
        self.capacity = data.get('capacity')
        self.range = data.get('range')
        self.show_clip_size = data.get('show_clip_size')
        self.show_fire_modes = data.get('show_fire_modes')
        self.show_range = data.get('show_range')
