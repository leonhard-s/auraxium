"""Data classes for :mod:`auraxium.ps2.effect`."""

from typing import Optional

from ._base import RESTPayload

__all__ = [
    'EffectData',
    'EffectTypeData'
]

# pylint: disable=too-few-public-methods


class EffectData(RESTPayload):
    """Data class for :class:`auraxium.ps2.effect.Effect`.

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
    """Data class for :class:`auraxium.ps2.effect.EffectType`.

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
