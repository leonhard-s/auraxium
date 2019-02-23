"""Defines title-related data types for PlanetSide 2."""

from ..datatypes import DataType, NamedDataType
from ..misc import LocalizedString


class Title(DataType, NamedDataType):
    """A title.

    A player title a player can equip. The title id_ "0" signifies that the
    player has not selected any title.

    """

    _collection = 'title'

    def __init__(self, id_):
        self.id_ = id_

        # Set default values
        self.name = None

    def populate(self, data=None):
        data_dict = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self.name = LocalizedString(data_dict['name'])
