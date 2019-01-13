from ..census import Query
from ..datatypes import InterimDatatype


class Title(InterimDatatype):
    _collection = 'title'

    def __init__(self, id, data_override=None):
        self.id = id

        if super().is_cached(self):  # If the object is cached, skip
            return

        if self.id == 0:
            self.name = '(No title)'
        else:
            data = data_override if data_override != None else super().get_data(self)
            self.name = data.get('name')

        super()._add_to_cache(self)  # Cache this instance for future use

    def __str__(self):
        return 'Title (ID: {}, Name[en]: "{}")'.format(
            self.id, self.name['en'])
