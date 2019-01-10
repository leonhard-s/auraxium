from ..census import _CENSUS_BASE_URL, Query
from ..datatypes import InterimDatatype, StaticDatatype
from .ability import Ability
from .faction import Faction
from .image import Image, ImageSet

# from .skillset import SkillSet


class Item(InterimDatatype):
    _cache_size = 250
    _collection = 'item'

    def __init__(self, id):
        self.id = id
        data = super(Item, self).get_data(self)

        self.active_ability = Ability(data.get('activatable_ability_id'))
        self.category = ItemCategory(data.get('item_category_id'))
        self.description = data.get('description')
        self.faction = Faction(data.get('faction_id'))
        self.image = Image(data.get('image_id'), data.get('image_path'))
        self.image_set = ImageSet(data.get('image_set_id'))
        self.is_default_attachment = True if data.get(
            'is_default_attachment') == '1' else False
        self.is_vehicle_weapon = True if data.get(
            'is_vehicle_weapon') == '1' else False
        self.max_stack_size = data.get('max_stack_size')
        self.name = data.get('name')
        self.passive_ability = Ability(data.get('passive_ability_id'))
        # self.skill_set = SkillSet(data.get('skill_set'))
        self.type = ItemType(data.get('item_type_id'))

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
        data = super(ItemCategory, self).get_data(self)
        self.name = data.get('name')


class ItemType(StaticDatatype):
    _collection = 'item_category'

    def __init__(self, id):
        self.id = id
        data = super(ItemType, self).get_data(self)
        self.name = data.get('name')
        self.code = data.get('code')
