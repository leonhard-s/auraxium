from .census import Query


class DatatypeBase(object):
    """The base class for datatypes used by the Census APi wrapper.

    All other datatype objects are subclassed to this class. It currently does
    not have any active components. If needed, it's there.

    """

    def __new__(cls, id, *args, **kwargs):
        # If the id of a datatype is None, return none instead of an object.
        # This is done to allow the `<datatype>(data.get('id'))` syntax
        if id == None:
            return None
        else:
            return super(DatatypeBase, cls).__new__(cls)

    def get_data(cls, instance, data_override=None):
        # If data_override hasn't been specified, retrieve the data yourself
        if data_override == None:
            data = Query(instance.__class__, id=instance.id).get_single()
        else:
            data = data_override
        return data


class StaticDatatype(DatatypeBase):
    """The base class for all static datatypes used by the Census API wrapper.

    Static datatypes are only retrieved once, after which they will be cached
    in a class attribute. Be mindful of which collections you make into a
    static datatype, as the cache is never emptied.

    """

    _cache = {}  # Downloaded items will be kept in this dictionary forever

    def __new__(cls, id, *args, **kwargs):
        # If the ID already exists
        if id in cls._cache.keys():
            return cls._cache[id]  # Return the cached object
        else:
            instance = super(StaticDatatype, cls).__new__(cls, id)
            cls._cache[id] = instance  # Store the new object
            return instance


class InterimDatatype(DatatypeBase):
    """The base class for datatypes that are neither static nor dynamic.

    An interim datatype will be retrieved and kept in storage until it is
    overridden by a newer entry.

    """

    _cache = {}  # Cached items are kept in this dictionary
    # This list keeps track of the order the items were added to the dictionary
    _cache_order = []
    _cache_size = 10  # The size of the cache (i.e. maximum number of items)

    def __new__(cls, id, *args, **kwargs):
        # If the ID already exists
        if id in cls._cache.keys():
            return cls._cache[id]  # Returned the cached object
        else:
            instance = super(InterimDatatype, cls).__new__(cls, id)
            # If the cache is full
            if len(cls._cache) >= cls._cache_size:
                cls._cache_order.append(id)  # Append the new id to the list
                del_id = cls._cache_order.pop(0)  # Remove the oldest entry
                del cls._cache[del_id]  # Delete the oldest cached object
            cls._cache[id] = instance  # Store the new object
            return instance


class DynamicDatatype(DatatypeBase):
    """The base class for datatypes that are always retrieved without caching.

    Use this base class for datatypes that are either too unique to bother
    keeping (such as leaderboard information), or that are expected to change
    too regularly (such as player or weapon statistics).

    """

    pass
