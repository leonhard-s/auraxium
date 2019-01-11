from ..census import Query
from ..datatypes import StaticDatatype


class Server(StaticDatatype):
    _collection = 'world'

    def __init__(self, id):
        self.id = id
        data = super(Server, self).get_data(self)
        self.name = data.get('name')

        @property
        def status(self):
            # perform request to get current state
            pass

    def __str__(self):
        return 'Server (ID: {}, Name[en]: "{}")'.format(
            self.id, self.name['en'])
