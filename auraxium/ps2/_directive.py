"""Directive class definitions."""

from typing import List, Optional

from ..base import ImageMixin, Named
from ..census import Query
from ..models import (DirectiveData, DirectiveTierData,
                      DirectiveTreeCategoryData, DirectiveTreeData)
from .._proxy import InstanceProxy, SequenceProxy
from ..types import LocaleData

from ._objective import Objective
from ._reward import Reward

__all__ = [
    'Directive',
    'DirectiveTier',
    'DirectiveTree',
    'DirectiveTreeCategory'
]


class DirectiveTreeCategory(Named, cache_size=10, cache_ttu=300.0):
    """A category of directive.

    In-game, this is represented by the side bar to the left, e.g.
    "Infantry", "Weapons", or "Vehicles".

    .. attribute:: id
       :type: int

       The unique ID of the directive tree category. In the API
       payload, this field is called ``directive_tree_category_id``.

    .. attribute:: name
       :type: auraxium.types.LocaleData

       The localised name of the directive tree category.
    """

    collection = 'directive_tree_category'
    data: DirectiveTreeCategoryData
    id_field = 'directive_tree_category_id'
    _model = DirectiveTreeCategoryData

    # Type hints for data class fallback attributes
    id: int
    name: LocaleData

    def trees(self) -> SequenceProxy['DirectiveTree']:
        """Return the directive trees in this category.

        This returns a :class:`auraxium.SequenceProxy`.
        """
        query = Query(
            DirectiveTree.collection, service_id=self._client.service_id)
        query.add_term(field='directive_tree_id', value=self.id).limit(50)
        return SequenceProxy(DirectiveTree, query, client=self._client)


class DirectiveTree(Named, ImageMixin, cache_size=30, cache_ttu=60.0):
    """A multi-tiered tree of directives for a given category.

    Directive trees are chains of related directives like
    "Heavy Assault" in the "Infantry" category, or "Carbines" in the
    "Weapons" category.

    .. attribute:: id
       :type: int

       The unique ID of the directive tree. In the API payload, this
       field is called ``directive_tree_id``.

    .. attribute:: directive_tree_category_id
       :type: int

       The ID of the :class:`DirectiveTreeCategory` of this directive
       tree.

       .. seealso::

          :meth:`category` -- Return the directive tree category of
          this directive tree.

    .. attribute:: description
       :type: auraxium.types.LocaleData | None

       The localised description of the directive tree.

    .. attribute:: name
       :type: auraxium.types.LocaleData

       The localised name of the directive tree.
    """

    collection = 'directive_tree'
    data: DirectiveTreeData
    id_field = 'directive_tree_id'
    _model = DirectiveTreeData

    # Type hints for data class fallback attributes
    id: int
    directive_tree_category_id: int
    description: Optional[LocaleData]
    name: LocaleData
    image_id: Optional[int]
    image_set_id: Optional[int]
    image_path: Optional[str]

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
    """A tier in a directive tree.

    Directive tiers list the set of directives required to advance to
    the next tier in the :class:`DirectiveTree`, e.g.
    "Combat Medic: Adept" or "Shotguns: Master".

    .. attribute:: id
       :type: int

       The unique ID of the directive tier. In the API payload, this
       field is called ``directive_tier_id``.

    .. attribute:: directive_tree_id
       :type: int

       The ID of the :class:`DirectiveTree` this directive tier is a
       part of.

       .. seealso::

          :meth:`tree` -- Return the directive tree of this directive
          tier.

    .. attribute:: reward_set_id
       :type: int | None

       The ID of the reward set awarded upon completion of this
       directive tier.

       .. seealso::

          :meth:`rewards` -- Return the list of rewards awarded upon
          completion of this directive tier.

    .. attribute:: directive_points
       :type: int

       The number of directive points awarded upon completion of this
       directive tier.

    .. attribute:: completion_count
       :type: int

       The number of directives in this tier that must be completed to
       advance to the next stage.

    .. attribute:: name
       :type: auraxium.types.LocaleData

       The localised name of the directive tier.
    """

    collection = 'directive_tier'
    data: DirectiveTierData
    id_field = 'directive_tier_id'
    _model = DirectiveTierData

    # Type hints for data class fallback attributes
    id: int
    directive_tree_id: int
    name: LocaleData
    reward_set_id: Optional[int]
    directive_points: int
    completion_count: int
    image_id: Optional[int]
    image_set_id: Optional[int]
    image_path: Optional[str]

    def directives(self) -> SequenceProxy['Directive']:
        """Return the list of directives in this tier.

        This returns a :class:`auraxium.SequenceProxy`.
        """
        query = Query(Directive.collection, service_id=self._client.service_id)
        query.add_term(field='directive_tier_id', value=self.id).limit(100)
        return SequenceProxy(Directive, query, client=self._client)

    async def rewards(self) -> List[Reward]:
        """Return the rewards granted upon completion of this tier."""
        if self.reward_set_id is None:
            return []
        return await Reward.get_by_reward_set(
            self.reward_set_id, client=self._client).flatten()

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

    .. attribute:: id
       :type: int

       The unique ID of this directive. In the API payload, this field
       is called ``directive_id``.

    .. attribute:: directive_tree_id
       :type: int

       The ID of the :class:`DirectiveTree` of this directive.

       .. seealso::

          :meth:`tree` -- Return the directive tree of this directive.

    .. attribute:: directive_tier_id
       :type: int

       The ID of the :class:`DirectiveTier` of this directive.

       .. seealso::

          :meth:`tier` -- Return the directive tier of this directive.

    .. attribute:: objective_set_id
       :type: int

       The objective set of this directive. All objectives in the given
       set will contribute towards this directive.

       .. seealso::

          :meth:`objectives` -- Return the objectives counting towards
          completion of this directive.

    .. attribute:: name
       :type: auraxium.types.LocaleData

       The localised name of the directive.

    .. attribute:: qualify_requirement_id
       :type: int

       The ID of an :class:`~auraxium.ps2.Item` (usually weapon) that
       must be unlocked for this directive to be available.

    .. attribute:: description
       :type: auraxium.types.LocaleData

       The localised description of the directive.
    """

    collection = 'directive'
    data: DirectiveData
    id_field = 'directive_id'
    _model = DirectiveData

    # Type hints for data class fallback attributes
    id: int
    directive_tree_id: int
    directive_tier_id: int
    name: LocaleData
    objective_set_id: int
    qualify_requirement_id: Optional[int]
    description: Optional[LocaleData]
    image_id: Optional[int]
    image_set_id: Optional[int]
    image_path: Optional[str]

    def objectives(self) -> SequenceProxy[Objective]:
        """Return the objectives for this directive.

        This returns a :class:`auraxium.SequenceProxy`.
        """
        return Objective.get_by_objective_set(
            self.objective_set_id, self._client)

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
