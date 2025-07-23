"""Dataclasses for :mod:`auraxium.ps2._fish`."""

from .base import RESTPayload, ImageData
from ..types import LocaleData

__all__ = [
    'FishData',
]


class FishData(RESTPayload, ImageData):
    """Data class for :class:`auraxium.ps2.Fish`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    fish_id: int
    name: LocaleData
    rarity: int
    average_size: int
    size_deviation: int
    scan_point_amount: int
    cost: int
