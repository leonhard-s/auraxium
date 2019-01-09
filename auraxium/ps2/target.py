from ..census import Query
from ..datatypes import StaticDatatype


class TargetType(StaticDatatype):
    _collection = 'target_type'

    def __init__(self, id):
        self.id = id

        data = Query(self.__class__, id=id).get_single()
        self.description = data['description']
