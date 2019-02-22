from ..datatypes import EnumeratedDataType


class ResourceType(EnumeratedDataType):
    """A resource in PS2.

    A resource fuels abilities like the Combat Medic's AoE heal or the Heavy
    Assault's overshield.

    """

    _collection = 'resource_type'

    def __init__(self, id):
        self.id = id

        # Set default values
        self.description = None

    def populate(self, data=None):
        d = data if data is not None else super()._get_data(self.id)

        # Set attribute values
        self.description = d['description']
