"""Object definition for the faction type."""

from typing import Optional

from ..base import ImageMixin, Named
from ..models import FactionData
from ..types import LocaleData

__all__ = [
    'Faction'
]


class Faction(Named, ImageMixin, cache_size=10):
    """A faction in PS2.

    This includes both playable factions, as well as the default
    Nanite Systems faction used for uncapturable territories and
    cross-faction items.

    .. attribute:: id
       :type: int

       The unique ID of this faction. In the API payload, this
       field is called ``faction_id``.

    .. attribute:: code_tag
       :type: str

       The canonical tag representation of the faction (VS, TR, NC, or
       NSO).

    .. attribute:: name
       :type: auraxium.types.LocaleData

       The localised name of the faction.

    .. attribute:: user_selectable
       :type: bool

       Whether this faction is playable.
    """

    collection = 'faction'
    data: FactionData
    id_field = 'faction_id'
    _model = FactionData

    # Type hints for data class fallback attributes
    id: int
    code_tag: str
    name: LocaleData
    user_selectable: bool
    image_id: Optional[int]
    image_set_id: Optional[int]
    image_path: Optional[str]

    def __repr__(self) -> str:
        """Return the unique string representation of the faction.

        This will take the form of <class:id:tag>, e.g. <Faction:2:NC>.
        """
        return f'<{self.__class__.__name__}:{self.id}:{self.data.code_tag}>'

    @property
    def tag(self) -> str:
        """Return the tag of this faction (VS, TR, NC, or NSO)."""
        return str(self.data.code_tag)
