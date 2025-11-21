"""Data classes for :mod:`auraxium.ps2._effect`."""

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
    ability_id: int | None
    target_type_id: int | None
    resist_type_id: int
    is_drain: bool | None
    duration_seconds: float | None
    param1: str | None
    param2: str | None
    param3: str | None
    param4: str | None
    param5: str | None
    param6: str | None
    param7: str | None
    param8: str | None
    param9: str | None
    param10: str | None
    param11: str | None
    param12: str | None
    param13: str | None


class EffectTypeData(RESTPayload):
    """Data class for :class:`auraxium.ps2.EffectType`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    effect_type_id: int
    description: str
    param1: str | None
    param2: str | None
    param3: str | None
    param4: str | None
    param5: str | None
    param6: str | None
    param7: str | None
    param8: str | None
    param9: str | None
    param10: str | None
    param11: str | None
    param12: str | None
    param13: str | None


class ZoneEffectData(RESTPayload):
    """Data class for :class:`auraxium.ps2.ZoneEffect`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    zone_effect_id: int
    zone_effect_type_id: int
    ability_id: int
    param1: str | None = None
    param2: str | None = None
    param3: str | None = None
    param4: str | None = None
    param5: str | None = None
    param6: str | None = None


class ZoneEffectTypeData(RESTPayload):
    """Data class for :class:`auraxium.ps2.ZoneEffectType`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    zone_effect_type_id: int
    description: str
    param1: str | None
    param2: str | None
    param3: str | None
    param4: str | None
    param5: str | None
    param6: str | None
