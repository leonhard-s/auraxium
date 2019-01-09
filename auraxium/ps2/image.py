from ..census import _CENSUS_BASE_URL, Query
from ..datatypes import InterimDatatype, StaticDatatype


class Image(InterimDatatype):
    _cache_size = 500
    _collection = 'image'

    def __init__(self, id, description=None, path=None):
        self.id = id

        # If path is already set, there is no more information to query. The
        # creation of the image object is only there to allow for caching

        if path != None:
            self.path = _CENSUS_BASE_URL + str(path)
            self.description = '(Skipped query)' if description == None else description
        else:
            data = super(Image, self).get_data(self)
            try:
                self.description = data['description']
            except KeyError:
                self.description = 'None'
            self.path = _CENSUS_BASE_URL + data['path']


class ImageSet(InterimDatatype):
    _cache_size = 100
    _collection = 'image_set'

    def __init__(self, id):
        self.id = id
        self.images = {}

        # Get a list of all images of this set, and join the default image
        q = Query(self.__class__, limit=10, id=id)
        q.join(ImageSetDefault, match='image_set_id').show('type_id')
        data = q.get()

        self.description = data[0]['description']

        for image_set in data:
            desc = '{} - {}'.format(image_set['description'],
                                    image_set['type_description'])
            self.images[image_set['type_id']] = Image(
                image_set['image_id'], description=desc, path=image_set['image_path'])

        self.default_image = self.images[data[0]
                                         ['image_set_default']['type_id']]


class ImageSetDefault(object):
    # Dummy object to get the _collection attribute from
    _collection = 'image_set_default'
