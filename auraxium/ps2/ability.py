"""Ability and ability type class definitions."""

import dataclasses
from typing import List, Optional

from ..base import Cached, Ps2Data
from ..census import Query
from ..proxy import InstanceProxy
from ..types import CensusData
from ..utils import optional


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
            int(data['resource_type_id']),
            str(data['description']))


class ResourceType(Cached, cache_size=50, cache_ttu=3600.0):
    """A type of resource consumed by an ability."""

    collection = 'resource_type'
    data: ResourceTypeData
    id_field = 'resource_type_id'

    @property
    def description(self) -> str:
        """A description of what this resource type is used for."""
        return self.data.description

    @staticmethod
    def _build_dataclass(data: CensusData) -> ResourceTypeData:
        return ResourceTypeData.from_census(data)


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
            int(data['ability_type_id']),
            optional(data, 'description', str),
            *params,
            *strings)


class AbilityType(Cached, cache_size=20, cache_ttu=60.0):
    """A type of ability.

    This class mostly specifies the purpose of any generic parameters.
    """

    collection = 'ability_type'
    data: AbilityTypeData
    id_field = 'ability_type_id'

    @staticmethod
    def _build_dataclass(data: CensusData) -> AbilityTypeData:
        return AbilityTypeData.from_census(data)


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
            int(data['ability_id']),
            int(data['ability_type_id']),
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


class Ability(Cached, cache_size=10, cache_ttu=60.0):
    """An ability cast by a character.

    Access the corresponding :class:`auraxium.ps2.ability.AbilityType`
    instance via the :meth:`type` method for information on generic
    parameters.
    """

    collection = 'ability'
    data: AbilityData
    id_field = 'ability_id'

    @staticmethod
    def _build_dataclass(data: CensusData) -> AbilityData:
        return AbilityData.from_census(data)

    def resource_type(self) -> InstanceProxy[ResourceType]:
        """Return the resource type used by this ability, if any."""
        type_id = self.data.resource_type_id or -1
        query = Query(
            ResourceType.collection, service_id=self._client.service_id)
        query.add_term(field=ResourceType.id_field, value=type_id)
        return InstanceProxy(ResourceType, query, client=self._client)

    def type(self) -> InstanceProxy[AbilityType]:
        """Return the ability type of this ability."""
        query = Query(
            AbilityType.collection, service_id=self._client.service_id)
        query.add_term(
            field=AbilityType.id_field, value=self.data.ability_type_id)
        return InstanceProxy(AbilityType, query, client=self._client)
