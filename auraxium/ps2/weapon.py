"""Weapon class definition."""

import dataclasses
import logging
from typing import Final, List, Optional

from ..base import Cached, Ps2Data
from ..client import Client
from ..census import Query
from ..proxy import InstanceProxy, SequenceProxy
from ..request import extract_payload, extract_single, run_query
from ..types import CensusData
from ..utils import LocaleData, optional

from .fire import FireGroup
from .item import Item

log = logging.getLogger('auraxium')


@dataclasses.dataclass(frozen=True)
class WeaponAmmoSlot(Ps2Data):
    """Data class for weapon ammo slot data.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    weapon_id: int
    weapon_slot_index: int
    clip_size: int
    capacity: int
    refill_ammo_rate: Optional[int]
    refill_ammo_delay_ms: Optional[int]

    @classmethod
    def from_census(cls, data: CensusData) -> 'WeaponAmmoSlot':
        return cls(
            int(data['weapon_id']),
            int(data['weapon_slot_index']),
            int(data['clip_size']),
            int(data['capacity']),
            optional(data, 'refill_ammo_rate', int),
            optional(data, 'refill_ammo_delay_ms', int))


@dataclasses.dataclass(frozen=True)
class WeaponDatasheet(Ps2Data):
    """Data class for weapon datasheets.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    item_id: int
    direct_damage: Optional[int]
    indirect_damage: Optional[int]
    damage: int
    damage_min: int
    damage_max: int
    fire_cone: float
    fire_cone_min: float
    fire_cone_max: float
    fire_rate_ms: int
    fire_rate_ms_min: int
    fire_rate_mx_max: int
    reload_ms: int
    reload_ms_min: int
    reload_ms_max: int
    clip_size: int
    capacity: int
    range: LocaleData
    show_clip_size: bool
    show_fire_modes: bool
    show_range: bool

    @classmethod
    def from_census(cls, data: CensusData) -> 'WeaponDatasheet':
        return cls(
            int(data['item_id']),
            optional(data, 'direct_damage', int),
            optional(data, 'indirect_damage', int),
            int(data['damage']),
            int(data['damage_min']),
            int(data['damage_max']),
            float(data['fire_cone']),
            float(data['fire_cone_min']),
            float(data['fire_cone_max']),
            int(data['fire_rate_ms']),
            int(data['fire_rate_ms_min']),
            int(data['fire_rate_mx_max']),  # The "mx" is not a typo - not mine
            int(data['reload_ms']),
            int(data['reload_ms_min']),
            int(data['reload_ms_max']),
            int(data['clip_size']),
            int(data['capacity']),
            LocaleData.from_census(data['range']),
            bool(int(data['show_clip_size'])),
            bool(int(data['show_fire_modes'])),
            bool(int(data['show_range'])))


@dataclasses.dataclass(frozen=True)
class WeaponData(Ps2Data):
    """Data class for :class:`auraxium.ps2.ability.Weapon`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    weapon_id: int
    weapon_group_id: Optional[int]
    turn_modifier: float
    move_modifier: float
    sprint_recovery_ms: Optional[int]
    equip_ms: Optional[int]
    unequip_ms: Optional[int]
    to_iron_sights_ms: Optional[int]
    from_iron_sights_ms: Optional[int]
    heat_capacity: Optional[int] = None
    heat_bleed_off_rate: Optional[float] = None
    heat_overheat_penalty_ms: Optional[int] = None
    melee_detect_width: Optional[float] = None
    melee_detect_height: Optional[float] = None

    @classmethod
    def from_census(cls, data: CensusData) -> 'WeaponData':
        return cls(
            int(data['weapon_id']),
            optional(data, 'weapon_group_id', int),
            float(data['turn_modifier']),
            float(data['move_modifier']),
            optional(data, 'sprint_recovery_ms', int),
            optional(data, 'equip_ms', int),
            optional(data, 'unequip_ms', int),
            optional(data, 'to_iron_sights_ms', int),
            optional(data, 'from_iron_sights_ms', int),
            optional(data, 'heat_capacity', int),
            optional(data, 'heat_bleed_off_rate_ms', int),
            optional(data, 'heat_overhead_penalty_ms', int),
            optional(data, 'melee_detect_width', float),
            optional(data, 'melee_detect_height', float))


class Weapon(Cached, cache_size=128, cache_ttu=3600.0):
    """A weapon available to a player.

    This can be treated as an extension to the
    :class:`auraxium.ps2.item.Item` class.
    """

    collection = 'weapon'
    data: WeaponData
    id_field = 'weapon_id'

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
        payload = await run_query(query, session=self._client.session)
        data = extract_payload(payload, collection)
        return [WeaponAmmoSlot.from_census(d) for d in data]

    def attachments(self) -> SequenceProxy[Item]:
        """Return the attachments available for this weapon.

        This returns a :class:`auraxium.proxy.SequenceProxy`.
        """
        collection: Final[str] = 'weapon_to_attachment'
        group_id = self.data.weapon_group_id or -1
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field='weapon_group_id', value=group_id)
        query.limit(100)
        join = query.create_join(Item.collection)
        join.parent_field = join.child_field = Item.id_field
        join.set_outer(False)
        return SequenceProxy(Item, query, client=self._client)

    @staticmethod
    def _build_dataclass(data: CensusData) -> WeaponData:
        return WeaponData.from_census(data)

    async def datasheet(self) -> WeaponDatasheet:
        """Return the datasheet for the weapon."""
        collection: Final[str] = 'weapon_datasheet'
        if (item := await self.item()) is None:
            raise RuntimeError(f'Invalid item for weapon ID: {self.id}')
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=Item.id_field, value=item.id)
        payload = await run_query(query, session=self._client.session)
        data = extract_single(payload, collection)
        return WeaponDatasheet.from_census(data)

    def fire_groups(self) -> SequenceProxy[FireGroup]:
        """Return the fire groups for this weapon.

        This returns a :class:`auraxium.proxy.SequenceProxy`.
        """
        collection: Final[str] = 'weapon_to_fire_group'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        query.limit(20)
        join = query.create_join(FireGroup.collection)
        join.parent_field = join.child_field = FireGroup.id_field
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
        join.parent_field = 'item_id'
        return InstanceProxy(Item, query, client=self._client)
