"""Weapon class definition."""

import logging
from typing import Final, List, Optional

from .._base import Cached
from .._client import Client
from ..census import Query
from ..models import WeaponAmmoSlot, WeaponData, WeaponDatasheet
from .._proxy import InstanceProxy, SequenceProxy
from .._request import extract_payload, extract_single

from .fire import FireGroup
from .item import Item

__all__ = [
    'Weapon',
    'WeaponAmmoSlot',
    'WeaponDatasheet'
]

log = logging.getLogger('auraxium')


class Weapon(Cached, cache_size=128, cache_ttu=3600.0):
    """A weapon available to a player.

    This can be treated as an extension to the
    :class:`auraxium.ps2.Item` class.

    Attributes:
        weapon_id: The unique ID of this weapon.
        weapon_group_id: Used to group upgradable weapons together and
            track them as a single entity, such as the Infiltrator's
            Recon Dart Device or the Engineer's Repair Tool.
        turn_modifier: Turn speed modifier to apply while the weapon is
            equipped.
        move_modifier: Move speed modifier to apply while the weapon is
            equipped.
        sprint_recovery_ms: Recovery time to allow firing or ADS after
            the player stopped sprinting.
        equip_ms: The weapon equip time in milliseconds.
        unequip_ms: The weapon unequip time in milliseconds.
        to_iron_sights_ms: The ADS enter time in milliseconds.
        from_iron_sights_ms: The ADS exit time in milliseconds.
        heat_capacity: The heat capacity of the weapon. Generally
            identical to :attr:`~auraxium.ps2.FireMode.heat_threshold`,
            but this only uses the first fire mode of the weapon.
        heat_bleed_off_rate: The rate at which the weapon will cool
            down after firing stops.
        heat_overheat_penalty_ms: The overheat penalty imposed if the
            user overheats the weapon.
        melee_detect_width: The hitbox width for melee weapons.
        melee_detect_height: The hitbox height for melee weapons.

    """

    collection = 'weapon'
    data: WeaponData
    _dataclass = WeaponData
    id_field = 'weapon_id'

    # Type hints for data class fallback attributes
    weapon_id: int
    weapon_group_id: Optional[int]
    turn_modifier: float
    move_modifier: float
    sprint_recovery_ms: Optional[int]
    equip_ms: Optional[int]
    unequip_ms: Optional[int]
    to_iron_sights_ms: Optional[int]
    from_iron_sights_ms: Optional[int]
    heat_capacity: Optional[int]
    heat_bleed_off_rate: Optional[float]
    heat_overheat_penalty_ms: Optional[int]
    melee_detect_width: Optional[float]
    melee_detect_height: Optional[float]

    @property
    def is_heat_weapon(self) -> bool:
        """Guess whether this weapon is using a heat mechanic.

        This checks for presence and non-zero value for the
        "heat_mechanic" stat.
        """
        if (capacity := self.data.heat_capacity) is not None:
            return capacity > 0
        return False

    async def ammo_slots(self) -> List[WeaponAmmoSlot]:
        """Return the ammo slots for the weapon."""
        collection: Final[str] = 'weapon_ammo_slot'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        query.limit(10).sort('weapon_slot_index')
        payload = await self._client.request(query)
        data = extract_payload(payload, collection)
        return [WeaponAmmoSlot(**d) for d in data]

    def attachments(self) -> SequenceProxy[Item]:
        """Return the attachments available for this weapon.

        This returns a :class:`auraxium.SequenceProxy`.
        """
        collection: Final[str] = 'weapon_to_attachment'
        group_id = self.data.weapon_group_id or -1
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field='weapon_group_id', value=group_id)
        query.limit(100)
        join = query.create_join(Item.collection)
        join.set_fields(Item.id_field)
        join.set_outer(False)
        return SequenceProxy(Item, query, client=self._client)

    async def datasheet(self) -> WeaponDatasheet:
        """Return the datasheet for the weapon."""
        collection: Final[str] = 'weapon_datasheet'
        if (item := await self.item()) is None:
            raise RuntimeError(f'Invalid item for weapon ID: {self.id}')
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=Item.id_field, value=item.id)
        payload = await self._client.request(query)
        data = extract_single(payload, collection)
        return WeaponDatasheet(**data)

    def fire_groups(self) -> SequenceProxy[FireGroup]:
        """Return the fire groups for this weapon.

        This returns a :class:`auraxium.SequenceProxy`.
        """
        collection: Final[str] = 'weapon_to_fire_group'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        query.limit(20)
        join = query.create_join(FireGroup.collection)
        join.set_fields(FireGroup.id_field)
        return SequenceProxy(FireGroup, query, client=self._client)

    @classmethod
    async def get_by_name(cls, name: str, *, locale: str = 'en',
                          client: Client) -> Optional['Weapon']:
        """Retrieve a weapon by name.

        This is a helper method provided as weapons themselves do not
        have a name. This looks up an item by name, then returns the
        weapon associated with this item.

        Returns:
            The weapon associated with the given item, or None

        """
        item = await Item.get_by_name(name, locale=locale, client=client)
        if item is None:
            return None
        return await item.weapon().resolve()

    def item(self) -> InstanceProxy[Item]:
        """Return the item associated with this weapon."""
        query = Query('item_to_weapon', service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        join = query.create_join('item')
        join.set_fields('item_id', None)
        return InstanceProxy(Item, query, client=self._client)
