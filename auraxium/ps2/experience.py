from ..census import Query
from ..datatypes import InterimDatatype


class Experience(InterimDatatype):
    _cache_size = 100
    _collection = 'experience'

    def __init__(self, id):
        self.id = id
        data = super(Experience, self).get_data(self)
        self.amount = data.get('xp')
        self.description = data.get('description')

    def __str__(self):
        return 'Experience (ID: {}, Description: "{}")'.format(
            self.id, self.description)
