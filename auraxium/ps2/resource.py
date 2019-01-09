from ..census import Query
from ..datatypes import InterimDatatype, StaticDatatype


class ResourceType(StaticDatatype):
    _collection = 'resource_type'

    def __init__(self, id):
        self.id = id

        data = Query(self.__class__, id=id).get_single()
        self.description = data['description']
