from ..census import Query
from ..datatypes import CachableDataType, EnumeratedDataType


class ResistInfo(CachableDataType):
    """A resist info entry.

    Resist info contains information about how resistant an entity is to certain
    types of damage.

    """

    _collection = 'resist_info'

    def __init__(self, id):
        self.id = id

        # Set default values
        self.description = None
        self.headshot_multiplier = None
        self.percent = None
        self._resist_type_id = None

        # Define properties
        @property
        def resist_type(self):
            try:
                return self._resist_type
            except AttributeError:
                self._resist_type = ResistType.get(cls=self.__class__,
                                                   id=self._resist_type_id)
                return self._resist_type

    def _populate(self, data=None):
        d = data if data != None else super()._get_data(self.id)

        # Set attribute values
        self.description = d.get('description')

        self.description = d['description']
        self.headshot_multiplier = d.get('multiplier_when_headshot')
        self.percent = d['resist_percent']
        self._resist_type_id = d.get('resist_type_id')


class ResistType(EnumeratedDataType):
    """A resist type.

    A type of damage for which resistance information might exist.
    Examples include "Heavy Machine Gun" or "Explosive".

    """

    _collection = 'resist_type'

    def __init__(self, id):
        self.id = id

        # Set default values
        self.description = None

        def _populate(self, data=None):
            d = data if data != None else super()._get_data(self.id)

            # Set attribute values
            self.description = d['description']
