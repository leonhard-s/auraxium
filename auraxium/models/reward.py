"""Data classes for :mod:`auraxium.ps2.reward`."""

from typing import Optional

from ..base import Ps2Data

__all__ = [
    'RewardData',
    'RewardTypeData'
]


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
    param2: Optional[str] = None
    param3: Optional[str] = None
    param4: Optional[str] = None
    param5: Optional[str] = None


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
    param2: Optional[str] = None
    param3: Optional[str] = None
    param4: Optional[str] = None
    param5: Optional[str] = None
