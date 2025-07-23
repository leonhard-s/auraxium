"""Data classes for :mod:`auraxium.ps2._metagame`."""

from typing import Optional

from .base import RESTPayload
from ..types import LocaleData

__all__ = [
    'MetagameEventData'
]


class MetagameEventData(RESTPayload):
    """Data class for :class:`auraxium.ps2.MetagameEvent`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    metagame_event_id: int
    name: LocaleData
    description: LocaleData
    type: int
    duration_minutes: float
    experience_bonus: Optional[float] = None
