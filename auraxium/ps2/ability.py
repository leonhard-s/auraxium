from ..census import Query
from ..datatypes import InterimDatatype, StaticDatatype


class Ability(InterimDatatype):
    _cache_size = 100
    _collection = 'ability'
    _join = ['ability_type']

    def __init__(self, id, data_override=None):
        self.id = id

        if super().is_cached(self):  # If the object is cached, skip
            return

        data = data_override if data_override != None else super().get_data(self)

        self.type = AbilityType(
            data.get('ability_type_id'), data_override=data.get('ability_type'))
        self.expire_msec = data.get('expire_msec')
        self.first_use_delay_msec = data.get('first_use_delay_msec')
        self.next_use_delay_msec = data.get('next_use_delay_msec')
        self.reuse_delay_msec = data.get('reuse_delay_msec')
        self.resource_type = ResourceType(data.get('resource_type'))
        self.resource_first_cost = data.get('resource_first_cost')
        self.resource_cost_per_msec = data.get('resource_cost_per_msec')
        self.distance_max = data.get('distance_max')
        self.radius_max = data.get('radius_max')
        self.flag_toggle = data.get('flag_toggle')

        self.parameters = {}
        self.strings = {}
        for i in range(14):
            self.parameters[i] = data.get('param{}'.format(i + 1))
            self.string[i] = data.get('string{}'.format(i + 1))

        super()._add_to_cache(self)  # Cache this instance for future use

    def __str__(self):
        return 'Ability (ID: {})'.format(self.id)


class AbilityType(StaticDatatype):
    """Represents a type of ability.

    The 'parameters_*' and 'string_*' attributes contain descriptions of the
    attributes for the corresponding ability.

    """

    _collection = 'ability_type'

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
        return 'AbilityType (ID: {}, Description: "{}")'.format(
            self.id, self.description)
