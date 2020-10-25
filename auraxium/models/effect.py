"""Data classes for :mod:`auraxium.ps2.effect`."""

from typing import Optional

from ..base import Ps2Data

__all__ = [
    'EffectData',
    'EffectTypeData'
]


class EffectData(Ps2Data):
    """Data class for :class:`auraxium.ps2.effect.Effect`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        effect_id: The unique ID of this effect.
        effect_type_id: The associated effect type for this effect.
        ability_id: The ability spawning the effect, if any.
        target_type_id: Integer value of the :class:`TargetType`
            enumerator used to find targets for this effect.
        resist_type_id: The :class:`~auraxium.ps2.ResistInfo` entry
            used by this effect.
        is_drain: (Not yet documented)
        duration_seconds: The duration of the effect.
        param*: Type-specific parameters for this effect. Refer to the
            corresponding :class:`EffectType` for details.

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


class EffectTypeData(Ps2Data):
    """Data class for :class:`auraxium.ps2.effect.EffectType`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        effect_type_id: The unique ID of this effect type.
        description: A description of what this effect type is used
            for.
        param*: Descriptions of what the corresponding parameter is
            used for in abilities of this type.

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
