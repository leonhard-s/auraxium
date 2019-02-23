"""Defines currency-related data types for PlanetSide 2."""

from ..datatypes import DataType, NamedDataType
from ..misc import LocalizedString
from .image import ImageSet


class Currency(DataType, NamedDataType):
    """A currency.

    Currently, the only currency are Nanites.

    """

    _collection = 'currency'

    def __init__(self, id_):
        self.id_ = id_

        # Set default values
        self.name = None
        self._image_set_id = None
        self.inventory_cap = None

    # Define properties
    @property
    def image_set(self):
        """The image set of the currency."""
        return ImageSet.get(id_=self._image_set_id)

    def populate(self, data=None):
        data_dict = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self.name = LocalizedString(data_dict['name'])
        self._image_set_id = data_dict['icon_id']
        self.inventory_cap = data_dict['inventory_cap']
