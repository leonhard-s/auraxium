from ..census import Query
from ..datatypes import InterimDatatype, StaticDatatype


class Ability(InterimDatatype):
    """An ability in PlanetSide 2.

    I was unable to find proper names for any of the abilities. It's possible
    that the name can only be inferred using the corresponding skill
    (certification).

    """

    _collection = 'ability'

    def __init__(self, id, data_override=None):
        self.id = id
        data = super(Ability, self).get_data(self)

        self.type = AbilityType(data['ability_type_id'])  # ability_type_id
        self.expire_msec = data.get('expire_msec')
        self.first_use_delay_msec = data.get('first_use_delay_msec')
        self.next_use_delay_msec = data.get('next_use_delay_msec')
        self.reuse_delay_msec = data.get('reuse_delay_msec')
        self.resource_type = ResourceType(
            data['resource_type']) if 'resource_type' in data.keys() else None
        self.resource_first_cost = data.get('resource_first_cost')
        self.resource_cost_per_msec = data.get('resource_cost_per_msec')
        self.distance_max = data.get('distance_max')
        self.radius_max = data.get('radius_max')
        self.flag_toggle = data.get('flag_toggle')

        self.parameters = {}
        self.strings = {}
        for i in range(14):
            try:
                self.parameters[i] = data['param{}'.format(i + 1)]
                self.string[i] = data['string{}'.format(i + 1)]
            except KeyError:
                pass


class AbilityType(StaticDatatype):
    """Represents a type of ability.

    The 'parameters_*' and 'string_*' attributes contain descriptions of the
    attributes for the corresponding ability.

    """

    _collection = 'ability_type'

    def __init__(self, id):
        self.id = id
        data = super(AbilityType, self).get_data(self)

        self.description = data.get('description', '')

        self.parameters = {}
        self.strings = {}
        for i in range(14):
            try:
                self.parameters[i] = data['param{}'.format(i + 1)]
                self.string[i] = data['string{}'.format(i + 1)]
            except KeyError:
                pass
