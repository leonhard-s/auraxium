from ..census import Query
from ..datatypes import StaticDatatype
from .image import ImageSet


class Currency(StaticDatatype):
    """A currency in PlanetSide 2.

    Currently, the only currency are Nanites.

    """

    _collection = 'currency'

    def __init__(self, id):
        self.id = id
        data = super(Currency, self).get_data(self)

        self.name = data.get('name')
        self.icon = ImageSet(data.get('icon_id'))
        self.inventory_cap = data.get('inventory_cap')

    def __str__(self):
        return 'Currency (ID: {}, Name[en]: "{}")'.format(
            self.id, self.name['en'])
