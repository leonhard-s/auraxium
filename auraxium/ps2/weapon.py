"""Weapon class definition."""

import dataclasses
import logging
from typing import Final, List, Optional

from ..base import Cached, Ps2Data
from ..client import Client
from ..census import Query
from ..proxy import InstanceProxy, SequenceProxy
from ..request import extract_payload, extract_single
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

    Attributes:
        weapon_id: The ID of the associated :class:`Weapon`.
        weapon_slot_index: The position of the ammo type in the list of
            ammo types.
        clip_size: The clip size for this ammo type.
        capacity: The maximum amount of ammo that can be held with this
            ammo type.
        refill_ammo_rate: The amount of ammo being replenished every
            ammo refill tick.
        refill_ammo_delay_ms: The time between two ammo replenishment
            ticks.

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

    .. note::
        The data found herein is generally less reliable than the
        sources it was collected from, such as
        :class:`~auraxium.ps2.FireMode` or
        :class:`~auraxium.ps2.Projectile`.

        This data is mostly used for display in the depot and may not
        be inaccurate.

    Attributes:
        item_id: The item the datasheet is for.
        direct_damage: The direct damage amount.
        indirect_damage: The indirect damage amount.
        damage: (Not yet documented)
        damage_min: (Not yet documented)
        damage_max: (Not yet documented)
        fire_cone: (Not yet documented)
        fire_cone_min: (Not yet documented)
        fire_cone_max: (Not yet documented)
        fire_rate_ms: (Not yet documented)
        fire_rate_ms_min: (Not yet documented)
        fire_rate_mx_max: (Not yet documented)
        reload_ms: (Not yet documented)
        reload_ms_min: (Not yet documented)
        reload_ms_max: (Not yet documented)
        clip_size: The clip size for the default ammo type
        capacity: The total ammo capacity for the default ammo type
        range: The localised description of the weapon range (i.e.
            "Medium", "Long", etc.).
        show_clip_size: Whether to display the clip size data to the
            user.
        show_fire_modes: Whether to display the list of fire modes to
            the user.
        show_range: Whether to display the :attr:`range` data to the
            user.

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
            identical to :attr:`~auraxium.ps2.FireMode.heat_treshold`,
            but this only uses the first fire mode of the weapon.
        heat_bleed_off_rate: The rate at which the weapon will cool
            down after firing stops.
        heat_overheat_penalty_ms: The overheat penalty imposed if the
            user overheats the weapon.
        melee_detect_width: The hitbox width for melee weapons.
        melee_detect_height: The hitbox height for melee weapons.

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
        payload = await self._client.request(query)
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
        payload = await self._client.request(query)
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
