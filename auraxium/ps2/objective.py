"""Objective class definitions."""

import dataclasses
from typing import List, Optional

from ..base import Cached, Ps2Data
from ..census import Query
from ..proxy import InstanceProxy
from ..types import CensusData
from ..utils import optional


@dataclasses.dataclass(frozen=True)
class ObjectiveTypeData(Ps2Data):
    """Data class for :class:`auraxium.ps2.ability.ObjectiveType`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    objective_type_id: int
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

    @classmethod
    def from_census(cls, data: CensusData) -> 'ObjectiveTypeData':
        params: List[Optional[str]] = [
            optional(data, f'param{i+1}', str) for i in range(9)]
        return cls(
            int(data['objective_type_id']),
            str(data['description']),
            *params)


class ObjectiveType(Cached, cache_size=10, cache_ttu=60.0):
    """A type of objective.

    This class mostly specifies the purpose of any generic parameters.
    """

    collection = 'objective_type'
    data: ObjectiveTypeData
    id_field = 'objective_type_id'

    def _build_dataclass(self, data: CensusData) -> ObjectiveTypeData:
        return ObjectiveTypeData.from_census(data)


@dataclasses.dataclass(frozen=True)
class ObjectiveData(Ps2Data):
    """Data class for :class:`auraxium.ps2.ability.Objective`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    objective_id: int
    objective_type_id: int
    objective_group_id: int
    param1: Optional[str]
    param2: Optional[str]
    param3: Optional[str]
    param4: Optional[str]
    param5: Optional[str]
    param6: Optional[str]
    param7: Optional[str]
    param8: Optional[str]
    param9: Optional[str]

    @classmethod
    def from_census(cls, data: CensusData) -> 'ObjectiveData':
        params: List[Optional[str]] = [
            optional(data, f'param{i+1}', str) for i in range(9)]
        return cls(
            int(data['objective_id']),
            int(data['objective_type_id']),
            int(data['objective_group_id']),
            *params)


class Objective(Cached, cache_size=10, cache_ttu=60.0):
    """A objective presented to a character."""

    collection = 'objective'
    data: ObjectiveData
    id_field = 'objective_id'

    def _build_dataclass(self, data: CensusData) -> ObjectiveData:
        return ObjectiveData.from_census(data)

    def type(self) -> InstanceProxy[ObjectiveType]:
        """Return the objective type of this objective."""
        query = Query(
            ObjectiveType.collection, service_id=self._client.service_id)
        query.add_term(
            field=ObjectiveType.id_field, value=self.data.objective_type_id)
        return InstanceProxy(ObjectiveType, query, client=self._client)
