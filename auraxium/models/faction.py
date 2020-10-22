"""Data classes for :mod:`auraxium.ps2.faction`."""

import dataclasses

from ..base import ImageData, Ps2Data
from ..types import CensusData, LocaleData, optional

__all__ = [
    'FactionData'
]


@dataclasses.dataclass(frozen=True)
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

    @classmethod
    def from_census(cls, data: CensusData) -> 'FactionData':
        return cls(
            optional(data, 'image_id', int),
            optional(data, 'image_set_id', int),
            optional(data, 'image_path', str),
            int(data.pop('faction_id')),
            LocaleData.from_census(data.pop('name')),
            str(data.pop('code_tag')),
            bool(int(data.pop('user_selectable'))))
