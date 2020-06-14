"""Object definition for the faction type."""

from ..base import Named
from ..types import CensusInfo


class Faction(Named, cache_size=10):
    """A faction in PS2."""

    _collection = 'faction'
    _id_field = 'faction_id'

    _census_info = CensusInfo(
        # Census name to ARX name
        {'name': 'name',
         'image_set_id': 'image_set_id',
         'code_tag': 'tag'})

    # @property
    # def image(self) -> Awaitable[Image]:
    #     image_id = int(self._data['image_id'])
    #     return Image.get_by_id(image_id)

    # @property
    # def image_set(self) -> Awaitable[ImageSet]:
    #     image_id = int(self._data['image_set_id'])
    #     return ImageSet.get_by_id(image_id)

    @property
    def tag(self) -> str:
        """Return the tag of this faction (VS, TR, NC, and NSO)."""
        return str(self._data['tag'])
