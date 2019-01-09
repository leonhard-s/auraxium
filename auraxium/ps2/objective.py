from ..census import Query
from ..datatypes import InterimDatatype, StaticDatatype


class Objective(InterimDatatype):
    _cache_size = 100
    _collection = 'objective'

    def __init__(self, id):
        self.id = id

        data = Query(self.__class__, id=id).get_single()
        self.type = ObjectiveType(data['objective_type_id'])
        # self.group = ObjectiveGroup(data['objective_group_id'])
        self.parameters = {}
        for i in range(9):
            try:
                self.parameters[i] = data['param{}'.format(i + 1)]
            except KeyError:
                pass


class ObjectiveType(StaticDatatype):
    _collection = 'objective_type'

    def __init__(self, id):
        self.id = id

        data = Query(self.__class__, id=id).get_single()
        self.description = data['description']
        self.parameters = {}
        for i in range(9):
            try:
                self.parameters[i] = data['param{}'.format(i + 1)]
            except KeyError:
                pass
