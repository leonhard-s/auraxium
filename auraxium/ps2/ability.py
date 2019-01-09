from enum import Enum

from ..census import Query
from ..datatypes import InterimDatatype, StaticDatatype


class Ability(InterimDatatype):
    """An ability in PlanetSide 2.

    I was unable to find proper names for any of the abilities. It's possible
    that the name can only be inferred using the corresponding skill
    (certification).

    """

    _collection = 'ability'

    def __init__(self, id):
        self.id = id  # ability_id

        data = Query(self.__class__, id=id).get_single()

        self.type = AbilityType(data['ability_type_id'])  # ability_type_id

        # Remove the used fields from the data dictionary
        del data['ability_id']
        del data['ability_type_id']

        # Iterate over the remaining entries
        for k in data.keys():
            # If the key is one of the parameters
            if not k.startswith('param') and not k.startswith('string'):
                # Add it as an attribute
                exec('self.{} = None if data[k] == ''\'NULL\' '
                     'else data[k]'.format(k))

        self.parameters = {}
        self.strings = {}

        data = Query(self.__class__, id=id).get_single()
        del data['ability_type_id']

        for i in range(14):
            try:
                self.parameters[i] = data['param{}'.format(i + 1)]
                self.string[i] = data['string{}'.format(i + 1)]
            except KeyError:
                pass

        print(self.__dict__)


class AbilityType(StaticDatatype):
    """Represents a type of ability.

    The 'parameters_*' and 'string_*' attributes contain descriptions of the
    attributes for the corresponding ability.

    """

    _collection = 'ability_type'

    def __init__(self, id):
        self.id = id

        self.description = ''
        self.parameters = {}
        self.strings = {}

        data = Query(self.__class__, id=id).get_single()
        del data['ability_type_id']

        for i in range(14):
            try:
                self.parameters[i] = data['param{}'.format(i + 1)]
                self.string[i] = data['string{}'.format(i + 1)]
            except KeyError:
                pass

        print(self.__dict__)
