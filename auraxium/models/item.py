"""Data classes for :mod:`auraxium.ps2.item`."""

import dataclasses
from typing import Optional

from ..base import Ps2Data
from ..types import CensusData
from ..utils import LocaleData, optional

__all__ = [
    'ItemCategoryData',
    'ItemData',
    'ItemTypeData'
]


@dataclasses.dataclass(frozen=True)
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

    @classmethod
    def from_census(cls, data: CensusData) -> 'ItemCategoryData':
        return cls(
            int(data['item_category_id']),
            LocaleData.from_census(data['name']))


@dataclasses.dataclass(frozen=True)
class ItemData(Ps2Data):
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
        item_set_id: The image set for this item.
        item_id: The default image asset for this item.
        image_path: The path to the default image for this item.
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
    item_type_id: Optional[int]
    item_category_id: Optional[int]
    activatable_ability_id: Optional[int]
    passive_ability_id: Optional[int]
    is_vehicle_weapon: bool
    name: LocaleData
    description: LocaleData
    faction_id: Optional[int]
    max_stack_size: int
    image_set_id: Optional[int]
    image_id: Optional[int]
    image_path: Optional[str]
    skill_set_id: Optional[int]
    is_default_attachment: bool

    @classmethod
    def from_census(cls, data: CensusData) -> 'ItemData':
        if 'description' in data:
            description = LocaleData.from_census(data['description'])
        else:
            description = LocaleData.empty()
        return cls(
            int(data['item_id']),
            optional(data, 'item_type_id', int),
            optional(data, 'item_category_id', int),
            optional(data, 'activatable_ability_id', int),
            optional(data, 'passive_ability_id', int),
            bool(int(data['is_vehicle_weapon'])),
            LocaleData.from_census(data['name']),
            description,
            optional(data, 'faction_id', int),
            int(data['max_stack_size']),
            optional(data, 'image_set_id', int),
            optional(data, 'image_id', int),
            optional(data, 'image_path', str),
            optional(data, 'skill_set_id', int),
            bool(int(data['is_default_attachment'])))


@dataclasses.dataclass(frozen=True)
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

    @classmethod
    def from_census(cls, data: CensusData) -> 'ItemTypeData':
        return cls(
            int(data['item_type_id']),
            str(data['name']),
            str(data['code']))
