from ..census import Query
from ..datatypes import InterimDatatype


class Experience(InterimDatatype):
    _cache_size = 100
    _collection = 'experience'

    def __init__(self, id):
        self.id = id
        data = super(Experience, self).get_data(self)

        self.description = data['description']
        self.amount = int(data['xp'])
