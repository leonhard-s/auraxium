"""Object definition for the faction type."""

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

    .. attribute:: image_id
       :type: int | None

       The image ID of the default image.

    .. attribute:: image_set_id
       :type: int | None

       The corresponding image set.

    .. attribute:: image_path
       :type: str | None

       The base path to the image with the default :attr:`image_id`.
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
    image_id: int | None
    image_set_id: int | None
    image_path: str | None

    def __repr__(self) -> str:
        """Return the unique string representation of the faction.

        This will take the form of <class:id:tag>, e.g. <Faction:2:NC>.
        """
        return f'<{self.__class__.__name__}:{self.id}:{self.data.code_tag}>'

    @property
    def tag(self) -> str:
        """Return the tag of this faction (VS, TR, NC, or NSO)."""
        return str(self.data.code_tag)
