from ..census import Query
from ..datatypes import EnumeratedDataType, NamedDataType
from ..misc import LocalizedString
from .image import ImageSet


class Currency(EnumeratedDataType, NamedDataType):
    """A currency.

    Currently, the only currency are Nanites.

    """

    _collection = 'currency'

    def __init__(self, id):
        self.id = id

        # Set default values
        self.name = None
        self._image_set_id = None
        self.inventory_cap = None

    # Define properties
    @property
    def image_set(self):
        try:
            return self._image_set
        except AttributeError:
            self._image_set = ImageSet.get(id=self._image_set_id)
            return self._image_set

    def _populate(self, data=None):
        d = data if data != None else super()._get_data(self.id)

        # Set attribute values
        self.name = LocalizedString(d['name'])
        self._image_set_id = d['icon_id']
        self.inventory_cap = d['inventory_cap']
