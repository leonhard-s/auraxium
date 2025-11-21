"""Data classes for :mod:`auraxium.ps2._reward`."""

from .base import RESTPayload

__all__ = [
    'RewardData',
    'RewardTypeData'
]


class RewardData(RESTPayload):
    """Data class for :class:`auraxium.ps2.Reward`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    reward_id: int
    reward_type_id: int
    count_min: int
    count_max: int
    param1: str
    param2: str | None = None
    param3: str | None = None
    param4: str | None = None
    param5: str | None = None


class RewardTypeData(RESTPayload):
    """Data class for :class:`auraxium.ps2.RewardType`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    reward_type_id: int
    description: str
    count_min: str | None
    count_max: str | None
    param1: str
    param2: str | None = None
    param3: str | None = None
    param4: str | None = None
    param5: str | None = None
