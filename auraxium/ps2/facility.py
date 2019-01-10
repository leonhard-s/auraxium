from ..census import Query
from ..datatypes import InterimDatatype, StaticDatatype
from .faction import Faction
from .zone import Zone

# class Facility(InterimDatatype):
#     _cache_size = 100
#     _collection = 'map_region'


class Region(InterimDatatype):
    _cache_size = 100
    _collection = 'region'

    def __init__(self, id):
        self.id = id
        data = super(Region, self).get_data(self)
        self.initial_faction = Faction(data.get('faction_id'))
        self.name = data.get('name')
        self.zone = Zone(data.get('zone_id'))


class FacilityLink(InterimDatatype):
    _cache_size = 100
    _collection = 'facility_link'

    def __init__(self, id):
        self.id = id
        data = super(FacilityLink, self).get_data(self)
        self.description = data.get('description')
        self.facility_a = Region(data.get('facility_id_a'))
        self.facility_b = Region(data.get('facility_id_b'))
        self.zone = Zone(data.get('zone_id'))


class FacilityType(StaticDatatype):
    _collection = 'facility_type'

    def __init__(self, id):
        self.id = id
        data = super(FacilityType, self).get_data(self)
        self.description = data.get('description')
