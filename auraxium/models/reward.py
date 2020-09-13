"""Data classes for :mod:`auraxium.ps2.reward`."""

import dataclasses
from typing import List, Optional

from ..base import Ps2Data
from ..types import CensusData
from ..utils import optional

__all__ = [
    'RewardData',
    'RewardTypeData'
]

@dataclasses.dataclass(frozen=True)
class RewardData(Ps2Data):
    """Data class for :class:`auraxium.ps2.ability.Reward`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        reward_id: The unique ID of this reward.
        reward_type_id: The :class:`RewardType` of this reward.
        count_min: The minimum number of rewarded items/currency.
        count_max: The maximum number of rewarded items/currency.
        param*: Type-specific parameters for this reward. Refer to the
            corresponding :class:`RewardType` for details.

    """

    reward_id: int
    reward_type_id: int
    count_min: int
    count_max: int
    param1: str
    param2: Optional[str]
    param3: Optional[str]
    param4: Optional[str]
    param5: Optional[str]

    @classmethod
    def from_census(cls, data: CensusData) -> 'RewardData':
        params: List[Optional[str]] = [
            optional(data, f'param{i+1}', str) for i in range(1, 5)]
        return cls(
            int(data['reward_id']),
            int(data['reward_type_id']),
            int(data['count_min']),
            int(data['count_max']),
            str(data['param1']),
            *params)


@dataclasses.dataclass(frozen=True)
class RewardTypeData(Ps2Data):
    """Data class for :class:`auraxium.ps2.ability.ResourceType`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        reward_type_id: The unique ID of this reward type.
        description: A description of what this reward type is used
            for.
        count_min: The minimum number of rewarded items/currency.
        count_max: The maximum number of rewarded items/currency.
        param*: Descriptions of what the corresponding parameter is
            used for in rewards of this type.

    """

    reward_type_id: int
    description: str
    count_min: Optional[str]
    count_max: Optional[str]
    param1: str
    param2: Optional[str]
    param3: Optional[str]
    param4: Optional[str]
    param5: Optional[str]

    @classmethod
    def from_census(cls, data: CensusData) -> 'RewardTypeData':
        params: List[Optional[str]] = [
            optional(data, f'param{i+1}', str) for i in range(1, 5)]
        return cls(
            int(data['reward_type_id']),
            str(data['description']),
            optional(data, 'count_min', str),
            optional(data, 'count_max', str),
            str(data['param1']),
            *params)
