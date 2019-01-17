from ..census import Query
from ..datatypes import CachableDataType, NamedDataType
from ..misc import LocalizedString
from .image import Image, ImageSet
from .item import Item
from .objective import Objective
from .reward import Reward


class Achievement(CachableDataType, NamedDataType):
    """An achievement in PlanetSide 2.

    An achievement is a blanket term covering both weapon medals and service
    ribbons.

    """

    _collection = 'achievement'

    def __init__(self, id):
        self.id = id

        # Set default values
        self.description = None
        self._item_id = None
        self._image_id = None
        self._image_set_id = None
        self.name = None
        self._objectives = None  # Internal (See properties)
        self._objective_group_id = None
        self.repeatable = None
        self.resource_cast_cost = None
        self._reward_id = None

    # Define properties
    @property
    def item(self):
        return Item.get(id=self._item_id)

    @property
    def image(self):
        return Image.get(id=self._image_id)

    @property
    def image_set(self):
        return ImageSet.get(id=self._image_set_id)

    @property
    def objectives(self):
        try:
            return self._objectives
        except AttributeError:
            q = Query(type='objective', limit=100)
            q.add_filter(field='objective_group_id',
                         value=self._objective_group_id)
            data = q.get()
            self._objectives = Objective.list(
                ids=[o['objective_id'] for o in data])
            return self._objectives

    @property
    def reward(self):
        return Reward.get(id=self._reward_id)

    def _populate(self, data=None):
        d = data if data is not None else super()._get_data(self.id)

        # Set attribute values
        self.description = LocalizedString(d.get('description'))
        self._item_id = d.get('item_id')
        self._image_id = d.get('image_id')
        self._image_set_id = d.get('image_set_id')
        self.name = LocalizedString(d.get('name'))
        self._objective_group_id = d.get('objective_group_id')
        self.repeatable = d.get('repeatable')
        self._reward_id = d.get('reward_id')
