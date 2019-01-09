from ..census import Query
from ..datatypes import InterimDatatype, StaticDatatype


class ResourceType(StaticDatatype):
    _collection = 'resource_type'

    def __init__(self, id):
        self.id = id
        data = super(ResourceType, self).get_data(self)

        self.description = data['description']
