"""Data classes for :mod:`auraxium.ps2._item`."""

from .base import ImageData, RESTPayload
from ..types import LocaleData

__all__ = [
    'ItemCategoryData',
    'ItemData',
    'ItemTypeData'
]


class ItemCategoryData(RESTPayload):
    """Data class for :class:`auraxium.ps2.ItemCategory`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    item_category_id: int
    name: LocaleData


class ItemData(RESTPayload, ImageData):
    """Data class for :class:`auraxium.ps2.Item`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    item_id: int
    item_type_id: int | None = None
    item_category_id: int | None = None
    activatable_ability_id: int | None = None
    passive_ability_id: int | None = None
    is_vehicle_weapon: bool
    name: LocaleData | None = None
    description: LocaleData | None = None
    faction_id: int | None = None
    max_stack_size: int
    skill_set_id: int | None = None
    is_default_attachment: bool


class ItemTypeData(RESTPayload):
    """Data class for :class:`auraxium.ps2.ItemType`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    item_type_id: int
    name: str
    code: str
