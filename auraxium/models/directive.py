"""Data classes for :mod:`auraxium.ps2.directive`."""

import dataclasses
from typing import Optional

from ..base import Ps2Data
from ..types import CensusData, LocaleData, optional

__all__ = [
    'DirectiveData',
    'DirectiveTierData',
    'DirectiveTreeData',
    'DirectiveTreeCategoryData'
]


@dataclasses.dataclass(frozen=True)
class DirectiveData(Ps2Data):
    """Data class for :class:`auraxium.ps2.directive.Directive`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        directive_id: The unique ID of this directive.
        directive_tree_id: The directive tree of this directive.
        directive_tier_id: The directive tier of this directive.
        objective_set_id: The objective set contributing towards this
            directive.
        qualify_requirement_id: An item that must be unlocked for this
            directive to be available.
        name: The localised name of the directive.
        name: The localised description of the directive.
        image_set_id: The image set for this directive.
        image_id: The default image asset for this directive.
        image_path: The path of the default image asset for this
            directive.

    """

    directive_id: int
    directive_tree_id: int
    directive_tier_id: int
    objective_set_id: int
    qualify_requirement_id: Optional[int]
    name: LocaleData
    description: LocaleData
    image_set_id: int
    image_id: int
    image_path: str

    @classmethod
    def from_census(cls, data: CensusData) -> 'DirectiveData':
        return cls(
            int(data.pop('directive_id')),
            int(data.pop('directive_tree_id')),
            int(data.pop('directive_tier_id')),
            int(data.pop('objective_set_id')),
            optional(data, 'qualify_requirement_id', int),
            LocaleData.from_census(data.pop('name')),
            LocaleData.from_census(data.pop('description')),
            int(data.pop('image_set_id')),
            int(data.pop('image_id')),
            str(data.pop('image_path')))


@dataclasses.dataclass(frozen=True)
class DirectiveTierData(Ps2Data):
    """Data class for :class:`auraxium.ps2.directive.DirectiveTier`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        directive_tier_id: The unique ID of the directive tier.
        directive_tree_id: The directive tree this directive belongs
            to.
        reward_set_id: The reward set awarded upon completion of this
            directive tier.
        directive_points: The directive points awarded upon completion
            of this directive tier.
        completion_count: The number of directives that must be
            completed for completion of this directive tier.
        name: The localised name of the directive tier.
        image_set_id: The image set for this directive tier.
        image_id: The default image asset for this directive tier.
        image_path: The path of the default image asset for this
            directive tier.

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
            int(data.pop('directive_tier_id')),
            int(data.pop('directive_tree_id')),
            optional(data, 'reward_set_id', int),
            int(data.pop('directive_points')),
            int(data.pop('completion_count')),
            LocaleData.from_census(data.pop('name')),
            int(data.pop('image_set_id')),
            int(data.pop('image_id')),
            str(data.pop('image_path')))


@dataclasses.dataclass(frozen=True)
class DirectiveTreeData(Ps2Data):
    """Data class for :class:`auraxium.ps2.directive.DirectiveTree`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        directive_tree_id: The unique ID of the directive tree.
        directive_tree_category_id: The category of the directive tree.
        name: The localised name of the directive tree.
        description: The localised description of the directive tree.
        image_set_id: The image set for this directive tree.
        image_id: The default image asset for this directive tree.
        image_path: The path of the default image asset for this
            directive tree.

    """

    directive_tree_id: int
    directive_tree_category_id: int
    name: LocaleData
    description: LocaleData
    image_set_id: int
    image_id: int
    image_path: str

    @classmethod
    def from_census(cls, data: CensusData) -> 'DirectiveTreeData':
        if 'description' in data:
            description = LocaleData.from_census(data.pop('description'))
        else:
            description = LocaleData.empty()
        return cls(
            int(data.pop('directive_tree_id')),
            int(data.pop('directive_tree_category_id')),
            LocaleData.from_census(data.pop('name')),
            description,
            int(data.pop('image_set_id')),
            int(data.pop('image_id')),
            str(data.pop('image_path')))


@dataclasses.dataclass(frozen=True)
class DirectiveTreeCategoryData(Ps2Data):
    """Data class for :class:`auraxium.ps2.directive.DirectiveTreeCategory`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        directive_tree_category_id: The unique ID of the directive tree
            category.
        name: The localised name of the directive tree category.

    """

    directive_tree_category_id: int
    name: LocaleData

    @classmethod
    def from_census(cls, data: CensusData) -> 'DirectiveTreeCategoryData':
        return cls(
            int(data.pop('directive_tree_category_id')),
            LocaleData.from_census(data.pop('name')))
