import logging

# Create a logger
logger = logging.getLogger('auraxium.collections')

# A dictionary containing collections that have been previously downloaded and
# initialized, kept around for increased performance.
_cache = {}


class Collection(object):
    """Represents a PlanetSide 2 census collection."""

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


def get_collection(collection):
    """Returns the Collection object for a given string."""
    # If the collection has been previously used, use the cached data
    if collection in _cache.keys():
        logger.debug('Reusing cached collection "{}".'.format(collection))
    # If it hasn't, contact the server for information about it
    else:
        logger.debug('Retrieving collection "{}"...'.format(collection))
        try:
            _cache[collection] = Collection(collection)
        except UnknownCollectionError:
            raise

    return _cache[collection]
