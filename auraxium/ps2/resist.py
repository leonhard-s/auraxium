from ..census import Query
from ..datatypes import InterimDatatype, StaticDatatype


class ResistInfo(InterimDatatype):
    _cache_size = 250
    _collection = 'resist_info'
    _join = 'resist_type'

    def __init__(self, id, data_override=None):
        self.id = id

        if super().is_cached(self):  # If the object is cached, skip
            return

        data = data_override if data_override != None else super().get_data(self)

        self.description = data.get('description')
        self.headshot_multiplier = data.get('multiplier_when_headshot')
        self.percent = data.get('resist_percent')
        self.type = ResistType(data.get('resist_type_id'),
                               data_override=data.get('resist_type'))

        super()._add_to_cache(self)  # Cache this instance for future use

    def __str__(self):
        return 'ResistInfo (ID: {}, Description: "{}")'.format(
            self.id, self.description)


class ResistType(StaticDatatype):
    _collection = 'resist_type'

    def __init__(self, id, data_override=None):
        self.id = id

        if super().is_cached(self):  # If the object is cached, skip
            return

        data = data_override if data_override != None else super().get_data(self)

        self.description = data.get('description')

        super()._add_to_cache(self)  # Cache this instance for future use

    def __str__(self):
        return 'ResistInfo (ID: {}, Description: "{}")'.format(
            self.id, self.description)
