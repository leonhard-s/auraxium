"""Directive class definitions."""

import dataclasses
from typing import ClassVar, Optional, Union

from ..base import Named, Ps2Data
from ..cache import TLRUCache
from ..census import Query
from ..proxy import InstanceProxy, SequenceProxy
from ..types import CensusData
from ..utils import LocaleData, optional

from .objective import Objective


@dataclasses.dataclass(frozen=True)
class DirectiveTreeCategoryData(Ps2Data):
    """Data class for :class:`auraxium.ps2.directive.DirectiveTreeCategory`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    directive_tree_category_id: int
    name: LocaleData

    @classmethod
    def from_census(cls, data: CensusData) -> 'DirectiveTreeCategoryData':
        return cls(
            int(data['directive_tree_category_id']),
            LocaleData.from_census(data['name']))


class DirectiveTreeCategory(Named, cache_size=10, cache_ttu=300.0):
    """A directive category.

    Directive tree category are the topmost directive categorisation,
    e.g. "Infantry".
    """

    collection = 'directive_tree_category'
    data: DirectiveTreeCategoryData
    id_field = 'directive_tree_category_id'

    def _build_dataclass(self, data: CensusData) -> DirectiveTreeCategoryData:
        return DirectiveTreeCategoryData.from_census(data)

    def trees(self) -> SequenceProxy['DirectiveTree']:
        """Return the trees in the category.

        This returns a :class:`auraxium.proxy.SequenceProxy`.
        """
        query = Query(
            DirectiveTree.collection, service_id=self._client.service_id)
        query.add_term(field='directive_tree_id', value=self.id).limit(50)
        return SequenceProxy(DirectiveTree, query, client=self._client)


@dataclasses.dataclass(frozen=True)
class DirectiveTreeData(Ps2Data):
    """Data class for :class:`auraxium.ps2.directive.DirectiveTree`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    directive_tree_id: int
    directive_tree_category_id: int
    name: LocaleData
    description: Optional[LocaleData]
    image_set_id: int
    image_id: int
    image_path: str

    @classmethod
    def from_census(cls, data: CensusData) -> 'DirectiveTreeData':
        if (description := data.get('description')) is not None:
            description = LocaleData.from_census(description)
        return cls(
            int(data['directive_tree_id']),
            int(data['directive_tree_category_id']),
            LocaleData.from_census(data['name']),
            description,
            int(data['image_set_id']),
            int(data['image_id']),
            str(data['image_path']))


class DirectiveTree(Named, cache_size=30, cache_ttu=60.0):
    """A tree of directives.

    Directive trees are a chain of related directive, e.g.
    "Heavy Assault".
    """

    collection = 'directive_tree'
    data: DirectiveTreeData
    id_field = 'directive_tree_id'

    def _build_dataclass(self, data: CensusData) -> DirectiveTreeData:
        return DirectiveTreeData.from_census(data)

    def category(self) -> InstanceProxy[DirectiveTreeCategory]:
        """Return the category of the directive tree.

        This returns an :class:`auraxium.proxy.InstanceProxy`.
        """
        query = Query(DirectiveTreeCategory.collection,
                      service_id=self._client.service_id)
        query.add_term(field=DirectiveTreeCategory.id_field,
                       value=self.data.directive_tree_category_id)
        return InstanceProxy(DirectiveTreeCategory, query, client=self._client)

    def directives(self) -> SequenceProxy['Directive']:
        """Return the list of directives in this category.

        This returns a :class:`auraxium.proxy.SequenceProxy`.
        """
        query = Query(Directive.collection, service_id=self._client.service_id)
        query.add_term(field='directive_tree_id', value=self.id).limit(400)
        return SequenceProxy(Directive, query, client=self._client)

    def tiers(self) -> SequenceProxy['DirectiveTier']:
        """Return the list of directive tiers in this category.

        This returns a :class:`auraxium.proxy.SequenceProxy`.
        """
        query = Query(
            DirectiveTier.collection, service_id=self._client.service_id)
        query.add_term(field='directive_tree_id', value=self.id).limit(4)
        return SequenceProxy(DirectiveTier, query, client=self._client)


