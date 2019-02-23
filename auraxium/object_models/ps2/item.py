from ...base_api import Query
from ..datatypes import DataType, NamedDataType
from ..misc import LocalizedString
from .ability import Ability
from .faction import Faction
from .image import Image, ImageSet
from .profile import Profile


class Item(DataType, NamedDataType):
    """A PS2 item.

    An item is a player-bound entity in the game world. This includes obvious
    examples like weapons or consumables, but also depot items like camo or
    cosmetics.

    """

    _collection = 'item'

    def __init__(self, id_):
        self.id_ = id_

        # Set default values
        self._active_ability_id = None
        self._attachments = None  # Internal (See properties)
        self.description = None
        self._faction_id = None
        self._image_id = None
        self._image_set_id = None
        self.is_default_attachment = None
        self.is_vehicle_weapon = None
        self._items = None  # Internal (See properties)
        self.max_stack_size = None
        self.name = None
        self._passive_ability_id = None
        self._profiles = None  # Internal (See properties)
        self._skill_set_id = None

    # Define properties
    @property
    def active_ability(self):
        return Ability.get(id_=self._active_ability_id)

    @property
    def attachments(self):
        try:
            return self._attachments
        except AttributeError:
            data = Query(collection='item_attachment', item_id=self.id_).get()
            self._attachments = Item.list(ids=[i['attachment_item_id'] for i in data])
            return self._attachments

    @property
    def faction(self):
        return Faction.get(id_=self._faction_id)

    @property
    def image(self):
        return Image.get(id_=self._image_id)

    @property
    def image_set(self):
        return ImageSet.get(id_=self._image_set_id)

    @property
    def passive_ability(self):
        return Ability.get(id_=self._passive_ability_id)

    @property
    def profiles(self):
        try:
            return self._profiles
        except AttributeError:
            data = Query(collection='item_profile', item_id=self.id_).get()
            self._profiles = Profile.list(ids=[i['profile_id'] for i in data])
            return self._profiles

    @property
    def skill_set(self):
        from .skill import SkillSet
        # NOTE: Placing the import at the top would create a circular import,
        # hence why I placed it here instead.
        return SkillSet(id_=self._skill_set_id)

    def populate(self, data=None):
        d = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self._active_ability_id = d.get('activatable_ability_id')
        self.description = LocalizedString(d.get('description'))
        self._faction_id = d['faction_id']
        self._image_id = d['image_id']
        self._image_set_id = d['image_set_id']
        self.is_default_attachment = d['is_default_attachment']
        self.is_vehicle_weapon = d['is_vehicle_weapon']
        self.max_stack_size = d['max_stack_size']
        self.name = LocalizedString(d['name'])
        self._passive_ability_id = d.get('passive_ability_id')
        self._skill_set_id = d.get('skill_set_id')


class ItemCategory(DataType, NamedDataType):
    """The category of an item.

    Groups items into groups.
    Examples include "Knife", "Assault Rifle" or "VO Pack".

    """

    _collection = 'item_category'

    def __init__(self, id_):
        self.id_ = id_

        # Set default values
        self._items = None  # Internal (See properties)
        self.name = None

    # Define properties
    @property
    def items(self):
        """Returns a list of all items that belong to this category."""
        try:
            return self._items
        except AttributeError:
            data = Query(collection='item', item_category=self.id_).get()
            self._items = Item.list(ids=[i['item_id'] for i in data])
            return self._items

    def populate(self, data=None):
        d = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self.name = LocalizedString(d['name'])


class ItemType(DataType):
    """The type of item.

    This includes entries like "Attachment" or "Weapon", but also abstract
    objects like "Give Currency" or "Reward Set".

    """

    _collection = 'item_type'

    def __init__(self, id_):
        self.id_ = id_

        # Set default values
        self.code = None
        self.name = None

    def populate(self, data=None):
        d = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self.code = d['code']
        self.name = d['name']
