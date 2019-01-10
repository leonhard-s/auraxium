from ..census import Query
from ..datatypes import InterimDatatype


class Title(InterimDatatype):
    _collection = 'title'

    def __init__(self, id):
        self.id = id
        data = super(Title, self).get_data(self)
        self.name = data.get('name')
