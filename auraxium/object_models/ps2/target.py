"""Defines target-type-related data types for PlanetSide 2."""

from ..datatypes import DataType


class TargetType(DataType):
    """A type of target.

    Enumerates the types of target available, currently "Self", "Any, "Ally"
    and "Enemy".

    """

    _collection = 'target_type'

    def __init__(self, id_):
        self.id_ = id_

        # Set default values
        self.description = None

    def populate(self, data=None):
        data_dict = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self.description = data_dict['description']
