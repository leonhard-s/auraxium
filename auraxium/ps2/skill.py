from ..census import Query
from ..datatypes import InterimDatatype
from .image import Image, ImageSet
from .item import Item


class Skill(InterimDatatype):
    _cache_size = 100
    _collection = 'skill'
    _join = ['image_set', 'skill_line']

    def __init__(self, id, data_override=None):
        self.id = id

        if super().is_cached(self):  # If the object is cached, skip
            return

        data = data_override if data_override != None else super().get_data(self)

        self.description = data.get('description')
        self.grant_item_id = data.get('grant_item_id')
        self.image = Image(data.get('image_set_id'))
        self.image_set = ImageSet(
            data.get('image_id'), data_override=data.get('image_set'))
        self.name = data.get('name')
        self.skill_line = SkillLine(
            data.get('skill_line_id'), data_override=data.get('skill_line'))
        self.skill_line_index = data.get('skill_line_index')
        self.skill_points = data.get('skill_points')

        super()._add_to_cache(self)  # Cache this instance for future use

    def __str__(self):
        return 'Skill (ID: {}, Name[en]: "{}")'.format(
            self.id, self.name['en'])


class SkillCategory(InterimDatatype):
    _cache_size = 100
    _collection = 'skill_category'
    _join = ['image_set', 'skill_set']

    def __init__(self, id, data_override=None):
        self.id = id

        if super().is_cached(self):  # If the object is cached, skip
            return

        data = data_override if data_override != None else super().get_data(self)

        self.description = data.get('description')
        self.image = Image(data.get('image_set_id'))
        self.image_set = ImageSet(
            data.get('image_id'), data_override=data.get('image_set'))
        self.name = data.get('name')
        self.skill_points = data.get('skill_points')
        self.skill_set = SkillSet(
            data.get('skill_set_id'), data_override=data.get('skill_set'))
        self.skill_set_index = data.get('skill_set_index')

        super()._add_to_cache(self)  # Cache this instance for future use

    def __str__(self):
        return 'SkillCategory (ID: {}, Name[en]: "{}")'.format(
            self.id, self.name['en'])


class SkillLine(InterimDatatype):
    _cache_size = 100
    _collection = 'skill_line'
    _join = ['image_set', 'skill_category']

    def __init__(self, id, data_override=None):
        self.id = id

        if super().is_cached(self):  # If the object is cached, skip
            return

        data = super(SkillLine, self).get_data(self)

        self.category = SkillCategory(
            data.get('skill_category_id'), data_override=data.get('skill_category'))
        self.category_index = data.get('skill_category_id')
        self.description = data.get('description')
        self.image = Image(data.get('image_set_id'))
        self.image_set = ImageSet(
            data.get('image_id'), data_override=data.get('image_set'))
        self.name = data.get('name')
        self.skill_points = data.get('skill_points')

        super()._add_to_cache(self)  # Cache this instance for future use

    def __str__(self):
        return 'SkillLine (ID: {}, Name[en]: "{}")'.format(
            self.id, self.name['en'])


class SkillSet(InterimDatatype):
    _cache_size = 100
    _collection = 'skill_set'
    _join = 'image_set'

    def __init__(self, id, data_override=None):
        self.id = id

        if super().is_cached(self):  # If the object is cached, skip
            return

        data = super(SkillSet, self).get_data(self)

        self.description = data.get('description')
        self.image = Image(data.get('image_set_id'))
        self.image_set = ImageSet(
            data.get('image_id'), data_override=data.get('image_set'))
        self.name = data.get('name')
        self.required_item = Item(data.get('required_item_id'))
        self.skill_points = data.get('skill_points')

        super()._add_to_cache(self)  # Cache this instance for future use

    def __str__(self):
        return 'SkillSet (ID: {}, Name[en]: "{}")'.format(
            self.id, self.name['en'])
