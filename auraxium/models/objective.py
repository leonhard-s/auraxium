"""Data classes for :mod:`auraxium.ps2.objective`."""

import dataclasses
from typing import List, Optional

from ..base import Ps2Data
from ..types import CensusData
from ..utils import optional


__all__ = [
    'ObjectiveData',
    'ObjectiveTypeData'
]


@dataclasses.dataclass(frozen=True)
class ObjectiveData(Ps2Data):
    """Data class for :class:`auraxium.ps2.ability.Objective`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        objective_id: The unique ID of this objective.
        objective_type_id: The associated objective type for this
            objective.
        objective_group_id: The objective group this objective
            contributes to. Used to link objectives to directives.
        param*: Type-specific parameters for this objective. Refer to
            the corresponding :class:`ObjectiveType` for details.

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
            int(data.pop('objective_id')),
            int(data.pop('objective_type_id')),
            int(data.pop('objective_group_id')),
            *params)


@dataclasses.dataclass(frozen=True)
class ObjectiveTypeData(Ps2Data):
    """Data class for :class:`auraxium.ps2.ability.ObjectiveType`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        objective_type_id: The unique ID of the objective type.
        description: A description of what the objective type is used
            for.
        param*: Descriptions of what the corresponding parameter is
            used for in objectives of this type.

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
            int(data.pop('objective_type_id')),
            str(data.pop('description')),
            *params)
