from ..datatypes import CachableDataType


class Experience(CachableDataType):
    """An experience type.

    Lists all the actions that provide experience.

    """

    def __init__(self, id):
        self.id = id

        # Set default values
        self.amount = None
        self.description = None

    def _populate(self, data_override=None):
        data = data_override if data_override != None else super().get(self.id)

        # Set attribute values
        self.amount = data['xp']
        self.description = data['description']
