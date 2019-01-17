from ..census import Query
from ..datatypes import CachableDataType, NamedDataType
from ..misc import LocalizedString
from .image import Image, ImageSet
from .item import Item
# from .objetive import ObjectiveGroup
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
        # self._objective_group = None  # Always identical to the id?
        self.repeatable = None
        self.resource_cast_cost = None
        self._reward_id = None

    # Define properties
    @property
    def item(self):
        try:
            return self._item
        except AttributeError:
            self._item = Item.get(id=self._item_id)
            return self._item

    @property
    def image(self):
        try:
            return self._image
        except AttributeError:
            self._image = Image.get(id=self._image_id)
            return self._image

    @property
    def image_set(self):
        try:
            return self._image_set
        except AttributeError:
            self._image_set = ImageSet.get(id=self._image_set_id)
            return self._image_set

    # @property
    # def objective_group(self):
    #     try:
    #         return self._objective_group
    #     except AttributeError:
    #         self._objective_group = ObjectiveGroup.get(id=self._objective_group_id)
    #         return self._objective_group

    @property
    def reward(self):
        try:
            return self._reward
        except AttributeError:
            self._reward = Reward.get(id=self._reward_id)
            return self._reward

    def _populate(self, data=None):
        d = data if data != None else super()._get_data(self.id)

        # Set attribute values
        self.description = LocalizedString(d.get('description'))
        self._item_id = d.get('item_id')
        self._image_id = d.get('image_id')
        self._image_set_id = d.get('image_set_id')
        self.name = LocalizedString(d.get('name'))
        # self._objective_group_id = d.get('objective_group_id')
        self.repeatable = d.get('repeatable')
        self._reward_id = d.get('reward_id')
