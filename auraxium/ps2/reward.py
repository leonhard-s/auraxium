from ..census import Query
from ..datatypes import InterimDatatype, StaticDatatype


class Reward(InterimDatatype):
    _collection = 'reward'
    _join = 'reward_type'

    def __init__(self, id, data_override=None):
        self.id = id

        if super().is_cached(self):  # If the object is cached, skip
            return

        data = data_override if data_override != None else super().get_data(self)

        self.count_max = data.get('count_max')
        self.count_min = data.get('count_min')
        self.type = RewardType(data.get('reward_type_id'),
                               data_override=data.get('reward_type'))

        self.parameters = {}
        for i in range(5):
            self.parameters[i] = data.get('param{}'.format(i + 1))

        super()._add_to_cache(self)  # Cache this instance for future use

    def __str__(self):
        return 'Reward (ID: {})'.format(self.id)


class RewardType(StaticDatatype):
    _collection = 'reward_type'

    def __init__(self, id, data_override=None):
        self.id = id

        if super().is_cached(self):  # If the object is cached, skip
            return

        data = data_override if data_override != None else super().get_data(self)

        self.count_max = data.get('count_max')
        self.count_min = data.get('count_min')
        self.description = data.get('description')

        self.parameters = {}
        for i in range(5):
            self.parameters[i] = data.get('param{}'.format(i + 1))

        super()._add_to_cache(self)  # Cache this instance for future use

    def __str__(self):
        return 'RewardType (ID: {}, Description: "{}")'.format(
            self.id, self.description)
