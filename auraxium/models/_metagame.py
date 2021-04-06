"""Data classes for :mod:`auraxium.ps2.metagame`."""

from typing import Optional

from ._base import RESTPayload
from ..types import LocaleData

__all__ = [
    'MetagameEventData'
]

# pylint: disable=too-few-public-methods


class MetagameEventData(RESTPayload):
    """Data class for :class:`auraxium.ps2.metagame.MetagameEvent`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    metagame_event_id: int
    name: LocaleData
    description: LocaleData
    type: int
    experience_bonus: Optional[int] = None
