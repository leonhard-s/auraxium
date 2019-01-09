from ..census import Query
from ..datatypes import InterimDatatype, StaticDatatype


class FireGroup():
    pass


class FireMode():
    pass


class FireModeType(StaticDatatype):
    _collection = 'fire_mode_type'

    def __init__(self, id=id):
        self.id = id

        data = Query(self.__class__, id=id).get_single()
        self.description = data['description']


class Weapon(InterimDatatype):
    _cache_size = 500
    _collection = 'weapon'

    def __init__(self, id=id):
        self.id = id

        data = Query(self.__class__, id=id).get_single()
        self.group = int(data['weapon_group_id'])
        self.turn_modifier = float(data['turn_modifier'])
        self.move_modifier = float(data['move_modifier'])
        self.sprint_recovery_ms = int(data['sprint_recovery_ms'])
        self.equip_ms = int(equip_ms)
        self.unequip_ms = int(unequip_ms)
        self.to_iron_sights_ms = int(to_iron_sights_ms)
        self.from_iron_sights_ms = int(from_iron_sights_ms)
        self.heat_capacity = float(heat_capacity)
        self.heat_bleed_off_rate = float(heat_bleed_off_rate)
        self.heat_overheat_penalty_ms = int(heat_overheat_penalty_ms)
        self.melee_detect_width = float(melee_detect_width)
        self.melee_detect_height = float(melee_detect_height)

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

        data = Query(self.__class__, id=id).get_single()
        self.capacity = int(data['capacity'])
        self.clip_size = int(data['clip_size'])
        self.refill_ammo_rate = int(data['refill_ammo_rate'])
        self.refill_ammo_delay_ms = int(data['refill_ammo_delay_ms'])
        self.weapon_slot_index = int(data['weapon_slot_index'])


class WeaponDatasheet(InterimDatatype):
    _cache_size = 500
    _collection = 'weapon_datasheet'

    def __init__(self, id):
        self.id = id

        data = Query(self.__class__, id=id).get_single()
        self.item_id = data['item_id']
        self.direct_damage = data['direct_damage']
        self.indirect_damage = data['indirect_damage']
        self.damage = data['damage']
        self.damage_min = data['damage_min']
        self.damage_max = data['damage_max']
        self.fire_cone = data['fire_cone']
        self.fire_cone_min = data['fire_cone_min']
        self.fire_cone_max = data['fire_cone_max']
        self.fire_rate_ms = data['fire_rate_ms']
        self.fire_rate_ms_min = data['fire_rate_ms_min']
        self.fire_rate_mx_max = data['fire_rate_mx_max']
        self.reload_ms = data['reload_ms']
        self.reload_ms_min = data['reload_ms_min']
        self.reload_ms_max = data['reload_ms_max']
        self.clip_size = data['clip_size']
        self.capacity = data['capacity']
        self.range = data['range']
        self.show_clip_size = data['show_clip_size']
        self.show_fire_modes = data['show_fire_modes']
        self.show_range = data['show_range']
