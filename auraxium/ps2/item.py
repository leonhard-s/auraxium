"""Item and item attachment class definitions."""

from typing import Final, TYPE_CHECKING

from ..base import Cached, Named
from ..census import Query
from ..models import ItemCategoryData, ItemData, ItemTypeData
from ..request import extract_single
from ..proxy import InstanceProxy, SequenceProxy
from ..types import CensusData

from .faction import Faction
from .profile import Profile

if TYPE_CHECKING:
    # This is only imported during static type checking to resolve the forward
    # references. This avoids a circular import at runtime.
    from .weapon import Weapon, WeaponDatasheet


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
        # pylint: disable=import-outside-toplevel
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
        from .weapon import Weapon  # pylint: disable=import-outside-toplevel
        collection: Final[str] = 'item_to_weapon'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        join = query.create_join('weapon')
        join.set_fields('weapon_id')
        return InstanceProxy(Weapon, query, client=self._client)
