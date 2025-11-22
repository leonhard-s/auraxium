"""Data classes for :mod:`auraxium.ps2._resist`."""

from .base import RESTPayload

__all__ = [
    'ResistInfoData',
    'ResistTypeData'
]


class ResistInfoData(RESTPayload):
    """Data class for :class:`auraxium.ps2.ResistInfo`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    resist_info_id: int
    resist_type_id: int
    resist_percent: int | None = None
    resist_amount: int | None = None
    multiplier_when_headshot: float | None = None
    description: str


class ResistTypeData(RESTPayload):
    """Data class for :class:`auraxium.ps2.ResistType`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    resist_type_id: int
    description: str
