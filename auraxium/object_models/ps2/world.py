"""Defines world-related data types for PlanetSide 2."""

from ...base_api import Query
from ..datatypes import DataType, NamedDataType
from ..misc import LocalizedString


class World(DataType, NamedDataType):
    """A world in PS2.

    World is the internal name for game servers. Connery and Cobalt are
    worlds.

    """

    _collection = 'world'

    def __init__(self, id_):
        self.id_ = id_

        # Set default values
        self.name = None

    @property
    def status(self):
        """The server status of this world."""
        query = Query(collection='world', world_id=self.id_)
        raise NotImplementedError('NYI')

    def populate(self, data=None):
        data_dict = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self.name = LocalizedString(data_dict['name'])

    @staticmethod
    def get_by_name(name: str, locale: str, ignore_case: bool = True):
        from ... import namespace
        data = Query(collection='world', namespace=namespace).limit(50).lang(locale).get()
        world_list = World.list(ids=[w['world_id'] for w in data])
        if ignore_case:
            return [w for w in world_list if w.name.en.lower() == name.lower()]
        return [w for w in world_list if w.name.en == name]
