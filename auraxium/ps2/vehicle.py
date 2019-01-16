from ..census import Query
from ..datatypes import CachableDataType, EnumeratedDataType
from .currency import Currency
from .faction import Faction
from .image import Image, ImageSet
from ..misc import LocalizedString


class Vehicle(EnumeratedDataType):
    """A vehicle.

    A vehicle that a player can enter to traverse Auraxis in style.

    """

    _collection = 'vehicle'

    def __init__(self, id, data=None):
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
            try:
                return self._currency
            except AttributeError:
                self._currency = Currency.get(
                    cls=self.__class__, id=self._currency_id)
                return self._currency

        @property
        def faction(self):
            try:
                return self._faction
            except AttributeError:
                self._faction = Faction.get(
                    cls=self.__class__, id=self._faction_id)
                return self._faction

        @property
        def image(self):
            try:
                return self._image
            except AttributeError:
                self._image = Image.get(cls=self.__class__, id=self._image_id)
                return self._image

        @property
        def image_set(self):
            try:
                return self._image_set
            except AttributeError:
                self._image_set = ImageSet.get(cls=self.__class__,
                                               id=self._image_set_id)
                return self._image_set

        @property
        def skill_set(self):
            try:
                return self._skill_set
            except AttributeError:
                self._skill_set = ImageSet.get(cls=self.__class__,
                                               id=self._skill_set_id)
                return self._skill_set

    def _populate(self, data=None):
        d = data if data != None else super()._get_data(self.id)

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
