"""Data classes for :mod:`auraxium.ps2._armour`."""

from typing import Optional

from .base import RESTPayload

__all__ = [
    'ArmourInfoData'
]

# pylint: disable=too-few-public-methods


class ArmourInfoData(RESTPayload):
    """Data class for :class:`auraxium.ps2.ArmourInfo`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    armor_info_id: int
    armor_facing_id: int
    armor_percent: int
    armor_amount: Optional[int] = None
    description: str
