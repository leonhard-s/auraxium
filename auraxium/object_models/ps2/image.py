from ...base_api import Query
from ...constants import CENSUS_ENDPOINT
from ..datatypes import DataType


class Image(DataType):
    """An image object.

    Image objects contain information about a given image file. Note that not
    all images exist, the path generated might point to an empty image.

    """

    _collection = 'image'

    def __init__(self, id_):
        self.id_ = id_

        # Set default values
        self.description = None
        self.path = CENSUS_ENDPOINT + \
            '/files/ps2/images/static/{}.png'.format(id_)

    def populate(self, data=None):
        d = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self.description = d.get('description')
        self.path = d['path']


class ImageSet(DataType):
    """An image set.

    Image sets are used to group versions of the same image together, mostly
    to provide a set of sizes to choose from depending on the application.

    """

    _collection = 'image_set'

    def __init__(self, id_):
        self.id_ = id_

        # Set default values
        self._default_image = None  # Internal (See properties)
        self.description = None
        self._members = None  # Internal (See properties)

    # Define properties
    @property
    def default_image(self):
        try:
            return self._default_image
        except AttributeError:
            data = Query(collection='image_set_default', image_set_id=self.id_).get(single=True)
            self._default_image = Image.get(id_=data['default_image_id'])
            return self._default_image

    @property
    def members(self):
        try:
            return self._members
        except AttributeError:
            data = Query(collection='image_set', image_id=self.id_).get()
            # Bulk-load the images for caching to speed up the list comprehension below
            Image.list(ids=[i['image_id'] for i in data])
            # NOTE: This is not very elegant, but calling the `list()`
            # method for all images for this image type makes sure they
            # are cached using a single query.
            self._members = {i['type_id']: Image.get(id_=i['image_id']) for i in data}
            return self._members

    def populate(self, data=None):
        d = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self.description = d.get('description')
