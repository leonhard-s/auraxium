from ..census import Query
from ..datatypes import InterimDatatype
from .image import Image, ImageSet
from .item import Item


class Skill(InterimDatatype):
    _cache_size = 100
    _collection = 'skill'

    def __init__(self, id):
        self.id = id
        data = super(Skill, self).get_data(self)

        self.description = data['description'][next(iter(data['description']))]
        self.grant_item_id = int(data['grant_item_id'])
        self.image = Image(data['image_set_id'])
        self.image_set = ImageSet(data['image_id'])
        self.name = data['name'][next(iter(data['name']))]
        self.skill_line = SkillLine(data['skill_line_id'])
        self.skill_line_index = int(data['skill_line_index'])
        self.skill_points = int(data['skill_points'])


class SkillCategory(InterimDatatype):
    _cache_size = 100
    _collection = 'skill_category'

    def __init__(self, id):
        self.id = id
        data = super(SkillCategory, self).get_data(self)

        self.description = data['description'][next(iter(data['description']))]
        self.image = Image(data['image_set_id'])
        self.image_set = ImageSet(data['image_id'])
        self.name = data['name'][next(iter(data['name']))]
        self.skill_points = int(data['skill_points'])
        self.skill_set = SkillSet(data['skill_set_id'])
        self.skill_set_index = int(data['skill_set_index'])


class SkillLine(InterimDatatype):
    _cache_size = 100
    _collection = 'skill_line'

    def __init__(self, id):
        self.id = id
        data = super(SkillLine, self).get_data(self)

        self.category = SkillCategory(data['skill_category_id'])
        self.category_index = int(data['skill_category_id'])
        self.description = data['description'][next(iter(data['description']))]
        self.image = Image(data['image_set_id'])
        self.image_set = ImageSet(data['image_id'])
        self.name = data['name'][next(iter(data['name']))]
        self.skill_points = int(data['skill_points'])


class SkillSet(InterimDatatype):
    _cache_size = 100
    _collection = 'skill_set'

    def __init__(self, id):
        self.id = id
        data = super(SkillSet, self).get_data(self)

        self.description = data['description'][next(iter(data['description']))]
        self.image = Image(data['image_set_id'])
        self.image_set = ImageSet(data['image_id'])
        self.name = data['name'][next(iter(data['name']))]
        self.required_item = Item(data['required_item_id'])
        self.skill_points = int(data['skill_points'])
