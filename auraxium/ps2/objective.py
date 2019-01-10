from ..census import Query
from ..datatypes import InterimDatatype, StaticDatatype


class Objective(InterimDatatype):
    _cache_size = 100
    _collection = 'objective'

    def __init__(self, id):
        self.id = id
        data = super(Objective, self).get_data(self)

        self.type = ObjectiveType(data.get('objective_type_id'))
        # I do not know what an objective group is, this will need testing
        # self.group = ObjectiveGroup(data.get('objective_group_id'))

        self.parameters = {}
        for i in range(9):
            self.parameters[i] = data.get('param{}'.format(i + 1))


class ObjectiveType(StaticDatatype):
    _collection = 'objective_type'

    def __init__(self, id):
        self.id = id
        data = super(ObjectiveType, self).get_data(self)

        self.description = data.get('description')

        self.parameters = {}
        for i in range(9):
            self.parameters[i] = data.get('param{}'.format(i + 1))
