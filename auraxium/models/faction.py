"""Data classes for :mod:`auraxium.ps2.faction`."""

from .._base import ImageData, Ps2Data
from ..types import LocaleData

__all__ = [
    'FactionData'
]

# pylint: disable=too-few-public-methods


class FactionData(Ps2Data, ImageData):
    """Data class for :class:`auraxium.ps2.faction.Faction`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    faction_id: int
    name: LocaleData
    code_tag: str
    user_selectable: bool
