"""Data classes for :mod:`auraxium.ps2._effect`."""

from typing import Optional

from .base import RESTPayload

__all__ = [
    'EffectData',
    'EffectTypeData',
    'ZoneEffectData',
    'ZoneEffectTypeData'
]


class EffectData(RESTPayload):
    """Data class for :class:`auraxium.ps2.Effect`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    effect_id: int
    effect_type_id: int
    ability_id: Optional[int]
    target_type_id: Optional[int]
    resist_type_id: int
    is_drain: Optional[bool]
    duration_seconds: Optional[float]
    param1: Optional[str]
    param2: Optional[str]
    param3: Optional[str]
    param4: Optional[str]
    param5: Optional[str]
    param6: Optional[str]
    param7: Optional[str]
    param8: Optional[str]
    param9: Optional[str]
    param10: Optional[str]
    param11: Optional[str]
    param12: Optional[str]
    param13: Optional[str]


class EffectTypeData(RESTPayload):
    """Data class for :class:`auraxium.ps2.EffectType`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    effect_type_id: int
    description: str
    param1: Optional[str]
    param2: Optional[str]
    param3: Optional[str]
    param4: Optional[str]
    param5: Optional[str]
    param6: Optional[str]
    param7: Optional[str]
    param8: Optional[str]
    param9: Optional[str]
    param10: Optional[str]
    param11: Optional[str]
    param12: Optional[str]
    param13: Optional[str]


class ZoneEffectData(RESTPayload):
    """Data class for :class:`auraxium.ps2.ZoneEffect`.

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


class ZoneEffectTypeData(RESTPayload):
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
