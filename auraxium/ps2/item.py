"""Item and item attachment class definitions."""

import dataclasses
from typing import Final, Optional, TYPE_CHECKING

from ..base import Cached, Named, Ps2Data
from ..census import Query
from ..request import extract_single, run_query
from ..proxy import InstanceProxy, SequenceProxy
from ..types import CensusData
from ..utils import LocaleData, optional

from .profile import Profile

if TYPE_CHECKING:
    # This is only imported during static type checking to resolve the forward
    # references. During runtime, this would cause a circular import.
    from .weapon import Weapon, WeaponDatasheet


@dataclasses.dataclass(frozen=True)
class ItemCategoryData(Ps2Data):
    """Data class for :class:`auraxium.ps2.item.ItemCategory`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    item_category_id: int
    name: LocaleData

    @classmethod
    def from_census(cls, data: CensusData) -> 'ItemCategoryData':
        return cls(
            int(data['item_category_id']),
            LocaleData.from_census(data['name']))


class ItemCategory(Named, cache_size=32, cache_ttu=3600.0):
    """A category of item.

    This represents the item filter views used in the in-game depot,
    such as "Infantry Gear", "Weapon Camo" or "Vehicle Weapons".
    """

    collection = 'item_category'
    data: ItemCategoryData
    id_field = 'item_category_id'

    @staticmethod
    def _build_dataclass(data: CensusData) -> ItemCategoryData:
        return ItemCategoryData.from_census(data)


@dataclasses.dataclass(frozen=True)
class ItemTypeData(Ps2Data):
    """Data class for :class:`auraxium.ps2.item.ItemType`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
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


class ItemType(Cached, cache_size=10, cache_ttu=60.0):
    """A type of item.

    Item types are a coarser classification used internally. They are
    used to differentiate between tangible items like weapons or
    consumables, cosmetics, implants, as well as abstract item-like
    utilities like loadout slots, server transfers, or name change
    tokens.
    """

    collection = 'item_type'
    data: ItemTypeData
    id_field = 'item_type_id'

    @staticmethod
    def _build_dataclass(data: CensusData) -> ItemTypeData:
        return ItemTypeData.from_census(data)


@dataclasses.dataclass(frozen=True)
class ItemData(Ps2Data):
    """Data class for :class:`auraxium.ps2.item.Item`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
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


class Item(Named, cache_size=128, cache_ttu=3600.0):
    """An item that may be owned by a character.

    This includes the item component of weapons, which is extended by
    weapon specific data in the associated
    :class:`auraxium.ps2.weapon.Weapon` instance.
    """

    collection = 'item'
    data: ItemData
    id_field = 'item_id'

    @staticmethod
    def _build_dataclass(data: CensusData) -> ItemData:
        return ItemData.from_census(data)

    def attachments(self) -> SequenceProxy['Item']:
        """Return the attachment options for this item.

        This returns a :class:`auraxium.proxy.SequenceProxy`.
        """
        collection: Final[str] = 'item_attachment'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        query.limit(100)
        join = query.create_join(self.collection)
        join.parent_field = 'attachment_item_id'
        join.child_field = self.id_field
        return SequenceProxy(self.__class__, query, client=self._client)

    def category(self) -> InstanceProxy[ItemCategory]:
        """Return the category of the item.

        This returns an :class:`auraxium.proxy.InstanceProxy`.
        """
        if self.data.item_category_id is None:
            raise ValueError(f'{self} does not define a category')
        query = Query(
            ItemCategory.collection, service_id=self._client.service_id)
        query.add_term(
            field=ItemCategory.id_field, value=self.data.item_category_id)
        return InstanceProxy(ItemCategory, query, client=self._client)

    async def datasheet(self) -> 'WeaponDatasheet':
        """Return the datasheet for the weapon."""
        from .weapon import WeaponDatasheet
        collection: Final[str] = 'weapon_datasheet'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        payload = await run_query(query, session=self._client.session)
        data = extract_single(payload, collection)
        return WeaponDatasheet.from_census(data)

    def profiles(self) -> SequenceProxy[Profile]:
        """Return the profiles the item is available to.

        This returns a :class:`auraxium.proxy.SequenceProxy`.
        """
        collection: Final[str] = 'item_profile'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        query.limit(50)
        join = query.create_join(Profile.collection)
        join.parent_field = join.child_field = Profile.id_field
        return SequenceProxy(Profile, query, client=self._client)

    def type(self) -> InstanceProxy[ItemType]:
        """Return the type of item.

        This returns an :class:`auraxium.proxy.InstanceProxy`.
        """
        if self.data.item_type_id is None:
            raise ValueError(f'{self} does not define a type')
        query = Query(ItemType.collection, service_id=self._client.service_id)
        query.add_term(field=ItemType.id_field, value=self.data.item_type_id)
        return InstanceProxy(ItemType, query, client=self._client)

    def weapon(self) -> InstanceProxy['Weapon']:
        """Return the weapon associated with this item, if any.

        This returns an :class:`auraxium.proxy.InstanceProxy`.
        """
        from .weapon import Weapon
        collection: Final[str] = 'item_to_weapon'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        join = query.create_join('weapon')
        join.parent_field = join.child_field = 'weapon_id'
        return InstanceProxy(Weapon, query, client=self._client)
