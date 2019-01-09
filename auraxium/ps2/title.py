from ..census import Query
from ..datatypes import InterimDatatype


class Title(InterimDatatype):
    _collection = 'title'

    def __init__(self, id):
        self.id = id

        data = Query(self.__class__, id=id).get_single()
        self.name = data['name'][next(iter(data['name']))]
