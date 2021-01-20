"""Item and item attachment class definitions."""

from typing import Final, Optional, TYPE_CHECKING

from ..base import Cached, ImageMixin, Named
from ..census import Query
from ..models import ItemCategoryData, ItemData, ItemTypeData
from ..request import extract_single
from ..proxy import InstanceProxy, SequenceProxy
from ..types import LocaleData

from .faction import Faction
from .profile import Profile

if TYPE_CHECKING:
    # This is only imported during static type checking to resolve the forward
    # references. This avoids a circular import at runtime.
    from .weapon import Weapon, WeaponDatasheet  # pragma: no cover

__all__ = [
    'Item',
    'ItemCategory',
    'ItemType'
]


class ItemCategory(Named, cache_size=32, cache_ttu=3600.0):
    """A category of item.

    This represents the item filter views used in the in-game depot,
    such as "Infantry Gear", "Weapon Camo" or "Vehicle Weapons".

    Attributes:
        item_category_id: The unique ID of this item category.
        name: The localised name of the category.

    """

    collection = 'item_category'
    data: ItemCategoryData
    dataclass = ItemCategoryData
    id_field = 'item_category_id'

    # Type hints for data class fallback attributes
    item_category_id: int
    name: LocaleData


class ItemType(Cached, cache_size=10, cache_ttu=60.0):
    """A type of item.

    Item types are a coarser classification used internally. They are
    used to differentiate between tangible items like weapons or
    consumables, cosmetics, implants, as well as abstract item-like
    utilities like loadout slots, server transfers, or name change
    tokens.

    Attributes:
        item_type_id: The unique ID of this item type.
        name: The identifying name of this item type.
        code: The internal code used to describe this item type.

    """

    collection = 'item_type'
    data: ItemTypeData
    dataclass = ItemTypeData
    id_field = 'item_type_id'

    # Type hints for data class fallback attributes
    item_type_id: int
    name: str
    code: str


class Item(Named, ImageMixin, cache_size=128, cache_ttu=3600.0):
    """An item that may be owned by a character.

    This includes the item component of weapons, which is extended by
    weapon specific data in the associated
    :class:`auraxium.ps2.weapon.Weapon` instance.

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

    collection = 'item'
    data: ItemData
    dataclass = ItemData
    id_field = 'item_id'

    # Type hints for data class fallback attributes
    item_id: int
    item_type_id: Optional[int]
    item_category_id: Optional[int]
    activatable_ability_id: Optional[int]
    passive_ability_id: Optional[int]
    is_vehicle_weapon: bool
    name: LocaleData
    description: Optional[LocaleData]
    faction_id: Optional[int]
    max_stack_size: int
    skill_set_id: Optional[int]
    is_default_attachment: bool

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
        # pylint: disable=import-outside-toplevel
        from .weapon import WeaponDatasheet
        collection: Final[str] = 'weapon_datasheet'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        payload = await self._client.request(query)
        data = extract_single(payload, collection)
        return WeaponDatasheet(**data)

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
        from .weapon import Weapon  # pylint: disable=import-outside-toplevel
        collection: Final[str] = 'item_to_weapon'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        join = query.create_join('weapon')
        join.set_fields('weapon_id')
        return InstanceProxy(Weapon, query, client=self._client)
