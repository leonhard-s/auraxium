"""Defines experience-related data types for PlanetSide 2."""

from ..datatypes import DataType


class Experience(DataType):
    """An experience type.

    Lists all the actions that provide experience.

    """

    _collection = 'experience'

    def __init__(self, id_):
        self.id_ = id_

        # Set default values
        self.amount = None
        self.description = None

    def populate(self, data=None):
        data_dict = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self.amount = data_dict['xp']
        self.description = data_dict['description']
