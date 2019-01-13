from ..census import Query
from ..datatypes import InterimDatatype, StaticDatatype
from .ability import Ability


class Zone(StaticDatatype):
    _collection = 'zone'

    def __init__(self, id, data_override=None):
        self.id = id

        if super().is_cached(self):  # If the object is cached, skip
            return

        data = data_override if data_override != None else super().get_data(self)

        self.code = data.get('code')
        self.description = data.get('description')
        self.hex_size = data.get('hex_size')
        self.name = data.get('name')

        super()._add_to_cache(self)  # Cache this instance for future use

    def __str__(self):
        return 'Zone (ID: {}, Name[en]: "{}")'.format(
            self.id, self.name['en'])


class ZoneEffect(InterimDatatype):
    _cache_size = 100
    _collection = 'zone_effect'
    _join = ['ability', 'zone_effect_type']

    def __init__(self, id, data_override=None):
        self.id = id

        if super().is_cached(self):  # If the object is cached, skip
            return

        data = data_override if data_override != None else super().get_data(self)

        self.ability = Ability(data.get('ability_id'),
                               data_override=data.get('ability'))
        self.type = ZoneEffectType(
            data.get('zone_effect_type_id'), data_override=data.get('zone_effect_type'))

        self.parameters = {}
        self.strings = {}
        for i in range(14):
            self.parameters[i] = data.get('param{}'.format(i + 1))
            self.string[i] = data.get('string{}'.format(i + 1))

        super()._add_to_cache(self)  # Cache this instance for future use

    def __str__(self):
        return 'ZoneEffect (ID: {})'.format(self.id)


class ZoneEffectType(StaticDatatype):
    _collection = 'zone_effect_type'

    def __init__(self, id, data_override=None):
        self.id = id

        if super().is_cached(self):  # If the object is cached, skip
            return

        data = data_override if data_override != None else super().get_data(self)

        self.description = data.get('description')

        self.parameters = {}
        self.strings = {}
        for i in range(14):
            self.parameters[i] = data.get('param{}'.format(i + 1))
            self.string[i] = data.get('string{}'.format(i + 1))

        super()._add_to_cache(self)  # Cache this instance for future use

    def __str__(self):
        return 'ZoneEffectType (ID: {}, Description: "{}")'.format(
            self.id, self.description)
