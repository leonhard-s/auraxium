from ..census import Query
from ..datatypes import InterimDatatype, StaticDatatype


class Objective(InterimDatatype):
    _cache_size = 100
    _collection = 'objective'
    _join = 'objective_type'

    def __init__(self, id, data_override=None):
        self.id = id

        if super().is_cached(self):  # If the object is cached, skip
            return

        data = data_override if data_override != None else super().get_data(self)

        self.type = ObjectiveType(
            data.get('objective_type_id'), data_override=data.get('objective_type'))
        # I do not know what an objective group is, this will need testing
        # self.group = ObjectiveGroup(data.get('objective_group_id'))

        self.parameters = {}
        for i in range(9):
            self.parameters[i] = data.get('param{}'.format(i + 1))

        super()._add_to_cache(self)  # Cache this instance for future use

    def __str__(self):
        return 'Objective (ID: {})'.format(self.id)


class ObjectiveType(StaticDatatype):
    _collection = 'objective_type'

    def __init__(self, id, data_override=None):
        self.id = id

        if super().is_cached(self):  # If the object is cached, skip
            return

        data = data_override if data_override != None else super().get_data(self)

        self.description = data.get('description')

        self.parameters = {}
        for i in range(9):
            self.parameters[i] = data.get('param{}'.format(i + 1))

        super()._add_to_cache(self)  # Cache this instance for future use

    def __str__(self):
        return 'ObjectiveType (ID: {}, Description: "{}")'.format(
            self.id, self.description)
