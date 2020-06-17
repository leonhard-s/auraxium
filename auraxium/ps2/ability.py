"""Ability and ability type class definitions."""

import dataclasses
from typing import Awaitable, List, Optional

from ..base import Cached, Ps2Data
from ..utils import optional
from ..types import CensusData


@dataclasses.dataclass(frozen=True)
class AbilityTypeData(Ps2Data):
    """Data class for :class:`auraxium.ps2.ability.AbilityType`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
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

    _collection = 'ability_type'
    data: AbilityTypeData
    _id_field = 'ability_type_id'

    def _build_dataclass(self, data: CensusData) -> AbilityTypeData:
        return AbilityTypeData.from_census(data)


@dataclasses.dataclass(frozen=True)
class AbilityData(Ps2Data):
    """Data class for :class:`auraxium.ps2.ability.Ability`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
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
    """An ability cast by a player.

    Access the corresponding :class:`auraxium.ps2.ability.AbilityType`
    instance via the :meth:`type` property for information on generic
    parameters.
    """

    _collection = 'ability'
    data: AbilityData
    _id_field = 'ability_id'

    @property
    def type(self) -> Awaitable[AbilityType]:
        """Return the ability type of this ability."""

        async def get_type() -> AbilityType:
            id_ = int(self.data.ability_type_id)
            ability = await AbilityType.get_by_id(id_, client=self._client)
            assert ability is not None
            return ability

        return get_type()

    def _build_dataclass(self, data: CensusData) -> AbilityData:
        return AbilityData.from_census(data)
