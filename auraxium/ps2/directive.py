from ..census import Query
from ..datatypes import InterimDatatype, StaticDatatype
from .image import Image, ImageSet
from .objective import ObjectiveSet
from .reward import Reward, RewardSet


class Directive(InterimDatatype):
    """A directive in PlanetSide 2."""

    _collection = 'directive'

    def __init__(self, id):
        self.id = id
        data = super(Directive, self).get_data(self)

        self.description = data.get('description')
        self.image = Image(data.get('image_id'))
        self.image_set = ImageSet(data.get('image_set_id'))
        self.name = data.get('name')
        self.objective_set = ObjectiveSet(data.get('objective_set_id'))
        self.tier = DirectiveTier(data.get('directive_tier_id'))
        self.tree = DirectiveTree(data.get('directive_tree_id'))

        # I have no clue what this is linked to. qualify_requirement_id is not
        # a collection, so it might not be accessible to the API.
        # self.qualify_requirement_id = #?!
        pass


class DirectiveTier(StaticDatatype):
    _collection = 'directive_tier'

    def __init__(self, id):
        self.id = id
        data = super(Currency, self).get_data(self)

        self.completion_count = data.get('completion_count')
        self.directive_points = data.get('directive_points')
        self.directive_tree = DirectiveTree(data.get('directive_tree_id'))
        self.image = Image(data.get('image_id'))
        self.image_set = ImageSet(data.get('image_set_id'))
        self.name = data.get('name')
        # self.reward_set = RewardSet(data.get('reward_set_id'))


class DirectiveTree(StaticDatatype):
    _collection = 'directive_tree'

    def __init__(self, id):
        self.id = id
        data = super(DirectiveTree, self).get_data(self)

        self.category = DirectiveTreeCategory(
            data.get('directive_tree_category_id'))
        self.description = data.get('description')
        self.image = Image(data.get('image_id'))
        self.image_set = ImageSet(data.get('image_set_id'))
        self.name = data.get('name')


class DirectiveTreeCategory(StaticDatatype):
    _collection = 'directive_tree_category'

    def __init__(self, id):
        self.id = id
        data = super(DirectiveTreeCategory, self).get_data(self)
        self.name = data.get('name')
