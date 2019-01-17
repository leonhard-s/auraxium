from ..census import Query
from ..datatypes import EnumeratedDataType, NamedDataType
from .faction import Faction
from .image import Image, ImageSet
from ..misc import LocalizedString
from .armor import ArmorInfo
from .resist import ResistInfo


class Profile(EnumeratedDataType, NamedDataType):
    """An entity in PlanetSide 2.

    Lists the targetable entities in the game world.

    """

    _collection = 'profile'

    def __init__(self, id):
        self.id = id

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
        try:
            return self._armor_info
        except AttributeError:
            q = Query(type='profile_armor_map', limit=100)
            d = q.add_filter(field='profile_id', value=self.id).get()
            self._armor_info = ArmorInfo.list(
                ids=[i['armor_info_id'] for i in d])
            return self._armor_info

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
    def resist_info(self):
        try:
            return self._resist_info
        except AttributeError:
            q = Query(type='profile_resist_map', limit=100)
            d = q.add_filter(field='profile_id', value=self.id).get()
            self._resist_info = ResistInfo.list(
                ids=[i['resist_info_id'] for i in d])
            return self._resist_info

    def _populate(self, data=None):
        d = data if data is not None else super()._get_data(self.id)

        # Set attribute values
        self.profile_type_id = d['profile_type_id']
        self.profile_type_description = d['profile_type_description']
        self._faction_id = d['faction_id']
        self.description = LocalizedString(d['description'])
        self.name = LocalizedString(d['name'])
        self._image_id = d.get('image_id')
        self._image_set_id = d.get('image_set_id')
        self.movement_speed = d.get('movement_speed')
        self.reverse_speed = d.get('backpedal_speed_modifier')
        self.sprint_speed_modifier = d.get('sprint_speed_modifier')
        self.strafe_speed_modifier = d.get('strafe_speed_modifier')
