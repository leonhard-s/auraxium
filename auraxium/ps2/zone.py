from ..census import Query
from ..datatypes import CachableDataType, EnumeratedDataType, NamedDataType
from .ability import Ability
from ..misc import LocalizedString


class Zone(EnumeratedDataType, NamedDataType):
    """A zone in PS2.

    A zone is a continent such as Indar, Amerish or Hossin.

    """

    _collection = 'zone'

    def __init__(self, id):
        self.id = id

        # Set default values
        self.code = None
        self.description = None
        self.hex_size = None
        self.name = None

    def _populate(self, data=None):
        d = data if data != None else super()._get_data(self.id)

        # Set attribute values
        self.code = d['code']
        self.description = LocalizedString(d.get('description'))
        self.hex_size = d.get('hex_size')
        self.name = LocalizedString(d.get('name'))


class ZoneEffect(CachableDataType):
    """A zone effect.

    An zone reward effect.

    """

    _collection = 'zone_effect'

    def __init__(self, id):
        self.id = id

        # Set default values
        self._ability_id = None
        self._zone_effect_type_id = None
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
    def ability(self):
        try:
            return self._ability
        except AttributeError:
            self._ability = Ability.get(id=self._ability_id)
            return self._ability

    @property
    def zone_effect_type(self):
        try:
            return self._zone_effect_type
        except AttributeError:
            self._zone_effect_type = ZoneEffectType.get(
                id=self._zone_effect_type_id)
            return self._zone_effect_type

    def _populate(self, data=None):
        d = data if data != None else super()._get_data(self.id)

        # Set attribute values
        self._ability_id = d.get('ability_id')
        self._zone_effect_type_id = d['zone_effect_type_id']
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


class ZoneEffectType(EnumeratedDataType):
    """A zone effect type.

    A type of zone effect. The effect type's "param" and "string" fields
    contain information about the effect's values purpose.

    """

    _collection = 'zone_effect_type'

    def __init__(self, id):
        self.id = id

        # Set default values
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
        d = data if data != None else super()._get_data(self.id)

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
