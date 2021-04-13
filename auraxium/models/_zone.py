"""Data classes for :mod:`auraxium.ps2._zone`."""

from .base import RESTPayload
from ..types import LocaleData

__all__ = [
    'ZoneData'
]

# pylint: disable=too-few-public-methods


class ZoneData(RESTPayload):
    """Data class for :class:`auraxium.ps2.Zone`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    zone_id: int
    code: str
    hex_size: int
    name: LocaleData
    description: LocaleData
