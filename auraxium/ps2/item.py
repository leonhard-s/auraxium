from ..census import _CENSUS_BASE_URL, Query
from ..datatypes import InterimDatatype, StaticDatatype
from .ability import Ability
from .faction import Faction
from .image import Image, ImageSet

# from .skill import SkillSet


class Item(InterimDatatype):
    _cache_size = 250
    _collection = 'item'

    def __init__(self, id):
        self.id = id

        data = Query(self.__class__, id=id).get_single()

        try:
            self.active_ability = Ability(data['activatable_ability_id'])
        except KeyError:
            self.active_ability = None
        self.category = ItemCategory(data['item_category_id'])
        self.description = data['description'][next(iter(data['description']))]
        self.faction = Faction(data['faction_id'])
        self.image = Image(data['image_id'], data['image_path'])
        self.image_set = ImageSet(data['image_set_id'])
        self.is_default_attachment = True if data['is_default_attachment'] == 1 else False
        self.is_vehicle_weapon = True if data['is_vehicle_weapon'] == 1 else False
        self.max_stack_size = data['max_stack_size']
        self.name = data['name'][next(iter(data['name']))]
        try:
            self.passive_ability = Ability(data['passive_ability_id'])
        except KeyError:
            self.passive_ability = None
        try:
            self.skill_set = SkillSet(data['skill_set'])
        except KeyError:
            self.skill_set = None
        self.type = ItemType(data['item_type_id'])

        @property
        def attachments(self):
            # Return a list of all attachments that are linked to this weapon
            pass

        @property
        def profiles(self):
            # Return a list of classes that can use this item
            pass


class ItemCategory(StaticDatatype):
    _collection = 'item_category'

    def __init__(self, id):
        self.id = id

        data = Query(self.__cache__, id=id).get_single()

        self.name = data['name'][next(iter(data['name']))]


class ItemType(StaticDatatype):
    _collection = 'item_category'

    def __init__(self, id):
        self.id = id

        data = Query(self.__cache__, id=id).get_single()

        self.name = data['name']
        self.code = data['code']
