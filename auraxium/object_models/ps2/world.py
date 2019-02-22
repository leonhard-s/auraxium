from ...base_api import Query
from ..datatypes import EnumeratedDataType, NamedDataType
from ..misc import LocalizedString


class World(EnumeratedDataType, NamedDataType):
    """A world in PS2.

    World is the internal name for game servers. Connery and Cobalt are
    worlds.

    """

    _collection = 'world'

    def __init__(self, id):
        self.id = id

        # Set default values
        self.name = None

    @property
    def status(self):
        q = Query(collection='world', world_id=self.id)
        raise NotImplementedError('NYI')

    def populate(self, data=None):
        d = data if data is not None else super()._get_data(self.id)

        # Set attribute values
        self.name = LocalizedString(d['name'])
