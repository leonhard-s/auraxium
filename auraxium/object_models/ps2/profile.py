"""Defines profile-related data types for PlanetSide 2."""

from ...base_api import Query
from ..datatypes import DataType, NamedDataType
from .faction import Faction
from .image import Image, ImageSet
from ..misc import LocalizedString
from .armor import ArmorInfo
from .resist import ResistInfo


class Profile(DataType, NamedDataType):  # pylint: disable=too-many-instance-attributes
    """An entity in PlanetSide 2.

    Lists the targetable entities in the game world.

    """

    _collection = 'profile'

    def __init__(self, id_):
        self.id_ = id_

        # Set default values
        self._armor_info = None  # Internal (See properties)
        self.description = None
        self._faction_id = None
        self._image_id = None
        self._image_set_id = None
        self.movement_speed = None
        self.name = None
        self.profile_type_id = None
        self.profile_type_description = None
        self._resist_info = None  # Internal (See properties)
        self.reverse_speed = None
        self.sprint_speed_modifier = None
        self.strafe_speed_modifier = None

    # Define properties
    @property
    def armor_info(self):
        """A list of ArmorInfo objects for this profile."""
        try:
            return self._armor_info
        except AttributeError:
            data = Query(collection='profile_armor_map', profile_id=self.id_).limit(100).get()
            self._armor_info = ArmorInfo.list(ids=[i['armor_info_id'] for i in data])
            return self._armor_info

    @property
    def faction(self):
        """The faction of the profile."""
        return Faction.get(id_=self._faction_id)

    @property
    def image(self):
        """The image of the profile."""
        return Image.get(id_=self._image_id)

    @property
    def image_set(self):
        """The image set of the profile."""
        return ImageSet.get(id_=self._image_set_id)

    @property
    def resist_info(self):
        """A list of ResistInfo objects for this profile."""
        try:
            return self._resist_info
        except AttributeError:
            data = Query(collection='profile_resist_map', profile_id=self.id_).limit(100).get()
            self._resist_info = ResistInfo.list(ids=[i['resist_info_id'] for i in data])
            return self._resist_info

    def populate(self, data=None):
        data_dict = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self.profile_type_id = data_dict['profile_type_id']
        self.profile_type_description = data_dict['profile_type_description']
        self._faction_id = data_dict['faction_id']
        self.description = LocalizedString(data_dict['description'])
        self.name = LocalizedString(data_dict['name'])
        self._image_id = data_dict.get('image_id')
        self._image_set_id = data_dict.get('image_set_id')
        self.movement_speed = data_dict.get('movement_speed')
        self.reverse_speed = data_dict.get('backpedal_speed_modifier')
        self.sprint_speed_modifier = data_dict.get('sprint_speed_modifier')
        self.strafe_speed_modifier = data_dict.get('strafe_speed_modifier')
