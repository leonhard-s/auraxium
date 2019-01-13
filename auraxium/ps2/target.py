from ..census import Query
from ..datatypes import StaticDatatype


class TargetType(StaticDatatype):
    _collection = 'target_type'

    def __init__(self, id, data_override=None):
        self.id = id

        if super().is_cached(self):  # If the object is cached, skip
            return

        data = data_override if data_override != None else super().get_data(self)

        self.description = data.get('description')

        super()._add_to_cache(self)  # Cache this instance for future use

    def __str__(self):
        return 'TargetType (ID: {}, Description: "{}")'.format(
            self.id, self.description)
