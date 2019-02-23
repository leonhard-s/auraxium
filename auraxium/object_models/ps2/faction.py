"""Defines faction-related data types for PlanetSide 2."""

from ..datatypes import DataType, NamedDataType
from ..misc import LocalizedString
from .image import Image, ImageSet


class Faction(DataType, NamedDataType):
    """Represents a faction in PlanetSide 2.

    Factions are static datatypes. Each one should only need to be
    initialized once.

    """

    _collection = 'faction'

    def __init__(self, id_):
        self.id_ = id_

        # Set default values
        self.name = None
        self._image_id = None
        self._image_set_id = None
        self.is_playable = None
        self.tag = None

    # Define properties
    @property
    def image(self):
        """The image of this faction."""
        return Image.get(id_=self._image_id)

    @property
    def image_set(self):
        """The image set of this faction."""
        return ImageSet.get(id_=self._image_set_id)

    def populate(self, data=None):
        data_dict = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self.name = LocalizedString(data_dict['name'])
        self._image_id = data_dict['image_id']
        self._image_set_id = data_dict['image_set_id']
        self.is_playable = bool(data_dict['user_selectable'] == '1')
        # NOTE: As of the writing of this module, Nanite Systems does not have
        # a tag. As this might change with the introduction of combat robots, I
        # wrote this section in a way that should be able to handle that.
        self.tag = 'NS' if data_dict['code_tag'] == 'None' else data_dict['code_tag']
