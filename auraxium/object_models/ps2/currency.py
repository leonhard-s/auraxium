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
        return ImageSet.get(id_=self._image_set_id)

    def populate(self, data=None):
        d = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self.name = LocalizedString(d['name'])
        self._image_set_id = d['icon_id']
        self.inventory_cap = d['inventory_cap']
