"""Defines achievement-related data types for PlanetSide 2."""

from typing import List, Optional

from ...base_api import Query
from ..datatypes import DataType, NamedDataType
from ..misc import LocalizedString
from .image import Image, ImageSet
from .item import Item
from .objective import Objective
from .reward import Reward


class Achievement(DataType, NamedDataType):  # pylint: disable=too-many-instance-attributes
    """An achievement in PlanetSide 2.

    An achievement is a blanket term covering both weapon medals and service
    ribbons.

    """

    _collection = 'achievement'

    def __init__(self, id_: int) -> None:
        self.id_ = id_

        # Set default values
        self.description: Optional[LocalizedString] = None
        self._item_id: Optional[int] = None
        self._image_id: Optional[int] = None
        self._image_set_id: Optional[int] = None
        self.name: Optional[LocalizedString] = None
        self._objectives: List[Optional[Objective]] = []  # Internal (See properties)
        self._objective_group_id: Optional[int] = None
        self.repeatable: Optional[bool] = None
        self.resource_cast_cost: Optional[int] = None
        self._reward_id: Optional[int] = None

    # Define properties
    @property
    def item(self) -> Optional[Item]:
        """The item the achievement is for."""
        return Item.get(id_=self._item_id)

    @property
    def image(self) -> Image:
        """The image for the achievement."""
        return Image.get(id_=self._image_id)

    @property
    def image_set(self) -> ImageSet:
        """The image set for the achievement."""
        return ImageSet.get(id_=self._image_set_id)

    @property
    def objectives(self) -> List[Optional[Objective]]:
        """A list of objectives related to the achievement."""
        from ... import namespace
        try:
            return self._objectives
        except AttributeError:
            query = Query(collection='objective', namespace=namespace).limit(100)
            data = query.add_term(field='objective_group_id', value=self._objective_group_id).get()
            self._objectives = Objective.list(
                ids=[o['objective_id'] for o in data])
            return self._objectives

    @property
    def reward(self) -> Reward:
        """The Reward for earning this achievement."""
        return Reward.get(id_=self._reward_id)

    def populate(self, data: dict = None) -> None:
        """Populates the data type."""
        data_dict = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self.description = LocalizedString(data_dict.get('description'))
        self._item_id = int(data_dict['item_id']) if data_dict.get('item_id') is not None else None
        self._image_id = int(data_dict['image_id']) if data_dict.get(
            'image_id') is not None else None
        self._image_set_id = int(data_dict['image_set_id']) if data_dict.get(
            'image_set_id') is not None else None
        self.name = LocalizedString(data_dict.get('name'))
        self._objective_group_id = data_dict.get('objective_group_id')
        self.repeatable = data_dict.get('repeatable')
        self._reward_id = data_dict.get('reward_id')
