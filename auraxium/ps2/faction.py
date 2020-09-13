"""Object definition for the faction type."""

from ..base import Named
from ..models import FactionData
from ..types import CensusData


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

    @staticmethod
    def _build_dataclass(data: CensusData) -> FactionData:
        return FactionData.from_census(data)
