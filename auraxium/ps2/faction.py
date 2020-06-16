"""Object definition for the faction type."""

import dataclasses

from ..base import Named, Ps2Data
from ..image import CensusImage
from ..types import CensusData
from ..utils import LocaleData


@dataclasses.dataclass(frozen=True)
class FactionData(Ps2Data):
    """Data container for the Faction class."""

    faction_id: int
    name: LocaleData
    code_tag: str
    user_selectable: bool
    image_set_id: int
    image_id: int

    @classmethod
    def populate(cls, payload: CensusData) -> 'FactionData':
        if (image_set_id := payload.get('image_set_id')) is not None:
            image_set_id = int(image_set_id)
        if (image_id := payload.get('image_id')) is not None:
            image_id = int(image_id)
        # image_path = payload.get('image_set_id')
        return cls(
            # Required
            int(payload['faction_id']),
            LocaleData.populate(payload['name']),
            payload['code_tag'],
            bool(payload['user_selectable']),
            # Optional
            image_set_id,
            image_id,
            # image_path,
        )


class Faction(Named, cache_size=10):
    """A faction in PS2."""

    _collection = 'faction'
    data: FactionData
    _id_field = 'faction_id'

    def __repr__(self) -> str:
        """Return the unique string representation of the faction.

        This will take the form of <class:id:tag>, e.g. <Faction:2:NC>.

        Returns:
            A string representing the object.

        """
        return f'<{self.__class__.__name__}:{self.id}:{self.data.code_tag}>'

    @property
    def image(self) -> CensusImage:
        return CensusImage(self.data.image_set_id, client=self._client)

    @property
    def tag(self) -> str:
        """Return the tag of this faction (VS, TR, NC, and NSO)."""
        return str(self.data.code_tag)

    def _build_dataclass(self, payload: CensusData) -> FactionData:
        return FactionData.populate(payload)
