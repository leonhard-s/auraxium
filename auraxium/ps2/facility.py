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
    _join = 'faction'

    def __init__(self, id, data_override=None):
        self.id = id

        if super().is_cached(self):  # If the object is cached, skip
            return

        data = data_override if data_override != None else super().get_data(self)

        self.initial_faction = Faction(
            data.get('faction_id'), data_override=data.get('faction'))
        self.name = data.get('name')
        self.zone = Zone(data.get('zone_id'))

        super()._add_to_cache(self)  # Cache this instance for future use

    def __str__(self):
        return 'Region (ID: {}, Name[en]: "{}")'.format(
            self.id, self.name['en'])


class FacilityLink(InterimDatatype):
    _cache_size = 100
    _collection = 'facility_link'

    def __init__(self, id, data_override=None):
        self.id = id

        if super().is_cached(self):  # If the object is cached, skip
            return

        data = data_override if data_override != None else super().get_data(self)

        self.description = data.get('description')
        self.facility_a = Region(data.get('facility_id_a'))
        self.facility_b = Region(data.get('facility_id_b'))
        self.zone = Zone(data.get('zone_id'))

        super()._add_to_cache(self)  # Cache this instance for future use

    def __str__(self):
        return 'FacilityLink (ID: {}, Description: "{}")'.format(
            self.id, self.description)


class FacilityType(StaticDatatype):
    _collection = 'facility_type'

    def __init__(self, id, data_override=None):
        self.id = id

        if super().is_cached(self):  # If the object is cached, skip
            return

        data = data_override if data_override != None else super().get_data(self)

        self.description = data.get('description')

        super()._add_to_cache(self)  # Cache this instance for future use

    def __str__(self):
        return 'FacilityType (ID: {}, Description: "{}")'.format(
            self.id, self.description)
