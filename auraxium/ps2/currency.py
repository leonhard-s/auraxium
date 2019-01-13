from ..census import Query
from ..datatypes import StaticDatatype
from .image import ImageSet


class Currency(StaticDatatype):
    """A currency in PlanetSide 2.

    Currently, the only currency are Nanites.

    """

    _collection = 'currency'
    _join = 'image_set'

    def __init__(self, id, data_override=None):
        self.id = id

        if super().is_cached(self):  # If the object is cached, skip
            return

        data = data_override if data_override != None else super().get_data(self)

        self.name = data.get('name')
        self.icon = ImageSet(data.get('icon_id'),
                             data_override=data.get('image_set'))
        self.inventory_cap = data.get('inventory_cap')

        super()._add_to_cache(self)  # Cache this instance for future use

    def __str__(self):
        return 'Currency (ID: {}, Name[en]: "{}")'.format(
            self.id, self.name['en'])
