from .census import Query
from .caching import Cache
from .misc import LocalizedString


class DataType(object):
    """The base datatype object.

    All PS2 data types are subclasses to this class. It also provides the base
    methods required for retrieving and caching instances.

    """

    _collection = '<no_collection>'

    def __str__(self):
        s = 'PS2 {} ('.format(self.__class__.__name__)

        try:
            if isinstance(self.name, LocalizedString):
                s += 'Name[en]: "{}", '.format(self.name.en)
            else:
                s += 'Name: "{}", '.format(self.name)
        except AttributeError:
            pass

        s += 'ID: {}'.format(self.id)

        return s + ') at 0x{0:0{1}X}'.format(id(self), 16)

    @classmethod
    def get(cls, id, field=None):
        """Retrieves a single entry of the given datatype."""
        # id_field = field if field != None else cls._collection + '_id'

        # Retrieve or create the instance
        try:
            if id in cls._cache:
                instance = cls._cache.load(id)
            else:
                instance = cls(id=id)
                instance._populate()
                cls._cache.add(instance)
        except AttributeError:
            cls._cache = Cache()
            instance = cls(id=id)
            instance._populate()
            cls._cache.add(instance)

        return instance

    @classmethod
    def _get_data(cls, id, field=None):
        """Retrieves a single object used to populate the data type."""
        id_field = field if field != None else cls._collection + '_id'

        if field == None:
            q = Query(cls._collection, id=id)
        else:
            q = Query(cls._collection).add_filter(field=id_field, value=id)

        return q.get_single()

    @classmethod
    def list(cls, ids, field=None):
        """Retrieves a list of entries of a given datatype."""
        id_field = field if field != None else cls._collection + '_id'

        # Create a list of all object instances that are not cached
        try:
            ids_to_download = [i for i in ids if not i in cls._cache]
        except AttributeError:
            cls._cache = Cache()
            ids_to_download = ids

        # Download the missing entries
        q = Query(cls._collection, limit=len(ids_to_download))
        q.add_filter(field=id_field, value=','.join(ids_to_download))
        data = q.get()

        # Create an instance for all of the downloaded objects
        instances = [cls(id=d[id_field])._populate(data_override=d)
                     for d in data]

        # Cache all the newly added instances
        [cls._cache.add(i) for i in instances]

        # Create a list of all cached items
        cached_items = [cls._cache.load(i) for i in ids if i in cls._cache]

        # Join the two lists and sort the list by id
        instances.extend(cached_items).sort(key=lambda i: i.id)
        return instances


class CachableDataType(DataType):
    pass


class EnumeratedDataType(DataType):
    pass


class NamedDataType(object):
    """Auxilary parent class for localized named data types.

    Adds functinoality relevant to data types with a localized "name" field.
    Note that data types with non-localized names likes outfit or character
    will not be compatible.

    """

    @classmethod
    def get_by_name(cls, name, locale, ignore_case=True):
        # Generate request
        if ignore_case:
            q = Query(type=cls._collection, check_case=False)
        else:
            q = Query(type=cls._collection)
        q.add_filter(field='name.' + locale, value=name)

        d = q.get_single()
        if len(d) == 0:
            return  # TODO: Replace with exception

        # Create and return a weapon object
        instance = cls(id=d[cls._collection + '_id'])
        instance._populate(data=d)
        return instance
