"""Data classes for :mod:`auraxium.ps2.ability`."""

import dataclasses
from typing import List, Optional

from ..base import Ps2Data
from ..types import CensusData
from ..utils import optional

__all__ = [
    'AbilityData',
    'AbilityTypeData',
    'ResourceTypeData'
]


@dataclasses.dataclass(frozen=True)
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
    expire_msec: Optional[int]
    first_use_delay_msec: Optional[int]
    next_use_delay_msec: Optional[int]
    reuse_delay_msec: Optional[int]
    resource_type_id: Optional[int]
    resource_first_cost: Optional[int]
    resource_cost_per_msec: Optional[int]
    distance_max: Optional[float]
    radius_max: Optional[float]
    flag_toggle: Optional[bool]
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
    param14: Optional[str]
    string1: Optional[str]
    string2: Optional[str]
    string3: Optional[str]
    string4: Optional[str]

    @classmethod
    def from_census(cls, data: CensusData) -> 'AbilityData':
        params: List[Optional[str]] = [
            optional(data, f'param{i+1}', str) for i in range(14)]
        strings: List[Optional[str]] = [
            optional(data, f'string{i+1}', str) for i in range(4)]
        return cls(
            int(data.pop('ability_id')),
            int(data.pop('ability_type_id')),
            optional(data, 'expire_msec', int),
            optional(data, 'first_use_delay_msec', int),
            optional(data, 'next_use_delay_msec', int),
            optional(data, 'reuse_delay_msec', int),
            optional(data, 'resource_type_id', int),
            optional(data, 'resource_first_cost', int),
            optional(data, 'resource_cost_per_msec', int),
            optional(data, 'distance_max', float),
            optional(data, 'radius_max', float),
            optional(data, 'flag_toggle', bool),
            *params,
            *strings)


@dataclasses.dataclass(frozen=True)
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
    description: Optional[str]
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
    param14: Optional[str]
    string1: Optional[str]
    string2: Optional[str]
    string3: Optional[str]
    string4: Optional[str]

    @classmethod
    def from_census(cls, data: CensusData) -> 'AbilityTypeData':
        params: List[Optional[str]] = [
            optional(data, f'param{i+1}', str) for i in range(14)]
        strings: List[Optional[str]] = [
            optional(data, f'string{i+1}', str) for i in range(4)]
        return cls(
            int(data.pop('ability_type_id')),
            optional(data, 'description', str),
            *params,
            *strings)


@dataclasses.dataclass(frozen=True)
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

    @classmethod
    def from_census(cls, data: CensusData) -> 'ResourceTypeData':
        return cls(
            int(data.pop('resource_type_id')),
            str(data.pop('description')))
