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

    def __init__(self, id):
        self.id = id
        data = super(Achievement, self).get_data(self)

        self.description = data['description'][next(iter(data['description']))]
        self.item = Item(data['item_id'])
        self.image = Image(data['image_id'], path=data['image_path'])
        self.image_set = ImageSet(data['image_set_id'])
        self.name = data['name'][next(iter(data['name']))]
        self.objective_group = None  # Identical to objective_set?
        self.repeatable = data['repeatable']
        self.reward = Reward(data['reward_id'])
