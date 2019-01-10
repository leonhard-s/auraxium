from ..census import Query
from ..datatypes import InterimDatatype, StaticDatatype


class ResistInfo(InterimDatatype):
    _cache_size = 250
    _collection = 'resist_info'

    def __init__(self, id):
        self.id = id
        data = super(ResistInfo, self).get_data(self)
        self.description = data.get('description')
        self.headshot_multiplier = data.get('multiplier_when_headshot')
        self.percent = data.get('resist_percent')
        self.type = ResistType(data.get('resist_type_id'))


class ResistType(StaticDatatype):
    _collection = 'resist_type'

    def __init__(self, id):
        self.id = id
        data = super(ResistType, self).get_data(self)
        self.description = data.get('description')
