"""Provides the classes and methods used for the object model."""

from ..base_api import Query
from .caching import Cache
from .misc import LocalizedString
from .exceptions import NoMatchesFoundError


class DataType():
    """The base datatype object.

    All PS2 data types are subclasses to this class. It also provides the base
    methods required for retrieving and caching instances.

    """

    _collection = '<no_collection>'
    id_ = -1

    def __str__(self):
        string = 'PS2 {} ('.format(self.__class__.__name__)

        try:
            if isinstance(self.name, LocalizedString):
                string += 'Name[en]: "{}", '.format(self.name.en)
            else:
                string += 'Name: "{}", '.format(self.name)
        except AttributeError:
            pass

        string += 'ID: {}'.format(self.id_)

        return string + ') at 0x{0:0{1}X}'.format(id(self), 16)

    def __eq__(self, other):
        """Provides support for "is equal" comparisons between Datatypes."""
        if self.__class__ == other.__class__ and self.id_ == other.id_:
            return True
        return False

    def __ne__(self, other):
        """Provides support for "is not equal" comparisons."""
        if self.__class__ != other.__class__ and self.id_ != other.id_:
            return True
        return False

    @classmethod
    def get(cls, id_, data=None):
        """Retrieves a single entry of the given datatype."""
        # Retrieve or create the instance
        try:
            if id_ in cls._cache:
                instance = cls._cache.load(id_)
            else:
                instance = cls(id_=id_)
                instance.populate(data=data)
                cls._cache.add(instance)
        except AttributeError:
            cls._cache = Cache()
            instance = cls(id_=id_)
            instance.populate(data=data)
            cls._cache.add(instance)

        return instance

    @classmethod
    def _get_data(cls, id_):
        """Retrieves a single object used to populate the data type."""
        try:
            id_field = cls._id_field
        except AttributeError:
            id_field = cls._collection + '_id'

        return Query(cls._collection).add_term(field=id_field, value=id_).get(single=True)

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
        query = Query(cls._collection).limit(len(ids_to_download))
        query.add_term(field=id_field, value=','.join([str(i) for i in ids_to_download]))
        data = query.get()

        # Create an instance for all of the downloaded objects
        instances = [cls.get(id_=d[id_field], data=d) for d in data]

        # Cache all the newly added instances
        _ = [cls._cache.add(i) for i in instances]

        # Join the two lists and sort the list by id
        instances.extend(cached_items)
        instances.sort(key=lambda i: i.id_)
        return instances

    def populate(self, data=None) -> None:
        """Populates the data type with the data given."""
        raise NotImplementedError('This method can only be used with subclasses.')


class NamedDataType():  # pylint: disable=too-few-public-methods
    """Auxilary parent class for localized named data types.

    Adds functinoality relevant to data types with a localized "name" field.
    Note that data types with non-localized names likes outfit or character
    will not be compatible.

    """

    _collection = '<no_collection>'

    @classmethod
    def get_by_name(cls, name, locale, ignore_case=True):
        """Returns the object matching the name given.

        This will only work on exact matches, use the `Query` object
        for fuzzy searches.

        Parameters
        ----------
        `name`: The name to search for

        `locale`: The locale the name given is using

        `ignore_case` (Optional): Whether to ignore case when looking
        up the object. Defaults to True.
        """

        # Generate request
        if ignore_case:
            query = Query(collection=cls._collection).case(False)
        else:
            query = Query(collection=cls._collection)
        query.add_term(field='name.' + locale, value=name)

        data = query.get(single=True)
        if not data:
            raise NoMatchesFoundError

        # Retrieve and return the object
        instance = cls.get(id_=data[cls._collection + '_id'],  # pylint: disable=no-member
                           data=data)
        return instance
