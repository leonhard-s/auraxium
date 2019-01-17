from ..census import _CENSUS_BASE_URL, Query
from ..datatypes import CachableDataType


class Image(CachableDataType):
    """An image object.

    Image objects contain information about a given image file. Note that not
    all images exist, the path generated might point to an empty image.

    """

    _collection = 'image'

    def __init__(self, id):
        self.id = id

        # Set default values
        self.description = None
        self.path = _CENSUS_BASE_URL + \
            '/files/ps2/images/static/{}.png'.format(id)

    def _populate(self, data=None):
        d = data if data != None else super()._get_data(self.id)

        # Set attribute values
        self.description = d.get('description')
        self.path = d['path']


class ImageSet(CachableDataType):
    """An image set.

    Image sets are used to group versions of the same image together, mostly
    to provide a set of sizes to choose from depending on the application.

    """

    _collection = 'image_set'

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
            d = q.get_single()
            self._default_image = Image.get(id=d['profile_id'])
            return self._default_image

    @property
    def members(self):
        try:
            return self._members
        except AttributeError:
            d = Query(type='image_set', id=self.id).get()
            Image.list(ids=[i['image_id'] for i in d])
            # NOTE: This is not very elegant, but calling the `list()`
            # method for all images for this image type makes sure they
            # are cached using a single query.
            self._members = {i['type_id']: Image.get(
                id=i['image_id']) for i in d}
            return self._members

    def _populate(self, data=None):
        d = data if data != None else super()._get_data(self.id)

        # Set attribute values
        self.description = d.get('description')
        self._default_image_id = d.get()
