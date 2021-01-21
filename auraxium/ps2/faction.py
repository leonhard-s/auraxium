"""Object definition for the faction type."""

from .._base import ImageMixin, Named
from ..models import FactionData
from ..types import LocaleData

__all__ = [
    'Faction'
]


class Faction(Named, ImageMixin, cache_size=10):
    """A faction in PS2.

    Attributes:
        faction_id: The unique ID of this faction.
        code_tag: The canonical tag representation of the faction.
        user_selectable: Whether this faction is playable.

    """

    collection = 'faction'
    data: FactionData
    _dataclass = FactionData
    id_field = 'faction_id'

    # Type hints for data class fallback attributes
    faction_id: int
    code_tag: str
    user_selectable: bool

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
