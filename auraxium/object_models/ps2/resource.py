from ..datatypes import DataType


class ResourceType(DataType):
    """A resource in PS2.

    A resource fuels abilities like the Combat Medic's AoE heal or the Heavy
    Assault's overshield.

    """

    _collection = 'resource_type'

    def __init__(self, id_):
        self.id_ = id_

        # Set default values
        self.description = None

    def populate(self, data=None):
        d = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self.description = d['description']
