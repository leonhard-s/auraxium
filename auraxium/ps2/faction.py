from ..census import Query
from ..datatypes import EnumeratedDataType
from ..misc import LocalizedString
from .image import Image, ImageSet


class Faction(EnumeratedDataType):
    """Represents a faction in PlanetSide 2.

    Factions are static datatypes. Each one should only need to be
    initialized once.

    """

    def __init__(self, id):
        self.id = id

        # Set default values
        self.name = None
        self._image_id = None
        self._image_set_id = None
        self.is_playable = None
        self.tag = None

        # Define properties
        @property
        def image(self):
            try:
                return self._image
            except AttributeError:
                self._image = Image.get(id=self._image_id)
                return self._image

        @property
        def image_set(self):
            try:
                return self._image_set
            except AttributeError:
                self._image_set = ImageSet.get(id=self._image_set_id)
                return self._image_set

    def _populate(self, data_override=None):
        data = data_override if data_override != None else super().get(self.id)

        # Set attribute values
        self.name = LocalizedString(data['name'])
        self._image_id = data['image_id']
        self._image_set_id = data['image_set_id']
        self.is_playable = True if data['user_selectable'] == '1' else False
        # NOTE: As of the writing of this module, Nanite Systems does not have
        # a tag. As this might change with the introduction of combat robots, I
        # wrote this section in a way that should be able to handle that.
        self.tag = 'NS' if data['code_tag'] == 'None' else data['code_tag']
