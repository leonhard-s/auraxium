from ..census import Query
from ..datatypes import CachableDataType, EnumeratedDataType, NamedDataType
from ..misc import LocalizedString
from .image import Image, ImageSet
# from .objective import ObjectiveSet
from .reward import Reward  # , RewardSet


class Directive(CachableDataType, NamedDataType):
    """A directive in PlanetSide 2.

    A directive is a requirement that gives progress towards the next directive
    tier.

     """

    _collection = 'directive'

    def __init__(self, id):
        self.id = id

        # Set default value
        self.description = None
        self._image_id = None
        self._image_set = None
        self.name = None
        # self._objective_set_id = None
        self._directive_tier_id = None
        self._directive_tree_id = None
        self.qualify_requirement_id = None

    # Define properties
    @property
    def image(self):
        try:
            return self._image
        except AttributeError:
            self._image = Image.get(id=self._image_id)
            return self._image

    @property
    def image_set(self):
        try:
            return self._image_set
        except AttributeError:
            self._image_set = ImageSet.get(id=self._image_set_id)
            return self._image_set

    # @property
    # def objective_set(self):
    #     try:
    #         return self._objective_set
    #     except AttributeError:
    #         self._objective_set = ObjectiveSet.get(
    #             id=self._objective_set_id)
    #         return self._objective_set

    @property
    def directive_tier(self):
        try:
            return self._directive_tier
        except AttributeError:
            self._directive_tier = DirectiveTier.get(
                id=self._directive_tier_id)
            return self._directive_tier

    @property
    def directive_tree(self):
        try:
            return self._directive_tree
        except AttributeError:
            self._directive_tree = DirectiveTree.get(
                id=self._directive_tree_id)
            return self._directive_tree

    def _populate(self, data=None):
        d = data if data != None else super()._get_data(self.id)

        # Set attribute values
        self.description = LocalizedString(d['description'])
        self._image_id = d['image_id']
        self._image_set_id = d['image_set_id']
        self.name = LocalizedString(d['name'])
        # self.objective_set = d['objective_set_id']
        self.tier = d['directive_tier_id']
        self.tree = d['directive_tree_id']
        self.qualify_requirement_id = d.get('qualify_requirement_id')


class DirectiveTier(EnumeratedDataType, NamedDataType):
    """A directive tier.

    Examples include "Carbines: Novice" and "Combat Medic: Master".

    """

    _collection = 'directive_tier'

    def __init__(self, id):
        self.id = id

        # Set default values
        self.required_for_completion = None
        self.directive_points = None
        self._directive_tree_id = None
        self._image_id = None
        self._image_set_id = None
        self.name = None
        self._reward_set_id = None

    # Define properties
    @property
    def directive_tree(self):
        try:
            return self._directive_tree
        except AttributeError:
            self._directive_tree = DirectiveTree.get(
                id=self._directive_tree_id)
            return self._directive_tree

    @property
    def image(self):
        try:
            return self._image
        except AttributeError:
            self._image = Image.get(id=self._image_id)
            return self._image

    @property
    def image_set(self):
        try:
            return self._image_set
        except AttributeError:
            self._image_set = ImageSet.get(id=self._image_set_id)
            return self._image_set

    # @property
    # def reward_set(self):
    #     try:
    #         return self._reward_set
    #     except AttributeError:
    #         self._reward_set = RewardSet.get(id=self._reward_set_id)
    #         return self._reward_set

    def _populate(self, data=None):
        d = data if data != None else super()._get_data(self.id)

        # Set attribute values
        self.required_for_completion = d['completion_count']
        self.directive_points = d['directive_points']
        self._directive_tree_id = d['directive_tree_id']
        self._image_id = d['image_id']
        self._image_set_id = d['image_set_id']
        self.name = LocalizedString(d['name'])
        # self.reward_set = d.get('reward_set_id')


class DirectiveTree(EnumeratedDataType, NamedDataType):
    """A directive tree.

    Directive trees are an entry for a directive category. Examples for
    directive trees from the "Weapons" category would be "Carbines" or
    "Pistols".

    """

    _collection = 'directive_tier'

    def __init__(self, id):
        self.id = id

        # Set default values
        self._category_id = None
        self.description = None
        self._image_id = None
        self._image_set_id = None
        self.name = None

    # Define properties
    @property
    def category(self):
        try:
            return self._category
        except AttributeError:
            self._category = DirectiveTreeCategory.get(id=self._category_id)
            return self._category

    @property
    def directives(self):
        try:
            return self._directives
        except AttributeError:
            q = Query(type='directive')
            q.add_filter(field='directive_tree_id', value=self.id)
            d = q.get()
            self._directives = Directive.list(
                ids=[i['directive_id'] for i in d])
            return self._directives

    @property
    def image(self):
        try:
            return self._image
        except AttributeError:
            self._image = Image.get(id=self._image_id)
            return self._image

    @property
    def image_set(self):
        try:
            return self._image_set
        except AttributeError:
            self._image_set = ImageSet.get(id=self._image_set_id)
            return self._image_set

    def _populate(self, data=None):
        d = data if data != None else super()._get_data(self.id)

        # Set attribute values
        self._category_id = d['directive_tree_category_id']
        self.description = LocalizedString(d['description'])
        self._image_id = d['image_id']
        self._image_set_id = d['image_set_id']
        self.name = LocalizedString(d['name'])


class DirectiveTreeCategory(EnumeratedDataType, NamedDataType):
    """A category of directive trees.

    Examples for directive tree categories are "Infantry", "Vehicle" or
    "Weapons".

    """

    _collection = 'directive_tier_category'

    def __init__(self, id):
        self.id = id

        # Set default values
        self.name = None

    # Define properties
    @property
    def directive_trees(self):
        try:
            return self._directive_trees
        except AttributeError:
            q = Query(type='directive_tree')
            q.add_filter(field='directive_tree_category_id', value=self.id)
            d = q.get()
            self._directive_trees = DirectiveTree.list(
                ids=[i['directive_tree_id'] for i in d])
            return self._directive_trees

    def _populate(self, data=None):
        d = data if data != None else super()._get_data(self.id)

        # Set attribute values
        self.name = LocalizedString(d.get('name'))
