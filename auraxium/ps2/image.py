from ..census import _CENSUS_BASE_URL, Query
from ..datatypes import InterimDatatype, StaticDatatype


class Image(InterimDatatype):
    _cache_size = 500
    _collection = 'image'

    def __init__(self, id, data_override=None):
        self.id = id

        if super().is_cached(self):  # If the object is cached, skip
            return

        self.path = _CENSUS_BASE_URL + \
            '/files/ps2/images/static/{}.png'.format(id)

        super()._add_to_cache(self)  # Cache this instance for future use

    def __str__(self):
        return 'Image (ID: {})'.format(self.id)


class ImageSet(InterimDatatype):
    _cache_size = 100
    _collection = 'image_set'

    def __init__(self, id, data_override=None):
        self.id = id

        if super().is_cached(self):  # If the object is cached, skip
            return

        self.images = {}

        # Get a list of all images of this set, and join the default image
        q = Query(self.__class__._collection, limit=10, id=id)
        q.join('image_set_default', match='image_set_id').show('type_id')
        data = q.get()

        self.description = data[0]['description']

        for image_set in data:
            desc = '{} - {}'.format(image_set['description'],
                                    image_set['type_description'])
            self.images[image_set['type_id']] = Image(image_set['image_id'])

        self.default_image = self.images[data[0]
                                         ['image_set_default']['type_id']]

        super()._add_to_cache(self)  # Cache this instance for future use

    def __str__(self):
        return 'ImageSet (ID: {}, Description: "{}")'.format(
            self.id, self.description)
