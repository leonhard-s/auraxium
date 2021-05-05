"""Data classes for :mod:`auraxium.ps2._faction`."""

from .base import ImageData, RESTPayload
from ..types import LocaleData

__all__ = [
    'FactionData'
]

# pylint: disable=too-few-public-methods


class FactionData(RESTPayload, ImageData):
    """Data class for :class:`auraxium.ps2.Faction`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    faction_id: int
    name: LocaleData
    code_tag: str
    user_selectable: bool
