from ..datatypes import CachableDataType, EnumeratedDataType
from .resource import ResourceType


class Ability(CachableDataType):
    """A PS2 Ability.

    Abilities are persistent, player-bound objects responsible for persistent
    effects like AoE heal or the Heavy Assault's overshield. They are
    generally bound to a resource that is drained as the ability is used.

    """

    _collection = 'ability'

    def __init__(self, id):
        self.id = id

        # Set default values
        self._ability_type_id = None
        self.distance_max = None
        self.expires_after = None
        self.first_use_delay = None
        self.is_toggle = None
        self.next_use_delay = None
        self.radius_max = None
        self.resource_cast_cost = None
        self.resource_cost = None
        self._resource_type_id = None
        self.reuse_delay = None
        # Set default values for fields "param1" through "param14"
        s = ''
        for i in range(14):
            s += 'self.param{0} = None\n'.format(i + 1)
        exec(s)
        # Set default values for fields "string1" through "string4"
        s = ''
        for i in range(4):
            s += 'self.string{0} = None\n'.format(i + 1)
        exec(s)

    # Define properties
    @property
    def ability_type(self):
        return AbilityType.get(id=self._ability_type_id)

    @property
    def resource_type(self):
        return ResourceType.get(id=self._resource_type_id)

    def _populate(self, data=None):
        d = data if data is not None else super()._get_data(self.id)

        # Set attribute values
        self._ability_type_id = d.get('ability_type_id')
        self.distance_max = d.get('distance_max')
        self.expires_after = float(
            d.get('expire_msec')) / 1000.0 if d.get('expire_msec') is not None else None
        self.first_use_delay = float(d.get('first_use_delay_msec')) / \
            1000.0 if d.get(
                'first_use_delay_msec') is not None else None
        self.is_toggle = d.get('flag_toggle')
        self.next_use_delay = float(d.get('next_use_delay_msec')) / \
            1000.0 if d.get(
                'next_use_delay_msec') is not None else None
        self.radius_max = d.get('radius_max')
        self.resource_cast_cost = d.get('resource_first_cost')
        self.resource_cost = float(d.get('resource_cost_per_msec')) / \
            1000.0 if d.get(
                'resource_cost_per_msec') is not None else None
        self._resource_type_id = d.get('resource_type_id')
        self.reuse_delay = float(d.get('reuse_delay_msec')) / \
            1000.0 if d.get('reuse_delay_msec') is not None else None
        # Set attributes "param1" through "param14"
        s = ''
        for i in range(14):
            s += 'self.param{0} = d.get(\'param{0}\')\n'.format(i + 1)
        exec(s)
        # Set attributes "string1" through "string4
        s = ''
        for i in range(4):
            s += 'self.string{0} = d.get(\'string{0}\')\n'.format(i + 1)
        exec(s)


class AbilityType(EnumeratedDataType):
    """Represents a type of ability.

    Groups similarly functioning abilities together, the "param" and "string"
    fields of an ability type also explain the (unnamed) entries for the
    corresponding abilities.

    """

    _collection = 'ability_type'

    def __init__(self, id):
        self.id = id

        self.description = None
        # Set default values for fields "param1" through "param14"
        s = ''
        for i in range(14):
            s += 'self.param{0} = None\n'.format(i + 1)
        exec(s)
        # Set default values for fields "string1" through "string4"
        s = ''
        for i in range(4):
            s += 'self.string{0} = None\n'.format(i + 1)
        exec(s)

    def _populate(self, data=None):
        d = data if data is not None else super()._get_data(self.id)

        # Set attribute values
        self.description = d.get('description')
        # Set attributes "param1" through "param14"
        s = ''
        for i in range(14):
            s += 'self.param{0} = d.get(\'param{0}\')\n'.format(i + 1)
        exec(s)
        # Set attributes "string1" through "string4
        s = ''
        for i in range(4):
            s += 'self.string{0} = d.get(\'string{0}\')\n'.format(i + 1)
        exec(s)
