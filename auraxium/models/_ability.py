"""Data classes for :mod:`auraxium.ps2.ability`."""

from typing import Optional

from ._base import RESTPayload

__all__ = [
    'AbilityData',
    'AbilityTypeData',
    'ResourceTypeData'
]

# pylint: disable=too-few-public-methods


class AbilityData(RESTPayload):
    """Data class for :class:`auraxium.ps2.ability.Ability`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    """

    ability_id: int
    ability_type_id: int
    expire_msec: Optional[int] = None
    first_use_delay_msec: Optional[int] = None
    next_use_delay_msec: Optional[int] = None
    reuse_delay_msec: Optional[int] = None
    resource_type_id: Optional[int] = None
    resource_first_cost: Optional[int] = None
    resource_cost_per_msec: Optional[int] = None
    distance_max: Optional[float] = None
    radius_max: Optional[float] = None
    flag_toggle: Optional[bool] = None
    param1: Optional[str] = None
    param2: Optional[str] = None
    param3: Optional[str] = None
    param4: Optional[str] = None
    param5: Optional[str] = None
    param6: Optional[str] = None
    param7: Optional[str] = None
    param8: Optional[str] = None
    param9: Optional[str] = None
    param10: Optional[str] = None
    param11: Optional[str] = None
    param12: Optional[str] = None
    param13: Optional[str] = None
    param14: Optional[str] = None
    string1: Optional[str] = None
    string2: Optional[str] = None
    string3: Optional[str] = None
    string4: Optional[str] = None


class AbilityTypeData(RESTPayload):
    """Data class for :class:`auraxium.ps2.ability.AbilityType`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    """

    ability_type_id: int
    description: Optional[str] = None
    param1: Optional[str] = None
    param2: Optional[str] = None
    param3: Optional[str] = None
    param4: Optional[str] = None
    param5: Optional[str] = None
    param6: Optional[str] = None
    param7: Optional[str] = None
    param8: Optional[str] = None
    param9: Optional[str] = None
    param10: Optional[str] = None
    param11: Optional[str] = None
    param12: Optional[str] = None
    param13: Optional[str] = None
    param14: Optional[str] = None
    string1: Optional[str] = None
    string2: Optional[str] = None
    string3: Optional[str] = None
    string4: Optional[str] = None


class ResourceTypeData(RESTPayload):
    """Data class for :class:`auraxium.ps2.ability.ResourceType`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    """

    resource_type_id: int
    description: str
