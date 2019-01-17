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
    def get(cls, id, data=None):
        """Retrieves a single entry of the given datatype."""
        # Retrieve or create the instance
        try:
            if id in cls._cache:
                instance = cls._cache.load(id)
            else:
                instance = cls(id=id)
                instance._populate(data=data)
                cls._cache.add(instance)
        except AttributeError:
            cls._cache = Cache()
            instance = cls(id=id)
            instance._populate(data=data)
            cls._cache.add(instance)

        return instance

    @classmethod
    def _get_data(cls, id):
        """Retrieves a single object used to populate the data type."""
        try:
            id_field = cls._id_field
        except AttributeError:
            id_field = cls._collection + '_id'

        q = Query(cls._collection).add_filter(field=id_field, value=id)

        return q.get_single()

    @classmethod
    def list(cls, ids):
        """Retrieves a list of entries of a given datatype."""
        try:
            id_field = cls._id_field
        except AttributeError:
            id_field = cls._collection + '_id'

        # Create a list of all object instances that are not cached
        cached_items = []
        ids_to_download = []
        try:
            for i in ids:
                if i in cls._cache:
                    cached_items.append(cls._cache.load(i))
                else:
                    ids_to_download.append(i)
        except AttributeError:
            cls._cache = Cache()
            ids_to_download = ids

        # Download the missing entries
        q = Query(cls._collection, limit=len(ids_to_download))
        q.add_filter(field=id_field, value=','.join(ids_to_download))
        data = q.get()

        # Create an instance for all of the downloaded objects
        instances = [cls.get(id=d[id_field], data=d) for d in data]

        # Cache all the newly added instances
        [cls._cache.add(i) for i in instances]

        # Join the two lists and sort the list by id
        instances.extend(cached_items)
        instances.sort(key=lambda i: i.id)
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

        # Retrieve and return the object
        instance = cls.get(id=d[cls._collection + '_id'], data=d)
        return instance
