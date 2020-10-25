"""Data classes for :mod:`auraxium.ps2.zone_effect`."""

from typing import Optional

from ..base import Ps2Data

__all__ = [
    'ZoneEffectData',
    'ZoneEffectTypeData'
]


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
    param1: Optional[str] = None
    param2: Optional[str] = None
    param3: Optional[str] = None
    param4: Optional[str] = None
    param5: Optional[str] = None
    param6: Optional[str] = None


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
