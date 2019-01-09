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

        data = Query(self.__class__, id=id).get_single()

        self.name = data['name'][next(iter(data['name']))]
        self.icon = ImageSet(data['icon_id'])
        self.inventory_cap = int(data['inventory_cap'])
