"""Defines directive-related data types for PlanetSide 2."""

from ...base_api import Query
from ..datatypes import DataType, NamedDataType
from ..misc import LocalizedString
from .image import Image, ImageSet
from .objective import Objective
from .reward import Reward


class Directive(DataType, NamedDataType):  # pylint: disable=too-many-instance-attributes
    """A directive in PlanetSide 2.

    A directive is a requirement that gives progress towards the next directive
    tier.

     """

    _collection = 'directive'

    def __init__(self, id_):
        self.id_ = id_

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
        """The image of the directive."""
        return Image.get(id_=self._image_id)

    @property
    def image_set(self):
        """The image set of the directive."""
        return ImageSet.get(id_=self._image_set_id)

    @property
    def objectives(self):
        """A list of objectives linked to this directive."""
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
        """The tier of the directive."""
        return DirectiveTier.get(id_=self._directive_tier_id)

    @property
    def directive_tree(self):
        """The directive tree this directive is in."""
        return DirectiveTree.get(id_=self._directive_tree_id)

    def populate(self, data=None):
        data_dict = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self.description = LocalizedString(data_dict['description'])
        self._image_id = data_dict['image_id']
        self._image_set_id = data_dict['image_set_id']
        self.name = LocalizedString(data_dict['name'])
        self._objective_set_id = data_dict['objective_set_id']
        self._directive_tier_id = data_dict['directive_tier_id']
        self._directive_tree_id = data_dict['directive_tree_id']
        self.qualify_requirement_id = data_dict.get('qualify_requirement_id')


class DirectiveTier(DataType, NamedDataType):  # pylint: disable=too-many-instance-attributes
    """A directive tier.

    Examples include "Carbines: Novice" and "Combat Medic: Master".

    """

    _collection = 'directive_tier'

    def __init__(self, id_):
        self.id_ = id_

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
        """The directive tree the directive tier is in."""
        return DirectiveTree.get(id_=self._directive_tree_id)

    @property
    def image(self):
        """The image of the directive tier."""
        return Image.get(id_=self._image_id)

    @property
    def image_set(self):
        """The image set of the directive tier."""
        return ImageSet.get(id_=self._image_set_id)

    @property
    def rewards(self):
        """The list of rewards for completing this directive tier."""
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

    def populate(self, data=None):
        data_dict = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self.directive_points = data_dict['directive_points']
        self._directive_tree_id = data_dict['directive_tree_id']
        self._image_id = data_dict['image_id']
        self._image_set_id = data_dict['image_set_id']
        self.name = LocalizedString(data_dict['name'])
        self.required_for_completion = data_dict['completion_count']
        self._reward_set_id = data_dict.get('reward_set_id')


class DirectiveTree(DataType, NamedDataType):
    """A directive tree.

    Directive trees are an entry for a directive category. Examples for
    directive trees from the "Weapons" category would be "Carbines" or
    "Pistols".

    """

    _collection = 'directive_tier'

    def __init__(self, id_):
        self.id_ = id_

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
        """The category of the directive."""
        return DirectiveTreeCategory.get(id_=self._category_id)

    @property
    def directives(self):
        """A list of directives that are in this directive tier."""
        try:
            return self._directives
        except AttributeError:
            data = Query(collection='directive', directive_tree_id=self.id_).get()
            self._directives = Directive.list(ids=[i['directive_id'] for i in data])
            return self._directives

    @property
    def image(self):
        """The image of this directive tier."""
        return Image.get(id_=self._image_id)

    @property
    def image_set(self):
        """The image set of this directive tier."""
        return ImageSet.get(id_=self._image_set_id)

    def populate(self, data=None):
        data_dict = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self._category_id = data_dict['directive_tree_category_id']
        self.description = LocalizedString(data_dict['description'])
        self._image_id = data_dict['image_id']
        self._image_set_id = data_dict['image_set_id']
        self.name = LocalizedString(data_dict['name'])


class DirectiveTreeCategory(DataType, NamedDataType):
    """A category of directive trees.

    Examples for directive tree categories are "Infantry", "Vehicle" or
    "Weapons".

    """

    _collection = 'directive_tier_category'

    def __init__(self, id_):
        self.id_ = id_

        # Set default values
        self._directive_trees = None
        self.name = None

    # Define properties
    @property
    def directive_trees(self):
        """A list of directive trees that are in this category."""
        try:
            return self._directive_trees
        except AttributeError:
            data = Query(collection='directive_tree', directive_tree_category_id=self.id_).get()
            self._directive_trees = DirectiveTree.list(ids=[i['directive_tree_id'] for i in data])
            return self._directive_trees

    def populate(self, data=None):
        data_dict = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self.name = LocalizedString(data_dict.get('name'))
