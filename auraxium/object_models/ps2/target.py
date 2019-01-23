from ..datatypes import EnumeratedDataType


class TargetType(EnumeratedDataType):
    """A type of target.

    Enumerates the types of target available, currently "Self", "Any, "Ally"
    and "Enemy".

    """

    _collection = 'target_type'

    def __init__(self, id):
        self.id = id

        # Set default values
        self.description = None

    def _populate(self, data=None):
        d = data if data is not None else super()._get_data(self.id)

        # Set attribute values
        self.description = d['description']
