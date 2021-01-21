"""Data classes for :mod:`auraxium.ps2.reward`."""

from typing import Optional

from .._base import Ps2Data

__all__ = [
    'RewardData',
    'RewardTypeData'
]

# pylint: disable=too-few-public-methods


class RewardData(Ps2Data):
    """Data class for :class:`auraxium.ps2.Reward`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
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
    """Data class for :class:`auraxium.ps2.RewardType`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
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
