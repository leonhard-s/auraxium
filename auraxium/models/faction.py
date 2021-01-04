"""Data classes for :mod:`auraxium.ps2.faction`."""

from ..base import ImageData, Ps2Data
from ..types import LocaleData

__all__ = [
    'FactionData'
]

# pylint: disable=too-few-public-methods


class FactionData(Ps2Data, ImageData):
    """Data class for :class:`auraxium.ps2.faction.Faction`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        faction_id: The unique ID of this faction.
        name: The localised name of the faction.
        code_tag: The canonical tag representation of the faction.
        user_selectable: Whether this faction is playable.

    """

    faction_id: int
    name: LocaleData
    code_tag: str
    user_selectable: bool
