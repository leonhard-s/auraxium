"""Data classes for :mod:`auraxium.ps2.resist`."""

from typing import Optional

from .._base import Ps2Data

__all__ = [
    'ResistInfoData',
    'ResistTypeData'
]

# pylint: disable=too-few-public-methods


class ResistInfoData(Ps2Data):
    """Data class for :class:`auraxium.ps2.armour.ResistInfo`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    resist_info_id: int
    resist_type_id: int
    resist_percent: Optional[int] = None
    resist_amount: Optional[int] = None
    multiplier_when_headshot: Optional[float] = None
    description: str


class ResistTypeData(Ps2Data):
    """Data class for :class:`auraxium.ps2.armour.ResistType`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    resist_type_id: int
    description: str