@dataclasses.dataclass(frozen=True)
class DirectiveTierData(Ps2Data):
    """Data class for :class:`auraxium.ps2.directive.DirectiveTier`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    directive_tier_id: int
    directive_tree_id: int
    reward_set_id: Optional[int]
    directive_points: int
    completion_count: int
    name: LocaleData
    image_set_id: int
    image_id: int
    image_path: str

    @classmethod
    def from_census(cls, data: CensusData) -> 'DirectiveTierData':
        return cls(
            int(data['directive_tier_id']),
            int(data['directive_tree_id']),
            optional(data, 'reward_set_id', int),
            int(data['directive_points']),
            int(data['completion_count']),
            LocaleData.from_census(data['name']),
            int(data['image_set_id']),
            int(data['image_id']),
            str(data['image_path']))


class DirectiveTier(Named, cache_size=30, cache_ttu=60.0):
    """A directive tier.

    Container for related directives, e.g. "Combat Medic: Adept".
    """

    collection = 'directive_tier'
    data: DirectiveTierData
    id_field = 'directive_tier_id'

    def _build_dataclass(self, data: CensusData) -> DirectiveTierData:
        return DirectiveTierData.from_census(data)

    def directives(self) -> SequenceProxy['Directive']:
        """Return the list of directives in this tier.

        This returns a :class:`auraxium.proxy.SequenceProxy`.
        """
        query = Query(Directive.collection, service_id=self._client.service_id)
        query.add_term(field='directive_tier_id', value=self.id).limit(100)
        return SequenceProxy(Directive, query, client=self._client)

    def tree(self) -> InstanceProxy[DirectiveTree]:
        """Return the tree of the directive.

        This returns an :class:`auraxium.proxy.InstanceProxy`.
        """
        query = Query(
            DirectiveTree.collection, service_id=self._client.service_id)
        query.add_term(
            field=DirectiveTree.id_field, value=self.data.directive_tree_id)
        return InstanceProxy(DirectiveTree, query, client=self._client)


@dataclasses.dataclass(frozen=True)
class DirectiveData(Ps2Data):
    """Data class for :class:`auraxium.ps2.directive.Directive`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    directive_id: int
    directive_tree_id: int
    directive_tier_id: int
    objective_set_id: int
    quality_requirement_id: Optional[int]
    name: LocaleData
    description: LocaleData
    image_set_id: int
    image_id: int
    image_path: str

    @classmethod
    def from_census(cls, data: CensusData) -> 'DirectiveData':
        return cls(
            int(data['directive_id']),
            int(data['directive_tree_id']),
            int(data['directive_tier_id']),
            int(data['objective_set_id']),
            optional(data, 'qualify_requirement_id', int),
            LocaleData.from_census(data['name']),
            LocaleData.from_census(data['description']),
            int(data['image_set_id']),
            int(data['image_id']),
            str(data['image_path']))


class Directive(Named, cache_size=30, cache_ttu=60.0):
    """A directive a character may complete."""

    _cache: ClassVar[TLRUCache[Union[int, str], 'Directive']]
    collection = 'directive'
    data: DirectiveData
    id_field = 'directive_id'

    def _build_dataclass(self, data: CensusData) -> DirectiveData:
        return DirectiveData.from_census(data)

    def objectives(self) -> SequenceProxy[Objective]:
        """Return the objectives for this directive.

        This returns a :class:`auraxium.proxy.SequenceProxy`.
        """
        # NOTE: This table is being treated as a single set mapping to multiple
        # objectives via their common group. This is a guess. I was not able to
        # find any directives with multiple objectives associated.
        collection: Final[str] = 'objective_set_to_objective'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(
            field='objective_set_id', value=self.data.objective_set_id)
        join = query.create_join(Objective.collection)
        join.parent_field = join.child_field = 'objective_group_id'
        join.set_list(True)
        return SequenceProxy(Objective, query, client=self._client)

    def tier(self) -> InstanceProxy[DirectiveTier]:
        """Return the tier of the directive.

        This returns an :class:`auraxium.proxy.InstanceProxy`.
        """
        query = Query(
            DirectiveTier.collection, service_id=self._client.service_id)
        query.add_term(
            field=DirectiveTier.id_field, value=self.data.directive_tier_id)
        return InstanceProxy(DirectiveTier, query, client=self._client)

    def tree(self) -> InstanceProxy[DirectiveTree]:
        """Return the tree of the directive.

        This returns an :class:`auraxium.proxy.InstanceProxy`.
        """
        query = Query(
            DirectiveTree.collection, service_id=self._client.service_id)
        query.add_term(
            field=DirectiveTree.id_field, value=self.data.directive_tree_id)
        return InstanceProxy(DirectiveTree, query, client=self._client)
