from ...base_api import Query
from ..datatypes import CachableDataType, EnumeratedDataType, NamedDataType
from ..misc import LocalizedString
from .image import Image, ImageSet
from .objective import Objective
from .reward import Reward


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
        self._image_set_id = None
        self.name = None
        self._objective_set_id = None
        self._directive_tier_id = None
        self._directive_tree_id = None
        self._objectives = None  # Internal (See properties)
        self.qualify_requirement_id = None

    # Define properties
    @property
    def image(self):
        return Image.get(id=self._image_id)

    @property
    def image_set(self):
        return ImageSet.get(id=self._image_set_id)

    @property
    def objectives(self):
        try:
            return self._objectives
        except AttributeError:
            query = Query(collection='objective_set_to_objective_group',
                          objective_set_id=self._objective_set_id).limit(100)
            query.join(type='objective', is_list=True, match='objective_group_id')
            data = query.get()
            self._objectives = Objective.list(
                ids=[o['objective_id'] for o in data['objective_list']])
            return self._objectives

    @property
    def directive_tier(self):
        return DirectiveTier.get(id=self._directive_tier_id)

    @property
    def directive_tree(self):
        return DirectiveTree.get(id=self._directive_tree_id)

    def _populate(self, data=None):
        d = data if data is not None else super()._get_data(self.id)

        # Set attribute values
        self.description = LocalizedString(d['description'])
        self._image_id = d['image_id']
        self._image_set_id = d['image_set_id']
        self.name = LocalizedString(d['name'])
        self._objective_set_id = d['objective_set_id']
        self._directive_tier_id = d['directive_tier_id']
        self._directive_tree_id = d['directive_tree_id']
        self.qualify_requirement_id = d.get('qualify_requirement_id')


class DirectiveTier(EnumeratedDataType, NamedDataType):
    """A directive tier.

    Examples include "Carbines: Novice" and "Combat Medic: Master".

    """

    _collection = 'directive_tier'

    def __init__(self, id):
        self.id = id

        # Set default values
        self.directive_points = None
        self._directive_tree_id = None
        self._image_id = None
        self._image_set_id = None
        self.name = None
        self.required_for_completion = None
        self._rewards = None  # Internal (See properties)
        self._reward_set_id = None

    # Define properties
    @property
    def directive_tree(self):
        return DirectiveTree.get(id=self._directive_tree_id)

    @property
    def image(self):
        return Image.get(id=self._image_id)

    @property
    def image_set(self):
        return ImageSet.get(id=self._image_set_id)

    @property
    def rewards(self):
        try:
            return self._rewards
        except AttributeError:
            query = Query(collection='reward_set_to_reward_group',
                          reward_set_id=self._reward_set_id)
            query.join(type='reward_group_to_reward', on='reward_group_id',
                       to='reward_group_id').is_list(True)
            data = query.get(single=True)
            self._rewards = Reward.list(
                ids=[r['reward_id'] for r in data['reward_group']['reward_list']])
            return self._rewards

    def _populate(self, data=None):
        d = data if data is not None else super()._get_data(self.id)

        # Set attribute values
        self.directive_points = d['directive_points']
        self._directive_tree_id = d['directive_tree_id']
        self._image_id = d['image_id']
        self._image_set_id = d['image_set_id']
        self.name = LocalizedString(d['name'])
        self.required_for_completion = d['completion_count']
        self._reward_set_id = d.get('reward_set_id')


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
        self._directives = None  # Internal (See properties)
        self._image_id = None
        self._image_set_id = None
        self.name = None

    # Define properties
    @property
    def category(self):
        return DirectiveTreeCategory.get(id=self._category_id)

    @property
    def directives(self):
        try:
            return self._directives
        except AttributeError:
            data = Query(collection='directive', directive_tree_id=self.id).get()
            self._directives = Directive.list(ids=[i['directive_id'] for i in data])
            return self._directives

    @property
    def image(self):
        return Image.get(id=self._image_id)

    @property
    def image_set(self):
        return ImageSet.get(id=self._image_set_id)

    def _populate(self, data=None):
        d = data if data is not None else super()._get_data(self.id)

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
        self._directive_trees = None
        self.name = None

    # Define properties
    @property
    def directive_trees(self):
        try:
            return self._directive_trees
        except AttributeError:
            data = Query(collection='directive_tree', directive_tree_category_id=self.id).get()
            self._directive_trees = DirectiveTree.list(ids=[i['directive_tree_id'] for i in data])
            return self._directive_trees

    def _populate(self, data=None):
        d = data if data is not None else super()._get_data(self.id)

        # Set attribute values
        self.name = LocalizedString(d.get('name'))
