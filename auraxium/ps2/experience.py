from ..census import Query
from ..datatypes import InterimDatatype


class Experience(InterimDatatype):
    _cache_size = 100
    _collection = 'experience'

    def __init__(self, id, data_override=None):
        self.id = id

        if super().is_cached(self):  # If the object is cached, skip
            return

        data = data_override if data_override != None else super().get_data(self)

        self.amount = data.get('xp')
        self.description = data.get('description')

        super()._add_to_cache(self)  # Cache this instance for future use

    def __str__(self):
        return 'Experience (ID: {}, Description: "{}")'.format(
            self.id, self.description)
