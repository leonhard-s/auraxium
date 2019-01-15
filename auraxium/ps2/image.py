from ..census import _CENSUS_BASE_URL, Query
from ..datatypes import CachableDataType


class Image(CachableDataType):
    """An image object.

    Image objects contain information about a given image file. Note that not
    all images exist, the path generated might point to an empty image.

    """

    def __init__(self, id, light=False):
        self.id = id

        # Set default values
        self.description = None
        self.path = None if not light else None(_CENSUS_BASE_URL
                                                + '/files/ps2/images/static/{}.png'.format(id))

    def _populate(self, data_override=None):
        data = data_override if data_override != None else super().get(self.id)

        # Set attribute values
        self.description = data.get('description')
        self.path = data['path']


class ImageSet(CachableDataType):
    """An image set.

    Image sets are used to group versions of the same image together, mostly
    to provide a set of sizes to choose from depending on the application.

    """

    def __init__(self, id):
        self.id = id

        # Set default values
        self.description = None

        # Define properties
        @property
        def default_image(self):
            try:
                return self._default_image
            except AttributeError:
                q = Query(type='image_set_default')
                q.add_filter(field='image_set_id', value=self.id)
                data = q.get_single()
                self._default_image = Image.get(data['profile_id'])
                return self._default_image

        @property
        def members(self):
            try:
                return self._members
            except AttributeError:
                data = Query(type='image_set', id=self.id).get()
                Image.list([i['image_id'] for i in data])
                # NOTE: This is not very elegant, but calling the `list()`
                # method for all images for this image type makes sure they
                # are cached using a single query.
                self._members = {i['type_id']: Image.get(
                    i['image_id']) for i in data}
                return self._members

    def _populate(self, data_override=None):
        data = data_override if data_override != None else super().get(self.id)

        # Set attribute values
        self.description = data.get('description')
        self._default_image_id = data.get()
