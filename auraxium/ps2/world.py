from ..census import Query
from ..datatypes import StaticDatatype


class Server(StaticDatatype):
    _collection = 'world'

    def __init__(self, id, data_override=None):
        self.id = id

        if super().is_cached(self):  # If the object is cached, skip
            return

        data = data_override if data_override != None else super().get_data(self)

        self.name = data.get('name')

        @property
        def status(self):
            # perform request to get current state
            pass

        super()._add_to_cache(self)  # Cache this instance for future use

    def __str__(self):
        return 'Server (ID: {}, Name[en]: "{}")'.format(
            self.id, self.name['en'])
