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

        self.description = data.get('description')
        self.grant_item_id = data.get('grant_item_id')
        self.image = Image(data.get('image_set_id'))
        self.image_set = ImageSet(data.get('image_id'))
        self.name = data.get('name')
        self.skill_line = SkillLine(data.get('skill_line_id'))
        self.skill_line_index = data.get('skill_line_index')
        self.skill_points = data.get('skill_points')

    def __str__(self):
        return 'Skill (ID: {}, Name[en]: "{}")'.format(
            self.id, self.name['en'])


class SkillCategory(InterimDatatype):
    _cache_size = 100
    _collection = 'skill_category'

    def __init__(self, id):
        self.id = id
        data = super(SkillCategory, self).get_data(self)

        self.description = data.get('description')
        self.image = Image(data.get('image_set_id'))
        self.image_set = ImageSet(data.get('image_id'))
        self.name = data.get('name')
        self.skill_points = data.get('skill_points')
        self.skill_set = SkillSet(data.get('skill_set_id'))
        self.skill_set_index = data.get('skill_set_index')

    def __str__(self):
        return 'SkillCategory (ID: {}, Name[en]: "{}")'.format(
            self.id, self.name['en'])


class SkillLine(InterimDatatype):
    _cache_size = 100
    _collection = 'skill_line'

    def __init__(self, id):
        self.id = id
        data = super(SkillLine, self).get_data(self)

        self.category = SkillCategory(data.get('skill_category_id'))
        self.category_index = data.get('skill_category_id')
        self.description = data.get('description')
        self.image = Image(data.get('image_set_id'))
        self.image_set = ImageSet(data.get('image_id'))
        self.name = data.get('name')
        self.skill_points = data.get('skill_points')

    def __str__(self):
        return 'SkillLine (ID: {}, Name[en]: "{}")'.format(
            self.id, self.name['en'])


class SkillSet(InterimDatatype):
    _cache_size = 100
    _collection = 'skill_set'

    def __init__(self, id):
        self.id = id
        data = super(SkillSet, self).get_data(self)

        self.description = data.get('description')
        self.image = Image(data.get('image_set_id'))
        self.image_set = ImageSet(data.get('image_id'))
        self.name = data.get('name')
        self.required_item = Item(data.get('required_item_id'))
        self.skill_points = data.get('skill_points')

    def __str__(self):
        return 'SkillSet (ID: {}, Name[en]: "{}")'.format(
            self.id, self.name['en'])
