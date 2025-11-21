"""Data classes for :mod:`auraxium.ps2._directive`."""

from .base import ImageData, RESTPayload
from ..types import LocaleData

__all__ = [
    'DirectiveData',
    'DirectiveTierData',
    'DirectiveTreeData',
    'DirectiveTreeCategoryData'
]


class DirectiveData(RESTPayload, ImageData):
    """Data class for :class:`auraxium.ps2.Directive`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    directive_id: int
    directive_tree_id: int
    directive_tier_id: int
    objective_set_id: int
    qualify_requirement_id: int | None = None
    name: LocaleData
    description: LocaleData | None = None


class DirectiveTierData(RESTPayload, ImageData):
    """Data class for :class:`auraxium.ps2.DirectiveTier`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    directive_tier_id: int
    directive_tree_id: int
    reward_set_id: int | None = None
    directive_points: int
    completion_count: int
    name: LocaleData


class DirectiveTreeData(RESTPayload, ImageData):
    """Data class for :class:`auraxium.ps2.DirectiveTree`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    directive_tree_id: int
    directive_tree_category_id: int
    name: LocaleData
    description: LocaleData | None = None


class DirectiveTreeCategoryData(RESTPayload):
    """Data class for :class:`auraxium.ps2.DirectiveTreeCategory`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    directive_tree_category_id: int
    name: LocaleData
