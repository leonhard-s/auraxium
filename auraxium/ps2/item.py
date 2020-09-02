"""Item and item attachment class definitions."""

import dataclasses
from typing import Final, Optional, TYPE_CHECKING

from ..base import Cached, Named, Ps2Data
from ..census import Query
from ..request import extract_single
from ..proxy import InstanceProxy, SequenceProxy
from ..types import CensusData
from ..utils import LocaleData, optional

from .faction import Faction
from .profile import Profile

if TYPE_CHECKING:
    # This is only imported during static type checking to resolve the forward
    # references. This avoids a circular import at runtime.
    from .weapon import Weapon, WeaponDatasheet


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
        join.set_fields('attachment_item_id', self.id_field)
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

    def description(self, locale: str = 'en') -> str:
        """Return the description of this item in the given locale.

        This will return "Missing String" if no string has been set for
        the selected locale.
        """
        if hasattr(self.data.description, locale):
            return str(getattr(self.data.description, locale))
        return 'Missing String'

    def faction(self) -> InstanceProxy[Faction]:
        """Return the faction that has access to this item.

        This returns an :class:`auraxium.proxy.InstanceProxy`.
        """
        value = self.data.faction_id or -1
        query = Query(Faction.collection, service_id=self._client.service_id)
        query.add_term(field=Faction.id_field, value=value)
        return InstanceProxy(Faction, query, client=self._client)

    async def datasheet(self) -> 'WeaponDatasheet':
        """Return the datasheet for the weapon."""
        from .weapon import WeaponDatasheet
        collection: Final[str] = 'weapon_datasheet'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        payload = await self._client.request(query)
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
        join.set_fields(Profile.id_field)
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
        join.set_fields('weapon_id')
        return InstanceProxy(Weapon, query, client=self._client)
