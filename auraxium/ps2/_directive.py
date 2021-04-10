"""Directive class definitions."""

from typing import Final, Optional

from ..base import ImageMixin, Named
from ..census import Query
from ..models import (DirectiveData, DirectiveTierData,
                      DirectiveTreeCategoryData, DirectiveTreeData)
from ..proxy import InstanceProxy, SequenceProxy
from ..types import LocaleData

from ._objective import Objective

__all__ = [
    'Directive',
    'DirectiveTier',
    'DirectiveTree',
    'DirectiveTreeCategory'
]


class DirectiveTreeCategory(Named, ImageMixin, cache_size=10, cache_ttu=300.0):
    """A directive category.

    Directive tree category are the topmost directive categorisation,
    e.g. "Infantry".

    Attributes:
        directive_tree_category_id: The unique ID of the directive tree
            category.
        name: Localised name of the directive tree category.

    """

    collection = 'directive_tree_category'
    data: DirectiveTreeCategoryData
    dataclass = DirectiveTreeCategoryData
    id_field = 'directive_tree_category_id'

    # Type hints for data class fallback attributes
    id: int
    name: LocaleData

    def trees(self) -> SequenceProxy['DirectiveTree']:
        """Return the trees in the category.

        This returns a :class:`auraxium.SequenceProxy`.
        """
        query = Query(
            DirectiveTree.collection, service_id=self._client.service_id)
        query.add_term(field='directive_tree_id', value=self.id).limit(50)
        return SequenceProxy(DirectiveTree, query, client=self._client)


class DirectiveTree(Named, ImageMixin, cache_size=30, cache_ttu=60.0):
    """A tree of directives.

    Directive trees are a chain of related directive, e.g.
    "Heavy Assault".

    Attributes:
        id: The unique ID of the directive tree.
        directive_tree_category_id: The category of the directive tree.
        description: The localised description of the directive tree.
        name: Localised name of the directive tree.

    """

    collection = 'directive_tree'
    data: DirectiveTreeData
    dataclass = DirectiveTreeData
    id_field = 'directive_tree_id'

    # Type hints for data class fallback attributes
    id: int
    directive_tree_category_id: int
    description: Optional[LocaleData]
    name: LocaleData

    def category(self) -> InstanceProxy[DirectiveTreeCategory]:
        """Return the category of the directive tree.

        This returns an :class:`auraxium.InstanceProxy`.
        """
        query = Query(DirectiveTreeCategory.collection,
                      service_id=self._client.service_id)
        query.add_term(field=DirectiveTreeCategory.id_field,
                       value=self.data.directive_tree_category_id)
        return InstanceProxy(DirectiveTreeCategory, query, client=self._client)

    def directives(self) -> SequenceProxy['Directive']:
        """Return the list of directives in this category.

        This returns a :class:`auraxium.SequenceProxy`.
        """
        query = Query(Directive.collection, service_id=self._client.service_id)
        query.add_term(field='directive_tree_id', value=self.id).limit(400)
        return SequenceProxy(Directive, query, client=self._client)

    def tiers(self) -> SequenceProxy['DirectiveTier']:
        """Return the list of directive tiers in this category.

        This returns a :class:`auraxium.SequenceProxy`.
        """
        query = Query(
            DirectiveTier.collection, service_id=self._client.service_id)
        query.add_term(field='directive_tree_id', value=self.id).limit(4)
        return SequenceProxy(DirectiveTier, query, client=self._client)


class DirectiveTier(Named, ImageMixin, cache_size=30, cache_ttu=60.0):
    """A directive tier.

    Container for related directives, e.g. "Combat Medic: Adept".

    Attributes:
        id: The unique ID of the directive tier.
        directive_tree_id: The directive tree this directive belongs
            to.
        reward_set_id: The reward set awarded upon completion of this
            directive tier.
        directive_points: The directive points awarded upon completion
            of this directive tier.
        completion_count: The number of directives that must be
            completed for completion of this directive tier.
        name: Localised name of the directive tier.

    """

    collection = 'directive_tier'
    data: DirectiveTierData
    dataclass = DirectiveTierData
    id_field = 'directive_tier_id'

    # Type hints for data class fallback attributes
    id: int
    directive_tree_id: int
    name: LocaleData
    reward_set_id: Optional[int]
    directive_points: int
    completion_count: int

    def directives(self) -> SequenceProxy['Directive']:
        """Return the list of directives in this tier.

        This returns a :class:`auraxium.SequenceProxy`.
        """
        query = Query(Directive.collection, service_id=self._client.service_id)
        query.add_term(field='directive_tier_id', value=self.id).limit(100)
        return SequenceProxy(Directive, query, client=self._client)

    def tree(self) -> InstanceProxy[DirectiveTree]:
        """Return the tree of the directive.

        This returns an :class:`auraxium.InstanceProxy`.
        """
        query = Query(
            DirectiveTree.collection, service_id=self._client.service_id)
        query.add_term(
            field=DirectiveTree.id_field, value=self.data.directive_tree_id)
        return InstanceProxy(DirectiveTree, query, client=self._client)


class Directive(Named, ImageMixin, cache_size=30, cache_ttu=60.0):
    """A directive a character may complete.

    Attributes:
        id: The unique ID of this directive.
        directive_tree_id: The directive tree of this directive.
        directive_tier_id: The directive tier of this directive.
        objective_set_id: The objective set contributing towards this
            directive.
        name: Localised name of the directive.
        qualify_requirement_id: An item that must be unlocked for this
            directive to be available.
        description: The localised description of the directive.

    """

    collection = 'directive'
    data: DirectiveData
    dataclass = DirectiveData
    id_field = 'directive_id'

    # Type hints for data class fallback attributes
    id: int
    directive_tree_id: int
    directive_tier_id: int
    name: LocaleData
    objective_set_id: int
    qualify_requirement_id: Optional[int]
    description: Optional[LocaleData]

    def objectives(self) -> SequenceProxy[Objective]:
        """Return the objectives for this directive.

        This returns a :class:`auraxium.SequenceProxy`.
        """
        # NOTE: This table is being treated as a single set mapping to multiple
        # objectives via their common group. This is a guess. I was not able to
        # find any directives with multiple objectives associated.
        collection: Final[str] = 'objective_set_to_objective'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(
            field='objective_set_id', value=self.data.objective_set_id)
        join = query.create_join(Objective.collection)
        join.set_fields('objective_group_id')
        join.set_list(True)
        return SequenceProxy(Objective, query, client=self._client)

    def tier(self) -> InstanceProxy[DirectiveTier]:
        """Return the tier of the directive.

        This returns an :class:`auraxium.InstanceProxy`.
        """
        query = Query(
            DirectiveTier.collection, service_id=self._client.service_id)
        query.add_term(
            field=DirectiveTier.id_field, value=self.data.directive_tier_id)
        return InstanceProxy(DirectiveTier, query, client=self._client)

    def tree(self) -> InstanceProxy[DirectiveTree]:
        """Return the tree of the directive.

        This returns an :class:`auraxium.InstanceProxy`.
        """
        query = Query(
            DirectiveTree.collection, service_id=self._client.service_id)
        query.add_term(
            field=DirectiveTree.id_field, value=self.data.directive_tree_id)
        return InstanceProxy(DirectiveTree, query, client=self._client)
