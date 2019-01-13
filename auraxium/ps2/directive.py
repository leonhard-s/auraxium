from ..census import Query
from ..datatypes import InterimDatatype, StaticDatatype
from .image import Image, ImageSet
# from .objective import ObjectiveSet
from .reward import Reward  # , RewardSet


class Directive(InterimDatatype):
    """A directive in PlanetSide 2."""

    _collection = 'directive'
    _join = ['directive_tier', 'directive_tree', 'image_set']

    def __init__(self, id, data_override=None):
        self.id = id

        if super().is_cached(self):  # If the object is cached, skip
            return

        data = data_override if data_override != None else super().get_data(self)

        self.description = data.get('description')
        self.image = Image(data.get('image_id'))
        self.image_set = ImageSet(
            data.get('image_set_id'), data_override=data.get('image_set'))
        self.name = data.get('name')
        # self.objective_set = ObjectiveSet(data.get('objective_set_id'))
        self.tier = DirectiveTier(
            data.get('directive_tier_id'), data_override=data.get('directive_tier'))
        self.tree = DirectiveTree(
            data.get('directive_tree_id'), data_override=data.get('directive_tree'))

        # I have no clue what this is linked to. qualify_requirement_id is not
        # a collection, so it might not be accessible to the API.
        # self.qualify_requirement_id = #?!

        super()._add_to_cache(self)  # Cache this instance for future use

    def __str__(self):
        return 'Directive (ID: {}, name[en]: "{}")'.format(
            self.id, self.name['en'])


class DirectiveTier(StaticDatatype):
    _collection = 'directive_tier'
    _join = ['directive_tree', 'image_set']

    def __init__(self, id, data_override=None):
        self.id = id

        if super().is_cached(self):  # If the object is cached, skip
            return

        data = data_override if data_override != None else super().get_data(self)

        self.completion_count = data.get('completion_count')
        self.directive_points = data.get('directive_points')
        self.directive_tree = DirectiveTree(
            data.get('directive_tree_id'), data_override=data.get('directive_tree'))
        self.image = Image(data.get('image_id'))
        self.image_set = ImageSet(data.get('image_set_id'),
                                  data_override=data.get('image_set'))
        self.name = data.get('name')
        # self.reward_set = RewardSet(data.get('reward_set_id'))

        super()._add_to_cache(self)  # Cache this instance for future use

    def __str__(self):
        return 'DirectiveTier (ID: {}, name[en]: "{}")'.format(
            self.id, self.name['en'])


class DirectiveTree(StaticDatatype):
    _collection = 'directive_tree'
    _join = ['directive_tree_category', 'image_set']

    def __init__(self, id, data_override=None):
        self.id = id

        if super().is_cached(self):  # If the object is cached, skip
            return

        data = data_override if data_override != None else super().get_data(self)

        self.category = DirectiveTreeCategory(
            data.get('directive_tree_category_id'), data_override=data.get('directive_tree_category'))
        self.description = data.get('description')
        self.image = Image(data.get('image_id'))
        self.image_set = ImageSet(data.get('image_set_id'),
                                  data_override=data.get('image_set'))
        self.name = data.get('name')

        super()._add_to_cache(self)  # Cache this instance for future use

    def __str__(self):
        return 'DirectiveTree (ID: {}, name[en]: "{}")'.format(
            self.id, self.name['en'])


class DirectiveTreeCategory(StaticDatatype):
    _collection = 'directive_tree_category'

    def __init__(self, id, data_override=None):
        self.id = id

        if super().is_cached(self):  # If the object is cached, skip
            return

        data = data_override if data_override != None else super().get_data(self)

        self.name = data.get('name')

        super()._add_to_cache(self)  # Cache this instance for future use

    def __str__(self):
        return 'DirectiveTreeCategory (ID: {}, name[en]: "{}")'.format(
            self.id, self.name['en'])
