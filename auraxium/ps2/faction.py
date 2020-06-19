"""Object definition for the faction type."""

import dataclasses
from typing import Optional

from ..base import Named, Ps2Data
from ..types import CensusData
from ..utils import LocaleData, optional


@dataclasses.dataclass(frozen=True)
class FactionData(Ps2Data):
    """Data class for :class:`auraxium.ps2.faction.Faction`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
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
            bool(data['user_selectable']),
            optional(data, 'image_set_id', int),
            optional(data, 'image_id', int),
            optional(data, 'image_path', str))


class Faction(Named, cache_size=10):
    """A faction in PS2."""

    collection = 'faction'
    data: FactionData
    id_field = 'faction_id'

    def __repr__(self) -> str:
        """Return the unique string representation of the faction.

        This will take the form of <class:id:tag>, e.g. <Faction:2:NC>.

        Returns:
            A string representing the object.

        """
        return f'<{self.__class__.__name__}:{self.id}:{self.data.code_tag}>'

    @property
    def tag(self) -> str:
        """Return the tag of this faction (VS, TR, NC, or NSO)."""
        return str(self.data.code_tag)

    def _build_dataclass(self, data: CensusData) -> FactionData:
        return FactionData.from_census(data)
