from ..census import Query
from ..datatypes import InterimDatatype, StaticDatatype

# from .zone import Zone


class FacilityLink(InterimDatatype):
    _cache_size = 100
    _collection = 'facility_link'

    def __init__(self, id):
        self.id = id

        data = Query(self.__cache__, id=id).get_single()

        self.description = data['description']
        # self.facility_a = Facility(data['facility_id_a'])
        # self.facility_b = Facility(data['facility_id_b'])
        # self.zone = Zone(data['zone_id'])
        pass


class FacilityType(StaticDatatype):
    _collection = 'facility_type'

    def __init__(self, id):
        self.id = id

        data = Query(self.__cache__, id=id).get_single()

        self.description = data['description']
