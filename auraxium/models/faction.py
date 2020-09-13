"""Data classes for :mod:`auraxium.ps2.faction`."""

import dataclasses
from typing import Optional

from ..base import Ps2Data
from ..types import CensusData
from ..utils import LocaleData, optional

__all__ = [
    'FactionData'
]


@dataclasses.dataclass(frozen=True)
class FactionData(Ps2Data):
    """Data class for :class:`auraxium.ps2.faction.Faction`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        faction_id: The unique ID of this faction.
        name: The localised name of the faction.
        code_tag: The canonical tag representation of the faction.
        user_selectable: Whether this faction is playable.
        image_set_id: The image set associated with this faction.
        image_id: The default image asset for this faction.
        image_path: The string version of the faction's default image.

    """

    faction_id: int
    name: LocaleData
    code_tag: str
    user_selectable: bool
    image_set_id: Optional[int]
    image_id: Optional[int]
    image_path: Optional[str]

    @classmethod
    def from_census(cls, data: CensusData) -> 'FactionData':
        return cls(
            int(data['faction_id']),
            LocaleData.from_census(data['name']),
            str(data['code_tag']),
            bool(int(data['user_selectable'])),
            optional(data, 'image_set_id', int),
            optional(data, 'image_id', int),
            optional(data, 'image_path', str))
