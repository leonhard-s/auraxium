from ..census import Query
from ..datatypes import InterimDatatype, StaticDatatype

# from .image import Image, ImageSet
# from .reward import Reward, RewardSet
# from .objective import ObjectiveSet


class Directive(InterimDatatype):
    """A directive in PlanetSide 2."""

    _collection = 'directive'

    def __init__(self, id):
        self.id = id

        data = Query(self.__class__, id=id).get_single()

        self.description = data['description'][next(iter(data['description']))]
        # self.image = Image()
        # self.image_set = ImageSet()
        self.name = data['name'][next(iter(data['name']))]
        # self.objective_set = ObjectSet(data['objective_set_id'])

        # I have no clue what this is linked to. qualify_requirement_id is not
        # a collection, so it might not be accessible to the API.
        # self.qualify_requirement_id = #?!

        self.tier = DirectiveTier(data['directive_tier_id'])
        self.tree = DirectiveTree(data['directive_tree_id'])


class DirectiveTier(StaticDatatype):
    _collection = 'directive_tier'

    def __init__(self, id):
        self.id = id

        data = Query(self.__class__, id=id).get_single()

        self.completion_count = int(data['completion_count'])
        self.directive_points = int(data['directive_points'])
        self.directive_tree = DirectiveTree(data['directive_tree_id'])

        # self.image = Image()
        # self.image_set = ImageSet()
        self.name = data['name'][next(iter(data['name']))]

        # Not all directives have a reward set, hence the try-statement
        try:
            # self.reward_set = RewardSet(data['reward_set_id'])
            self.reward_set = None
        except KeyError:
            self.reward_set = None


class DirectiveTree(StaticDatatype):
    _collection = 'directive_tree'

    def __init__(self, id):
        self.id = id

        data = Query(self.__class__, id=id).get_single()

        self.category = DirectiveTreeCategory(
            data['directive_tree_category_id'])
        self.description = data['description'][next(iter(data['description']))]
        # self.image = Image()
        # self.image_set = ImageSet()
        self.name = data['name'][next(iter(data['name']))]


class DirectiveTreeCategory(StaticDatatype):
    _collection = 'directive_tree_category'

    def __init__(self, id):
        self.id = id

        data = Query(self.__class__, id=id).get_single()

        self.name = data['name'][next(iter(data['name']))]
