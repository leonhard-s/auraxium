"""Defines armor-related data types for PlanetSide 2."""

from ..datatypes import DataType


class ArmorFacing(DataType):
    """The direction a vehicle is being attacked from.

    Enumerates the directions a vehicle can be attacked from. This is used as
    part of the armor info system to determine armor modifiers based on the
    angle of attack.

    """

    _collection = 'armor_facing'

    def __init__(self, id_):
        self.id_ = id_

        # Set default values
        self.description = None

    def populate(self, data=None):
        data_dict = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self.description = data_dict.get('description')


class ArmorInfo(DataType):
    """Armor information.

    Contains information about how armor is calculated based on the attack
    direction and entity type.

    """

    _collection = 'armor_info'

    def __init__(self, id_):
        self.id_ = id_

        # Set default values
        self._armor_facing_id = None
        self.armor_amount = None  # (Removed from the game)
        self.armor_percent = None
        self.description = None

    # Define properties
    @property
    def armor_facing(self):
        """The ArmorFacing the armor info is referencing."""
        return ArmorFacing.get(id_=self._armor_facing_id)

    def populate(self, data=None):
        data_dict = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self._armor_facing_id = data_dict.get('armor_facing_id')
        self.armor_amount = data_dict.get('armor_amount')  # (Removed from the game)
        self.armor_percent = data_dict.get('armor_percent')
        self.description = data_dict.get('description')
