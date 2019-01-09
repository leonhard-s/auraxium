from ..census import Query
from ..datatypes import InterimDatatype


class Experience(InterimDatatype):
    _cache_size = 100
    _collection = 'experience'

    def __init__(self, id):
        self.id = id

        data = Query(self.__cache__, id=id).get_single()

        self.description = data['description']
        self.amount = int(data['xp'])
