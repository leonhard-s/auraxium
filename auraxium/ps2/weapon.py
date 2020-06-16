import dataclasses
import logging
from typing import ClassVar, Optional, Tuple

from ..base import Cached, Ps2Data
from ..cache import TLRUCache
from ..types import CensusData

log = logging.getLogger('auraxium')


@dataclasses.dataclass(frozen=True)
class WeaponData(Ps2Data):
    # Required
    weapon_id: int
    weapon_group_id: int
    turn_modifier: float
    move_modifier: float
    sprint_recovery_ms: int
    equip_ms: int
    unequip_ms: int
    to_iron_sights_ms: int
    from_iron_sights_ms: int
    # Optional
    heat_capacity: Optional[int] = None
    heat_bleed_off_rate: Optional[float] = None
    heat_overheat_penalty_ms: Optional[int] = None
    melee_detect_width: Optional[float] = None
    melee_detect_height: Optional[float] = None

    @classmethod
    def populate(cls, payload: CensusData) -> 'WeaponData':
        heat_capacity = payload.get('heat_capacity')
        if heat_capacity is not None:
            heat_capacity = int(heat_capacity)
        heat_bleed_off_rate = payload.get('heat_bleed_off_rate')
        if heat_bleed_off_rate is not None:
            heat_bleed_off_rate = int(heat_bleed_off_rate)
        heat_overheat_penalty_ms = payload.get('heat_overheat_penalty_ms')
        if heat_overheat_penalty_ms is not None:
            heat_overheat_penalty_ms = int(heat_overheat_penalty_ms)
        melee_detect_width = payload.get('melee_detect_width')
        if melee_detect_width is not None:
            melee_detect_width = float(melee_detect_width)
        melee_detect_height = payload.get('melee_detect_height')
        if melee_detect_height is not None:
            melee_detect_height = float(melee_detect_height)
        return cls(
            # Required
            int(payload['weapon_id']),
            int(payload['weapon_group_id']),
            float(payload['turn_modifier']),
            float(payload['move_modifier']),
            int(payload['sprint_recovery_ms']),
            int(payload['equip_ms']),
            int(payload['unequip_ms']),
            int(payload['to_iron_sights_ms']),
            int(payload['from_iron_sights_ms']),
            # Optional
            int(payload['heat_capacity']),
            float(payload['heat_bleed_off_rate']),  # float or int?
            int(payload['heat_overheat_penalty_ms']),
            melee_detect_width,
            melee_detect_height)


class Weapon(Cached, cache_size=128, cache_ttu=3600.0):

    _cache: ClassVar[TLRUCache[int, 'Weapon']]
    data: WeaponData
    _dataclass = WeaponData
    _collection = 'weapon'
    _id_field = 'weapon_id'

    @property
    def equip_times(self) -> Optional[Tuple[float, float]]:
        """Return the equip and unequip times in seconds."""
        equip_time: Optional[int] = self.data.equip_ms
        unequip_time: Optional[int] = self.data.unequip_ms
        if equip_time is None or unequip_time is None:
            return None
        return equip_time / 1000.0, unequip_time / 1000.0

    @property
    def ads_times(self) -> Optional[Tuple[float, float]]:
        """Return the ADS enter and exit times in seconds."""
        enter_ads: Optional[float] = self.data.to_iron_sights_ms
        exit_ads: Optional[float] = self.data.from_iron_sights_ms
        if enter_ads is None or exit_ads is None:
            return None
        return enter_ads / 1000.0, exit_ads / 1000.0

    @property
    def melee_hitbox(self) -> Optional[Tuple[float, float]]:
        """Return the ADS enter and exit times in seconds."""
        width: Optional[float] = self.data.melee_detect_width
        height: Optional[float] = self.data.melee_detect_height
        if width is None or height is None:
            return None
        return width / 1000.0, height / 1000.0

    @property
    def spring_recovery(self) -> Optional[float]:
        """Return the sprint recovery time in seconds."""
        value: Optional[float]
        if (value := self.data.sprint_recovery_ms) is not None:
            value /= 1000.0
        return value

    def _build_dataclass(self, payload: CensusData) -> WeaponData:
        return WeaponData.populate(payload)
