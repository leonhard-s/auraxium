"""Defines vehicle-related data types for PlanetSide 2."""

from ..datatypes import DataType, NamedDataType
from .currency import Currency
from .faction import Faction
from .image import Image, ImageSet
from ..misc import LocalizedString


class Vehicle(DataType, NamedDataType):  # pylint: disable=too-many-instance-attributes
    """A vehicle.

    A vehicle that a player can enter to traverse Auraxis in style.

    """

    _collection = 'vehicle'

    def __init__(self, id_):
        self.id_ = id_

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
        """The currency used to spawn the vehicle."""
        return Currency.get(id_=self._currency_id)

    @property
    def faction(self):
        """The faction of the vehicle."""
        return Faction.get(id_=self._faction_id)

    @property
    def image(self):
        """The image for the vehicle."""
        return Image.get(id_=self._image_id)

    @property
    def image_set(self):
        """The image set for the vehicle."""
        return ImageSet.get(id_=self._image_set_id)

    @property
    def skill_set(self):
        """The skill set for the vehicle."""
        return ImageSet.get(id_=self._skill_set_id)

    def populate(self, data=None):
        data_dict = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self.cost = data_dict.get('cost')
        self._currency_id = data_dict.get('currency_id')
        self.description = LocalizedString(data_dict['description'])
        self._faction_id = data_dict.get('faction_id')
        self._image_id = data_dict.get('image_id')
        self._image_set_id = data_dict.get('image_set_id')
        self.name = LocalizedString(data_dict['name'])
        self._skill_set_id = data_dict.get('skill_set_id')
        self.type_id = data_dict.get('type_id')
        self.type_name = data_dict.get('type_name')
