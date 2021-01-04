"""Data classes for :mod:`auraxium.ps2.item`."""

from typing import Optional

from ..base import ImageData, Ps2Data
from ..types import LocaleData

__all__ = [
    'ItemCategoryData',
    'ItemData',
    'ItemTypeData'
]

# pylint: disable=too-few-public-methods


class ItemCategoryData(Ps2Data):
    """Data class for :class:`auraxium.ps2.item.ItemCategory`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        item_category_id: The unique ID of this item category.
        name: The localised name of the category.

    """

    item_category_id: int
    name: LocaleData


class ItemData(Ps2Data, ImageData):
    """Data class for :class:`auraxium.ps2.item.Item`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        item_id: The unique ID of this item.
        item_type_id: The ID of the item type for this item.
        item_category_id: The ID of the item category for this item.
        activatable_ability_id: (Not yet documented)
        passive_ability_id: (Not yet documented)
        is_vehicle_weapon: Whether this item is a vehicle weapon.
        name: Localised name of the item.
        description: Localised description of the item.
        faction_id: The faction that has access to this item.
        max_stack_size: The stack size for stackable items such as
            grenades.
        skill_set_id: The skill set associated with this item. This is
            used for upgradable items like the Medical Applicator or
            Repair Tool.
        is_default_attachment: Default attachments are generally not
            visible to the user and are used whenever nothing is
            selected. Examples include the default iron sights, or the
            regular ammo type for weapon supporting non-standard
            ammo types.

    """

    item_id: int
    item_type_id: Optional[int] = None
    item_category_id: Optional[int] = None
    activatable_ability_id: Optional[int] = None
    passive_ability_id: Optional[int] = None
    is_vehicle_weapon: bool
    name: LocaleData
    description: Optional[LocaleData] = None
    faction_id: Optional[int] = None
    max_stack_size: int
    skill_set_id: Optional[int] = None
    is_default_attachment: bool


class ItemTypeData(Ps2Data):
    """Data class for :class:`auraxium.ps2.item.ItemType`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        item_type_id: The unique ID of this item type.
        name: The identifying name of this item type.
        code: The internal code used to describe this item type.

    """

    item_type_id: int
    name: str
    code: str
