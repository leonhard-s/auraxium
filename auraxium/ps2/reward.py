from ..census import Query
from ..datatypes import InterimDatatype, StaticDatatype


class Reward(InterimDatatype):
    _collection = 'reward'

    def __init__(self, id):
        self.id = id

        data = Query(self.__class__, id=id).get_single()
        self.count_max = int(data['count_max'])
        self.count_min = int(data['count_min'])
        self.type = RewardType(data['reward_type_id'])
        self.parameters = {}
        for i in range(5):
            try:
                self.parameters[i] = data['param{}'.format(i + 1)]
            except KeyError:
                pass


class RewardType(StaticDatatype):
    _collection = 'reward_type'

    def __init__(self, id):
        self.id = id

        data = Query(self.__class__, id=id).get_single()
        self.count_max = data['count_max']
        self.count_min = data['count_min']
        self.description = data['description']
        self.parameters = {}
        for i in range(5):
            try:
                self.parameters[i] = data['param{}'.format(i + 1)]
            except KeyError:
                pass
