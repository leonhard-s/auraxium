import logging
from datetime import datetime

from .census import Query

# Create a logger
logger = logging.getLogger('auraxium.census')


class Cache(object):
    """A cache stores instances of other objects.

    Caches are used to reduce the number of times an object needs to be
    re-created to reduce network traffic. They can be size-limited (only keep
    x items and discard the oldest ones), age-limited (keep items for y seconds
    before discarding them) or both.

    """

    def __init__(self, max_size=None, max_age=None):
        self._contents = {}
        self.max_age = max_age
        self.max_size = max_size
        self._meta_list = []  # Contains tuples like (<id>, <time_added>)

    def __contains__(self, item):
        return True if item in self._contents.keys() else False

    def __getitem__(self, key):
        return self._contents[key]

    def __len__(self):
        return len(self._meta_list)

    def add(self, item):
        """Adds a new item to the cache."""
        # No caching of non-existing objects
        if item == None:
            return

        # Only proceed if the item has not already been cached
        if item in self._contents:
            return

        try:
            # If the cache is full, delete the oldest item
            if len(self._meta_list) >= self.max_size:
                del self.contents[self._meta_list.pop(0)[0]]
        except TypeError:
            # The TypeError is raised in case max_size has not been set
            pass

        self._contents[str(item.id)] = item
        self._meta_list.append((str(item.id), datetime.utcnow()))

    def clear(self):
        """Removes all stored items from the cache."""
        self._contents = {}
        self._order = []

    def trim(self):
        """Checks if any items are scheduled for deletion."""
        now = datetime.utcnow()
        trim_list = [t for t in self._meta_list if now > t[1] + self.max_age]
        for t in trim_list:
            del self._contents[t[0]]
            self._meta_list.remove(t)


class DatatypeBase(object):
    """The base class for datatypes used by the Census APi wrapper.

    All other datatype objects are subclassed to this class.

    """

    def get_data(cls, instance):
        try:
            joins = instance._join
            if not isinstance(joins, list):
                joins = [joins]
        except:
            joins = []
        # Some collections, such as `profile_2`, don't have id field names that
        # match their collection name. For these, the _id_field class attribute
        # is used instead.
        try:
            id_field = cls._id_field
        except AttributeError:
            id_field = cls._collection + '_id'

        # Create a new request
        q = Query(cls._collection).add_filter(
            field=id_field, value=instance.id)
        # Apply the default join for any collection listed in `join`
        for j in joins:
            q.join(j)
        return q.get_single()

    def is_cached(cls, instance):
        is_cached = True if instance.id in cls._cache else False
        s = 'Retrieving' if is_cached else 'Creating'
        logger.debug('{} {} (ID: {}).'.format(
            s, instance.__class__.__name__, instance.id))
        return is_cached


class StaticDatatype(DatatypeBase):
    """The base class for all static datatypes used by the Census API wrapper.

    Static datatypes are only retrieved once, after which they will be cached
    in a class attribute. Be mindful of which collections you make into a
    static datatype, as the cache is never emptied.

    """

    def __new__(cls, id=None, *args, **kwargs):
        # We don't cache nobody! But we will cache anybody...
        if id == None:
            return

        # If the id exists in the cache, return it. If the cache doesn't exist,
        # create it.
        try:
            len(cls._cache)
        except AttributeError:
            cls._cache = Cache()

        if id in cls._cache:
            return cls._cache[id]

        return super().__new__(cls)

    def _add_to_cache(cls, instance):
        cls._cache.add(instance)


class InterimDatatype(DatatypeBase):
    """The base class for datatypes that are neither static nor dynamic.

    An interim datatype will be retrieved and kept in storage until it is
    overridden by a newer entry.

    """

    _cache_lifespan = None
    _cache_size = None

    def __new__(cls, id=None, *args, **kwargs):
        # We don't cache nobody! But we will cache anybody...
        if id == None:
            return

        try:
            if id in cls._cache and id != None:
                return cls._cache[id]
        except AttributeError:
            cls._cache = Cache(cls._cache_size, cls._cache_lifespan)

        return super().__new__(cls)

    def _add_to_cache(cls, instance):
        cls._cache.add(instance)


class DynamicDatatype(DatatypeBase):
    """The base class for datatypes that are always retrieved without caching.

    Use this base class for datatypes that are either too unique to bother
    keeping (such as leaderboard information), or that are expected to change
    too regularly (such as player or weapon statistics).

    """

    pass
