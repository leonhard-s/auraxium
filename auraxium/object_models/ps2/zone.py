"""Defines zone-related data types for PlanetSide 2."""

from typing import List
from ..datatypes import DataType, NamedDataType
from ..misc import LocalizedString
from ..typing import Param

from .ability import Ability


class Zone(DataType, NamedDataType):
    """A zone in PS2.

    A zone is a continent such as Indar, Amerish or Hossin.

    """

    _collection = 'zone'

    def __init__(self, id_):
        self.id_ = id_

        # Set default values
        self.code = None
        self.description = None
        self.hex_size = None
        self.name = None

    def populate(self, data=None):
        data_dict = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self.code = data_dict['code']
        self.description = LocalizedString(data_dict.get('description'))
        self.hex_size = data_dict.get('hex_size')
        self.name = LocalizedString(data_dict.get('name'))


class ZoneEffect(DataType):
    """A zone effect.

    An zone reward effect.

    """

    _collection = 'zone_effect'

    def __init__(self, id_):
        self.id_ = id_

        # Set default values
        self._ability_id = None
        self._zone_effect_type_id = None

        self.param: List[Param] = [None for i in range(14)]
        self.string: List[str] = [None for i in range(4)]

    # Define properties
    @property
    def ability(self):
        """The ability of the zone effect."""
        return Ability.get(id_=self._ability_id)

    @property
    def zone_effect_type(self):
        """The type of zone effect."""
        return ZoneEffectType.get(id_=self._zone_effect_type_id)

    def populate(self, data=None):
        data_dict = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self._ability_id = data_dict.get('ability_id')
        self._zone_effect_type_id = data_dict['zone_effect_type_id']

        self.param = [data_dict['param' + str(i + 1)] if data_dict.get('param' + str(i + 1))
                      is not None else None for i in range(13)]
        self.string = [data_dict['string' + str(i + 1)] if data_dict.get('string' + str(i + 1))
                       is not None else None for i in range(4)]


class ZoneEffectType(DataType):
    """A zone effect type.

    A type of zone effect. The effect type's "param" and "string" fields
    contain information about the effect's values purpose.

    """

    _collection = 'zone_effect_type'

    def __init__(self, id_):
        self.id_ = id_

        # Set default values
        self.description = None

        self.param: List[Param] = [None for i in range(14)]
        self.string: List[str] = [None for i in range(4)]

    def populate(self, data=None):
        data_dict = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self.description = data_dict.get('description')

        self.param = [data_dict['param' + str(i + 1)] if data_dict.get('param' + str(i + 1))
                      is not None else None for i in range(13)]
        self.string = [data_dict['string' + str(i + 1)] if data_dict.get('string' + str(i + 1))
                       is not None else None for i in range(4)]
