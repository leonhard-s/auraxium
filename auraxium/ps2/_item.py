"""Item and item attachment class definitions."""

from typing import Final, Optional, TYPE_CHECKING

from ..base import Cached, ImageMixin, Named
from ..census import Query
from ..models import ItemCategoryData, ItemData, ItemTypeData
from .._rest import extract_single
from .._proxy import InstanceProxy, SequenceProxy
from ..types import LocaleData

from ._faction import Faction
from ._profile import Profile

if TYPE_CHECKING:  # pragma: no cover
    # This is only imported during static type checking to resolve the forward
    # references. This avoids a circular import at runtime.
    from ._weapon import Weapon, WeaponDatasheet

__all__ = [
    'Item',
    'ItemCategory',
    'ItemType'
]


class ItemCategory(Named, cache_size=32, cache_ttu=3600.0):
    """A category of item.

    This represents the item filter views used in the in-game depot,
    such as "Infantry Gear", "Weapon Camo" or "Vehicle Weapons".

    .. attribute:: id
       :type: int

       The unique ID of this item category. In the API payload, this
       field is called ``item_category_id``.

    .. attribute:: name
       :type: auraxium.types.LocaleData

       Localised name of the item category.
    """

    collection = 'item_category'
    data: ItemCategoryData
    id_field = 'item_category_id'
    _model = ItemCategoryData

    # Type hints for data class fallback attributes
    id: int
    name: LocaleData


class ItemType(Cached, cache_size=10, cache_ttu=60.0):
    """A type of item.

    Item types are a coarser classification used internally. They are
    used to differentiate between tangible items like weapons or
    consumables, cosmetics, implants, as well as abstract item-like
    utilities like loadout slots, server transfers, or name change
    tokens.

    .. attribute:: id
       :type: int

       The unique ID of this item type. In the API payload, this field
       is called ``item_type_id``.

    .. attribute:: name
       :type: str

       The internal identifying name of this item type.

    .. attribute:: code
       :type: str

       The internal code used to describe this item type.
    """

    collection = 'item_type'
    data: ItemTypeData
    id_field = 'item_type_id'
    _model = ItemTypeData

    # Type hints for data class fallback attributes
    id: int
    name: str
    code: str


class Item(Named, ImageMixin, cache_size=128, cache_ttu=3600.0):
    """An item that may be owned by a character.

    This includes the item component of weapons, which is extended by
    weapon specific data in the associated
    :class:`auraxium.ps2.Weapon` instance.

    .. attribute:: id
       :type: int

       The unique ID of this item. In the API payload, this field is
       called ``item_id``.

    .. attribute:: item_type_id
       :type: int | None

       The ID of the :class:`~auraxium.ps2.ItemType` for this item.

       .. seealso::

          :meth:`type` -- Retrieve the type of this item.

    .. attribute:: item_category_id
       :type: int | None

       The ID of the :class:`~auraxium.ps2.ItemCategory` for this item.

       .. seealso::

          :meth:`category` -- Retrieve the category of this item.

    .. attribute:: activatable_ability_id
       :type: int | None

       (Not yet documented)

    .. attribute:: passive_ability_id
       :type: int | None

       (Not yet documented)

    .. attribute:: is_vehicle_weapon
       :type: bool

       Whether this item is a vehicle weapon.

    .. attribute:: description
       :type: auraxium.types.LocaleData | None

       Localised description of the item.

    .. attribute:: faction_id
       :type: int | None

       The :class:`~auraxium.ps2.Faction` that has access to this item.

    .. attribute:: max_stack_size
       :type: int

       The stack size for stackable items such as grenades.

    .. attribute:: name
       :type: auraxium.types.LocaleData

       Localised name of the item.

    .. attribute:: skill_set_id
       :type: int | None

       The :class:`~auraxium.ps2.SkillSet` associated with this item.
       This is used for upgradable items like the Medical Applicator or
       Repair Tool.

    .. attribute:: is_default_attachment
       :type: bool

       Default attachments are generally not visible to the user and
       are used whenever nothing is selected. Examples include the
       default iron sights, or the regular ammo type for weapon
       supporting non-standard ammo types.
    """

    collection = 'item'
    data: ItemData
    id_field = 'item_id'
    _model = ItemData

    # Type hints for data class fallback attributes
    id: int
    item_type_id: Optional[int]
    item_category_id: Optional[int]
    activatable_ability_id: Optional[int]
    passive_ability_id: Optional[int]
    is_vehicle_weapon: bool
    description: Optional[LocaleData]
    faction_id: Optional[int]
    max_stack_size: int
    name: LocaleData
    skill_set_id: Optional[int]
    is_default_attachment: bool

    def attachments(self) -> SequenceProxy['Item']:
        """Return the attachment options for this item.

        This returns a :class:`auraxium.SequenceProxy`.
        """
        collection: Final[str] = 'item_attachment'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        query.limit(100)
        join = query.create_join(self.collection)
        join.set_fields('attachment_item_id', self.id_field)
        return SequenceProxy(Item, query, client=self._client)

    def category(self) -> InstanceProxy[ItemCategory]:
        """Return the category of the item.

        This returns an :class:`auraxium.InstanceProxy`.
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

        This returns an :class:`auraxium.InstanceProxy`.
        """
        value = self.data.faction_id or -1
        query = Query(Faction.collection, service_id=self._client.service_id)
        query.add_term(field=Faction.id_field, value=value)
        return InstanceProxy(Faction, query, client=self._client)

    async def datasheet(self) -> 'WeaponDatasheet':
        """Return the datasheet for the weapon."""
        # pylint: disable=import-outside-toplevel
        from ._weapon import WeaponDatasheet
        collection: Final[str] = 'weapon_datasheet'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        payload = await self._client.request(query)
        data = extract_single(payload, collection)
        return WeaponDatasheet(**data)

    def profiles(self) -> SequenceProxy[Profile]:
        """Return the profiles the item is available to.

        This returns a :class:`auraxium.SequenceProxy`.
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

        This returns an :class:`auraxium.InstanceProxy`.
        """
        if self.data.item_type_id is None:
            raise ValueError(f'{self} does not define a type')
        query = Query(ItemType.collection, service_id=self._client.service_id)
        query.add_term(field=ItemType.id_field, value=self.data.item_type_id)
        return InstanceProxy(ItemType, query, client=self._client)

    def weapon(self) -> InstanceProxy['Weapon']:
        """Return the weapon associated with this item, if any.

        This returns an :class:`auraxium.InstanceProxy`.
        """
        from ._weapon import Weapon  # pylint: disable=import-outside-toplevel
        collection: Final[str] = 'item_to_weapon'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        join = query.create_join('weapon')
        join.set_fields('weapon_id')
        return InstanceProxy(Weapon, query, client=self._client)
