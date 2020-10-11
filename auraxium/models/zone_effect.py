"""Data classes for :mod:`auraxium.ps2.zone_effect`."""

import dataclasses
from typing import List, Optional

from ..base import Ps2Data
from ..types import CensusData, optional

__all__ = [
    'ZoneEffectData',
    'ZoneEffectTypeData'
]


@dataclasses.dataclass(frozen=True)
class ZoneEffectData(Ps2Data):
    """Data class for :class:`auraxium.ps2.zone_effect.ZoneEffectData`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        zone_effect_id: The unique ID of this zone effect.
        zone_effect_type_id: The ID of the associated
            :class:`ZoneEffectType`.
        ability_id: The :class:`~auraxium.ps2.Ability` associated with
            this zone effect.
        param*: Type-specific parameters for this zone effect. Refer to
            the corresponding :class:`ZoneEffectType` for details.

    """

    zone_effect_id: int
    zone_effect_type_id: int
    ability_id: int
    param1: Optional[str]
    param2: Optional[str]
    param3: Optional[str]
    param4: Optional[str]
    param5: Optional[str]
    param6: Optional[str]

    @classmethod
    def from_census(cls, data: CensusData) -> 'ZoneEffectData':
        params: List[Optional[str]] = [
            optional(data, f'param{i+1}', str) for i in range(6)]
        return cls(
            int(data.pop('zone_effect_id')),
            int(data.pop('zone_effect_type_id')),
            int(data.pop('ability_id')),
            *params)


@dataclasses.dataclass(frozen=True)
class ZoneEffectTypeData(Ps2Data):
    """Data class for :class:`auraxium.ps2.zone_effect.ZoneEffectType`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        zone_effect_type_id: The unique ID of this zone effect type.
        description: A description of what this zone effect type is
            used for.
        param*: Descriptions of what the corresponding parameter is
            used for in zone effects of this type.

    """

    zone_effect_type_id: int
    description: str
    param1: str
    param2: str
    param3: str
    param4: str
    param5: str
    param6: str

    @classmethod
    def from_census(cls, data: CensusData) -> 'ZoneEffectTypeData':
        params: List[str] = [str(data[f'param{i+1}']) for i in range(6)]
        return cls(
            int(data.pop('zone_effect_type_id')),
            str(data.pop('description')),
            *params)
