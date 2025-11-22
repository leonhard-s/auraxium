"""Data classes for :mod:`auraxium.ps2._ability`."""

from .base import RESTPayload

__all__ = [
    'AbilityData',
    'AbilityTypeData',
    'ResourceTypeData'
]


class AbilityData(RESTPayload):
    """Data class for :class:`auraxium.ps2.Ability`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    ability_id: int
    ability_type_id: int
    expire_msec: int | None = None
    first_use_delay_msec: int | None = None
    next_use_delay_msec: int | None = None
    reuse_delay_msec: int | None = None
    resource_type_id: int | None = None
    resource_first_cost: int | None = None
    resource_cost_per_msec: int | None = None
    distance_max: float | None = None
    radius_max: float | None = None
    flag_toggle: bool | None = None
    param1: str | None = None
    param2: str | None = None
    param3: str | None = None
    param4: str | None = None
    param5: str | None = None
    param6: str | None = None
    param7: str | None = None
    param8: str | None = None
    param9: str | None = None
    param10: str | None = None
    param11: str | None = None
    param12: str | None = None
    param13: str | None = None
    param14: str | None = None
    string1: str | None = None
    string2: str | None = None
    string3: str | None = None
    string4: str | None = None


class AbilityTypeData(RESTPayload):
    """Data class for :class:`auraxium.ps2.AbilityType`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    ability_type_id: int
    description: str | None = None
    param1: str | None = None
    param2: str | None = None
    param3: str | None = None
    param4: str | None = None
    param5: str | None = None
    param6: str | None = None
    param7: str | None = None
    param8: str | None = None
    param9: str | None = None
    param10: str | None = None
    param11: str | None = None
    param12: str | None = None
    param13: str | None = None
    param14: str | None = None
    string1: str | None = None
    string2: str | None = None
    string3: str | None = None
    string4: str | None = None


class ResourceTypeData(RESTPayload):
    """Data class for :class:`auraxium.ps2.ResourceType`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    resource_type_id: int
    description: str
