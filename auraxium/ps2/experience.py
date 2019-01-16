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

    def _populate(self, data=None):
        d = data if data != None else super()._get_data(self.id)

        # Set attribute values
        self.amount = d['xp']
        self.description = d['description']
