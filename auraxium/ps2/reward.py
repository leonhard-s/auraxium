from ..census import Query
from ..datatypes import InterimDatatype, StaticDatatype


class Reward(InterimDatatype):
    _collection = 'reward'

    def __init__(self, id):
        self.id = id
        data = super(Reward, self).get_data(self)

        self.count_max = data.get('count_max')
        self.count_min = data.get('count_min')
        self.type = RewardType(data.get('reward_type_id'))

        self.parameters = {}
        for i in range(5):
            self.parameters[i] = data.get('param{}'.format(i + 1))


class RewardType(StaticDatatype):
    _collection = 'reward_type'

    def __init__(self, id):
        self.id = id
        data = super(RewardType, self).get_data(self)

        self.count_max = data.get('count_max')
        self.count_min = data.get('count_min')
        self.description = data.get('description')

        self.parameters = {}
        for i in range(5):
            self.parameters[i] = data.get('param{}'.format(i + 1))
