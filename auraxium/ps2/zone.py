from ..census import Query
from ..datatypes import InterimDatatype, StaticDatatype
from .ability import Ability


class Zone(StaticDatatype):
    _collection = 'zone'

    def __init__(self, id):
        self.id = id
        data = super(Zone, self).get_data(self)
        self.code = data.get('code')
        self.description = data.get('description')
        self.hex_size = data.get('hex_size')
        self.name = data.get('name')


class ZoneEffect(InterimDatatype):
    _cache_size = 100
    _collection = 'zone_effect'

    def __init__(self, id):
        self.id = id
        data = super(ZoneEffect, self).get_data(self)
        self.ability = Ability(data.get('ability_id'))
        self.type = ZoneEffectType(data.get('zone_effect_type_id'))

        self.parameters = {}
        self.strings = {}
        for i in range(14):
            self.parameters[i] = data.get('param{}'.format(i + 1))
            self.string[i] = data.get('string{}'.format(i + 1))


class ZoneEffectType(StaticDatatype):
    _collection = 'zone_effect_type'

    def __init__(self, id):
        self.id = id
        data = super(ZoneEffectType, self).get_data(self)
        self.description = data.get('description')

        self.parameters = {}
        self.strings = {}
        for i in range(14):
            self.parameters[i] = data.get('param{}'.format(i + 1))
            self.string[i] = data.get('string{}'.format(i + 1))
