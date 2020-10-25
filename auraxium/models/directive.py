"""Data classes for :mod:`auraxium.ps2.directive`."""

from typing import Optional

from ..base import ImageData, Ps2Data
from ..types import LocaleData

__all__ = [
    'DirectiveData',
    'DirectiveTierData',
    'DirectiveTreeData',
    'DirectiveTreeCategoryData'
]


class DirectiveData(Ps2Data, ImageData):
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


    """

    directive_id: int
    directive_tree_id: int
    directive_tier_id: int
    objective_set_id: int
    qualify_requirement_id: Optional[int] = None
    name: LocaleData
    description: LocaleData


class DirectiveTierData(Ps2Data, ImageData):
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

    """

    directive_tier_id: int
    directive_tree_id: int
    reward_set_id: Optional[int] = None
    directive_points: int
    completion_count: int
    name: LocaleData


class DirectiveTreeData(Ps2Data, ImageData):
    """Data class for :class:`auraxium.ps2.directive.DirectiveTree`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        directive_tree_id: The unique ID of the directive tree.
        directive_tree_category_id: The category of the directive tree.
        name: The localised name of the directive tree.
        description: The localised description of the directive tree.

    """

    directive_tree_id: int
    directive_tree_category_id: int
    name: LocaleData
    description: LocaleData


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
