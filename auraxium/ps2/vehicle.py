from ..datatypes import EnumeratedDataType, NamedDataType
from .currency import Currency
from .faction import Faction
from .image import Image, ImageSet
from ..misc import LocalizedString


class Vehicle(EnumeratedDataType, NamedDataType):
    """A vehicle.

    A vehicle that a player can enter to traverse Auraxis in style.

    """

    _collection = 'vehicle'

    def __init__(self, id):
        self.id = id

        # Set default values
        self.cost = None
        self._currency_id = None
        self.description = None
        self._faction_id = None
        self._image_id = None
        self._image_set_id = None
        self.name = None
        self._skill_set_id = None
        self.type_id = None
        self.type_name = None

    # Define properties
    @property
    def currency(self):
        return Currency.get(id=self._currency_id)

    @property
    def faction(self):
        return Faction.get(id=self._faction_id)

    @property
    def image(self):
        return Image.get(id=self._image_id)

    @property
    def image_set(self):
        return ImageSet.get(id=self._image_set_id)

    @property
    def skill_set(self):
        return ImageSet.get(id=self._skill_set_id)

    def _populate(self, data=None):
        d = data if data is not None else super()._get_data(self.id)

        # Set attribute values
        self.cost = d.get('cost')
        self._currency_id = d.get('currency_id')
        self.description = LocalizedString(d['description'])
        self._faction_id = d.get('faction_id')
        self._image_id = d.get('image_id')
        self._image_set_id = d.get('image_set_id')
        self.name = LocalizedString(d['name'])
        self._skill_set_id = d.get('skill_set_id')
        self.type_id = d.get('type_id')
        self.type_name = d.get('type_name')
