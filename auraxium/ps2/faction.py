from ..base import Named
from ..types import CensusData


class Faction(Named, cache_size=10):

    _collection = 'faction'
    _id_field = 'faction_id'

    # @property
    # def image(self) -> Awaitable[Image]:
    #     image_id = int(self._data['image_id'])
    #     return Image.get_by_id(image_id)

    # @property
    # def image_set(self) -> Awaitable[ImageSet]:
    #     image_id = int(self._data['image_set_id'])
    #     return ImageSet.get_by_id(image_id)

    @staticmethod
    def _check_payload(payload: CensusData) -> CensusData:
        return payload

    @property
    def tag(self) -> str:
        """Return the tag of this faction (VS, TR, NC, and NSO)."""
        return str(self._data['code_tag'])
