from ..datatypes import CachableDataType, EnumeratedDataType
from .faction import Faction
from ..misc import LocalizedString
from .zone import Zone


class Region(CachableDataType):
    """A capturable territory.

    A region (aka. facility or base) is a capturable area of the map belonging
    to a faction.

    """

    def __init__(self, id):
        self.id = id

        # Set default values
        self._initial_faction_id = None
        self.name = None
        self._zone_id = None

        # Define properties
        @property
        def initial_faction(self):
            try:
                return self._initial_faction
            except AttributeError:
                self._initial_faction = Faction.get(cls=self.__class__,
                                                    id=self._initial_faction_id)
                return self._initial_faction

        @property
        def zone(self):
            try:
                return self._zone
            except AttributeError:
                self._zone = Zone.get(cls=self.__class__, id=self._zone_id)
                return self._zone

    def _populate(self, data=None):
        d = data if data != None else super()._get_data(self.id)

        # Set attribute values
        self._initial_faction_id = d.get('initial_faction_id')
        self.name = LocalizedString(d['name'])
        self._zone_id = Zone(d['zone_id'])


class FacilityLink(CachableDataType):
    """Links two facilities on the map to each other.

    Also known as a lattice link, this data type describes whether two
    facilities are connected and whether one can be attacked from the other.

    """

    _collection = 'facility_link'

    def __init__(self, id):
        self.id = id

        # Set default values
        self.description = None
        self._facility_a_id = None
        self._facility_b_id = None
        self._zone_id = None

        # Define properties
        @property
        def facility_a(self):
            try:
                return self._facility_a
            except AttributeError:
                self._facility_a = Region.get(cls=self.__class__,
                                              id=self._facility_a_id)
                return self._facility_a

        @property
        def facility_b(self):
            try:
                return self._facility_b
            except AttributeError:
                self._facility_b = Region.get(cls=self.__class__,
                                              id=self._facility_b_id)
                return self._facility_b

        @property
        def zone(self):
            try:
                return self._zone
            except AttributeError:
                self._zone = Zone.get(cls=self.__class__, id=self._zone_id)
                return self._zone

    def _populate(self, data=None):
        d = data if data != None else super()._get_data(self.id)

        # Set attribute values
        self.description = d['description']
        self._facility_a_id = d['facility_id_a']
        self._facility_b_id = d['facility_id_b']
        self._zone_id = d['zone_id']


class FacilityType(EnumeratedDataType):
    """A type of facility.

    Examples are "Tech Plant", "Bio Lab" or "Small Outpost".

    """

    def __init__(self, id):
        self.id = id

        # Set default values
        self.description = None

    def _populate(self, data=None):
        d = data if data != None else super()._get_data(self.id)

        # Set attribute values
        self.description = d['description']
