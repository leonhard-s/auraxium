"""Data classes for :mod:`auraxium.ps2._achievement`."""

from .base import ImageData, RESTPayload
from ..types import LocaleData

__all__ = [
    'AchievementData'
]


class AchievementData(RESTPayload, ImageData):
    """Data class for :class:`auraxium.ps2.Achievement`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    achievement_id: int
    item_id: int
    objective_group_id: int
    reward_id: int
    repeatable: bool
    name: LocaleData
    description: LocaleData
