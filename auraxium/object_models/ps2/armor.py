from ..datatypes import CachableDataType, EnumeratedDataType


class ArmorFacing(EnumeratedDataType):
    """The direction a vehicle is being attacked from.

    Enumerates the directions a vehicle can be attacked from. This is used as
    part of the armor info system to determine armor modifiers based on the
    angle of attack.

    """

    _collection = 'armor_facing'

    def __init__(self, id):
        self.id = id

        # Set default values
        self.description = None

    def populate(self, data=None):
        d = data if data is not None else super()._get_data(self.id)

        # Set attribute values
        self.description = d.get('description')


class ArmorInfo(CachableDataType):
    """Armor information.

    Contains information about how armor is calculated based on the attack
    direction and entity type.

    """

    _collection = 'armor_info'

    def __init__(self, id):
        self.id = id

        # Set default values
        self._armor_facing_id = None
        self.armor_amount = None  # (Removed from the game)
        self.armor_percent = None
        self.description = None

    # Define properties
    @property
    def armor_facing(self):
        return ArmorFacing.get(id=self._armor_facing_id)

    def populate(self, data=None):
        d = data if data is not None else super()._get_data(self.id)

        # Set attribute values
        self._armor_facing_id = d.get('armor_facing_id')
        self.armor_amount = d.get('armor_amount')  # (Removed from the game)
        self.armor_percent = d.get('armor_percent')
        self.description = d.get('description')
