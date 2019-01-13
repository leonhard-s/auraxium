from ..census import Query
from ..datatypes import InterimDatatype
from .image import Image, ImageSet
from .item import Item
# from .objective import ObjectiveSet
from .reward import Reward


class Achievement(InterimDatatype):
    """An achievement in PlanetSide 2.

    An achievement is a blanket term covering both weapon medals and service
    ribbons.

    """

    # Since achievements are quite light-weight and cannot be resolved further,
    # their cache size can be safely increased.
    _cache_size = 100
    _collection = 'achievement'
    _join = ['item', 'image_set', 'reward']

    def __init__(self, id, data_override=None):
        self.id = id

        if super().is_cached(self):  # If the object is cached, skip
            return

        data = data_override if data_override != None else super().get_data(self)

        self.description = data.get('description')
        self.item = Item(data.get('item_id'), data_override=data.get('item'))
        self.image = Image(data.get('image_id'))
        self.image_set = ImageSet(
            data.get('image_set_id'), data_override=data.get('image_set'))
        self.name = data.get('name')
        # self.objective_group = None  # Identical to objective_set?
        self.repeatable = data.get('repeatable')
        self.reward = Reward(data.get('reward_id'),
                             data_override=data.get('reward'))

        super()._add_to_cache(self)  # Cache this instance for future use

    def __str__(self):
        return 'Achievement (ID: {}, Name[en]: "{}")'.format(
            self.id, self.name['en'])
