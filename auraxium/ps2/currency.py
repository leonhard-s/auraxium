from ..census import Query
from ..datatypes import EnumeratedDataType
from ..misc import LocalizedString
from .image import ImageSet


class Currency(EnumeratedDataType):
    """A currency.

    Currently, the only currency are Nanites.

    """

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

    def _populate(self, data_override=None):
        data = data_override if data_override != None else super().get(self.id)

        # Set attribute values
        self.name = LocalizedString(data['name'])
        self._image_set_id = data['icon_id']
        self.inventory_cap = data['inventory_cap']
