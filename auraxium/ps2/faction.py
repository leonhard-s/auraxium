"""Object definition for the faction type."""

import dataclasses

from ..base import Named, Ps2Data
from ..types import CensusData


@dataclasses.dataclass(frozen=True)
class FactionData(Ps2Data):
    """Data container for Faction objects."""

    faction_id: int
    name: CensusData
    code_tag: str

    @classmethod
    def populate(cls, payload: CensusData) -> 'FactionData':
        return cls(
            # Required
            int(payload['faction_id']),
            payload['name'],
            payload['code_tag'])


class Faction(Named, cache_size=10):
    """A faction in PS2."""

    _collection = 'faction'
    data: FactionData
    _id_field = 'faction_id'

    # @property
    # def image(self) -> Awaitable[Image]:
    #     image_id = int(self.data['image_id'])
    #     return Image.get_by_id(image_id)

    # @property
    # def image_set(self) -> Awaitable[ImageSet]:
    #     image_id = int(self.data['image_set_id'])
    #     return ImageSet.get_by_id(image_id)

    @property
    def tag(self) -> str:
        """Return the tag of this faction (VS, TR, NC, and NSO)."""
        return str(self.data.code_tag)

    def _build_dataclass(self, payload: CensusData) -> FactionData:
        return FactionData.populate(payload)
