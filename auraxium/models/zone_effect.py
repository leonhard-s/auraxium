"""Data classes for :mod:`auraxium.ps2.zone_effect`."""

from typing import Optional

from .._base import Ps2Data

__all__ = [
    'ZoneEffectData',
    'ZoneEffectTypeData'
]

# pylint: disable=too-few-public-methods


class ZoneEffectData(Ps2Data):
    """Data class for :class:`auraxium.ps2.ZoneEffectData`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    zone_effect_id: int
    zone_effect_type_id: int
    ability_id: int
    param1: Optional[str] = None
    param2: Optional[str] = None
    param3: Optional[str] = None
    param4: Optional[str] = None
    param5: Optional[str] = None
    param6: Optional[str] = None


class ZoneEffectTypeData(Ps2Data):
    """Data class for :class:`auraxium.ps2.ZoneEffectType`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    zone_effect_type_id: int
    description: str
    param1: Optional[str]
    param2: Optional[str]
    param3: Optional[str]
    param4: Optional[str]
    param5: Optional[str]
    param6: Optional[str]
