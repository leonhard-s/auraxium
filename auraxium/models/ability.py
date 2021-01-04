"""Data classes for :mod:`auraxium.ps2.ability`."""

from typing import Optional

from ..base import Ps2Data

__all__ = [
    'AbilityData',
    'AbilityTypeData',
    'ResourceTypeData'
]

# pylint: disable=too-few-public-methods


class AbilityData(Ps2Data):
    """Data class for :class:`auraxium.ps2.ability.Ability`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        ability_id: The unique ID of this ability.
        ability_type_id: The associated ability type for this ability.
        expire_msec: The duration of the ability.
        first_use_delay_msec: The initial cooldown of the ability.
        next_use_delay_msec: The reuse cooldown of the ability.
        resource_type_id: The resource type used by the ability.
        resource_first_cost: The initial cast cost of the ability.
        resource_cost_per_msec: The resource cost per second for
            toggled abilities.
        distance_max: (Not yet documented)
        radius_max: (Not yet documented)
        flag_toggle: Whether the ability is toggled.
        param*: Type-specific parameters for this ability. Refer to the
            corresponding :class:`AbilityType` for details.
        string*: Type-specific string values for this ability. Refer to
            the corresponding :class:`AbilityType` for details.

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


class AbilityTypeData(Ps2Data):
    """Data class for :class:`auraxium.ps2.ability.AbilityType`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        ability_type_id: The unique ID for this ability type.
        description: A description of what this ability type is used
            for.
        param*: Descriptions of what the corresponding parameter is
            used for in abilities of this type.
        string*: Descriptions of what the corresponding string value is
            used for in abilities of this type.

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


class ResourceTypeData(Ps2Data):
    """Data class for :class:`auraxium.ps2.ability.ResourceType`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        resource_type_id: The unique ID of this resource type.
        description: A description of what this resource type is used
            for.

    """

    resource_type_id: int
    description: str
