"""Base classes for the Auraxium object model.

These classes define shared functionality required by all object
representations of API data, and defines the basic class hierarchy used
throughout the PlanetSide 2 object model.
"""

import abc
import logging
from typing import Any, ClassVar, List, Optional, Type, TypeVar, Union

import pydantic

from .models.base import RESTPayload
from ._cache import TLRUCache
from .census import Query
from .errors import PayloadError
from ._rest import RequestClient
from .types import CensusData
from ._support import deprecated

__all__ = [
    'Ps2Object',
    'Cached',
    'Named'
]

CachedT = TypeVar('CachedT', bound='Cached')
NamedT = TypeVar('NamedT', bound='Named')
Ps2ObjectT = TypeVar('Ps2ObjectT', bound='Ps2Object')

_log = logging.getLogger('auraxium.ps2')


class Ps2Object(metaclass=abc.ABCMeta):
    """Common base class for all PS2 object representations.

    This requires that subclasses overwrite the
    :attr:`Ps2Object.collection` and :attr:`Ps2Object.id_field` names,
    which are used to tie the class to its corresponding API
    counterpart.

    """

    collection: ClassVar[str] = 'bogus'
    _model: ClassVar[Type[RESTPayload]]
    id_field: ClassVar[str] = 'bogus_id'

    def __init__(self, data: CensusData, client: RequestClient) -> None:
        """Initialise the object.

        This sets the object's :attr:`~Ps2Object.id` attribute and
        populates the instance using the provided payload.

        Arguments:
            data: The census response dictionary to populate the
                object with.
            client (optional): The client object to use for requests
                performed via this object. Defaults to ``None``.

        """
        id_ = int(str(data[self.id_field]))
        _log.debug('Instantiating <%s:%d> using payload: %s',
                   self.__class__.__name__, id_, data)
        self.id = id_
        self._client = client
        try:
            self.data = self._model(**data)
        except pydantic.ValidationError as err:
            raise PayloadError(
                f'Unable to instantiate {self.__class__.__name__} instance '
                f'from given payload: {err}', data) from err

    def __eq__(self, value: Any) -> bool:
        if not isinstance(value, self.__class__):
            return False
        return self.id == value.id

    def __getattr__(self, name: str) -> Any:
        """Fallback for missing attributes.

        This allows missing attribute in the :class:`Ps2Object`
        instance to fall back to its corresponding data class.

        If the attribute cannot be found there either, an
        :class:`AttributeError` is raised as normal.

        """
        # Re-raising or propagating the inner exception would only clutter up
        # the exception traceback, so we raise one "from scratch" instead.
        if hasattr(self.data, name):
            return getattr(self.data, name)
        raise AttributeError(name)

    def __hash__(self) -> int:
        return hash((self.__class__, self.id))

    def __repr__(self) -> str:
        """Return the unique string representation of this object.

        This will take the form of ``<Class:id>``, e.g.
        ``<Weapon:108>``.

        Returns:
            A string representing the object.

        """
        return f'<{self.__class__.__name__}:{self.id}>'

    @classmethod
    @deprecated('0.3', replacement='Client.count()')
    async def count(cls, client: RequestClient, **kwargs: Any) -> int:
        """Return the number of items matching the given terms.

        Arguments:
            client: The client through which to perform the request.
            **kwargs: Any number of query filters to apply.

        Returns:
            The number of entries entries.

        """
        # NOTE: The following is a runtime-only compatibility hack and violates
        # type hinting. This is scheduled for removal as per the decorator.
        return await client.count(cls, **kwargs)  # type: ignore

    @classmethod
    @deprecated('0.3', replacement='Client.find()')
    async def find(cls: Type[Ps2ObjectT], results: int = 10, *,
                   offset: int = 0, promote_exact: bool = False,
                   check_case: bool = True, client: RequestClient,
                   **kwargs: Any) -> List[Ps2ObjectT]:
        """Return a list of entries matching the given terms.

        This returns up to as many entries as indicated by the results
        argument. Note that it may be fewer if not enough matches are
        found.

        Arguments:
            results (optional): The maximum number of results. Defaults
                to ``10``.
            offset (optional): The number of entries to skip. Useful
                for paginated views. Defaults to ``0``.
            promote_exact (optional): If enabled, exact matches to
                non-exact searches will always come first in the return
                list. Defaults to ``False``.
            check_case (optional): Whether to check case when comparing
                strings. Note that case-insensitive searches are much
                more expensive. Defaults to ``True``.
            client: The client through which to perform the request.
            **kwargs: Any number of filters to apply.

        Returns:
            A list of matching entries.

        """
        # NOTE: The following is a runtime-only compatibility hack and violates
        # type hinting. This is scheduled for removal as per the decorator.
        return await client.find(  # type: ignore
            cls, results=results, offset=offset, promote_exact=promote_exact,
            check_case=check_case, **kwargs)

    @classmethod
    @deprecated('0.3', replacement='Client.get()')
    async def get(cls: Type[Ps2ObjectT], client: RequestClient,
                  check_case: bool = True, **kwargs: Any
                  ) -> Optional[Ps2ObjectT]:
        """Return the first entry matching the given terms.

        Like :meth:`Ps2Object.get()`, but will only return one item.

        Arguments:
            client: The client through which to perform the request.
            check_case (optional): Whether to check case when comparing
                strings. Note that case-insensitive searches are much
                more expensive. Defaults to ``True``.

        Returns:
            A matching entry, or None if not found.

        """
        # NOTE: The following is a runtime-only compatibility hack and violates
        # type hinting. This is scheduled for removal as per the decorator.
        return await client.get(  # type: ignore
            cls, results=1, check_case=check_case, **kwargs)

    @classmethod
    @deprecated('0.3', replacement='Client.get())')
    async def get_by_id(cls: Type[Ps2ObjectT], id_: int, *,
                        client: RequestClient) -> Optional[Ps2ObjectT]:
        """Retrieve an object by its unique Census ID.

        Arguments:
            id_: The unique ID of the object.
            client: The client through which to perform the request.

        Returns:
            The entry with the matching ID, or None if not found.

        """
        # NOTE: The following is a runtime-only compatibility hack and violates
        # type hinting. This is scheduled for removal as per the decorator.
        return await client.get_by_id(cls, id_)  # type: ignore

    def query(self) -> Query:
        """Return a query from the current object.

        This is a utility method targeted at advanced users and
        developers. It is generally not required for most use cases.
        """
        query = Query(self.collection, service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        return query


class Cached(Ps2Object, metaclass=abc.ABCMeta):
    """Base class for cacheable data types.

    This generates a cache for each subclass that allows the storage
    and retrieval of objects by ID. This cache may be customised using
    keyword arguments as part of the class definition.

    This customisation is done via two parameters: the cache size and
    the TTU.

    The cache size defines the maximum number of items the cache may
    bold before it will discard the least recently used item for every
    new item added.

    The TTU (time-to-use) will independently discard items that are
    older than the given number of seconds to ensure data does not go
    too far out of date.

    """

    _cache: ClassVar[TLRUCache[int, Any]]

    def __init__(self, data: CensusData, client: RequestClient) -> None:
        """Initialise the cached object.

        After initialising this object via the parent class's
        initialiser, this adds the current class to the cache.

        Arguments:
            data: The API response to instantiate the object from.
            client: The client used to retrieve the object.

        """
        super().__init__(data=data, client=client)
        self._cache.add(self.id, self)

    @classmethod
    def __init_subclass__(cls, cache_size: int,
                          cache_ttu: float = 0.0) -> None:
        """Initialise a cacheable subclass.

        This sets up the TLRU cache for the given subclass using the
        keyword arguments provided in the class definitions.

        Arguments:
            cache_size: The maximum number of items in the cache. Once
                the cache reaches this number of items, it will delete
                the  least recently used item for every new item added.
            cache_ttu (optional): The time-to-use for cache items. If
                an item is older than  TTU allows, it will be
                re-fetched regardless of how often it is accessed.
                Defaults to ``0.0``.

        """
        super().__init_subclass__()
        _log.debug('Setting up cache for %s (size: %d, ttu: %.1f sec.)',
                   cls.__name__, cache_size, cache_ttu)
        cls._cache = TLRUCache(size=cache_size, ttu=cache_ttu,
                               name=f'{cls.__name__}_Cache')

    @classmethod
    def alter_cache(cls, size: int, ttu: Optional[float] = None) -> None:
        """Modify the class cache to use a new size and TTU.

        This will update and clear the cache for the current class.
        This allows customisation of the class depending on your
        use-case.

        Arguments:
            size: The new cache size.
            ttu (optional): The new item TTU. Defaults to ``None``.

        Raises:
            ValueError: Raised if the size is less than 1.

        """
        if size < 1:
            raise ValueError(f'{size} is not a valid cache size')
        cls._cache.clear()
        cls._cache.size = size
        if ttu is not None:
            cls._cache.ttu = ttu

    @classmethod
    def _check_cache(cls: Type[CachedT], id_: int) -> Optional[CachedT]:
        """Attempt to restore an item from the cache.

        If the item cannot be found, ``None`` will be returned instead.

        Arguments:
            id_: The unique identifier the item is cached by.

        Returns:
            An existing instance if found, or ``None`` if the object
            has not been retrieved before or expired.

        """
        return cls._cache.get(id_)

    @classmethod
    @deprecated('0.3', replacement='Client.get()')
    async def get_by_id(cls: Type[CachedT], id_: int, *,  # type: ignore
                        client: RequestClient) -> Optional[CachedT]:
        """Retrieve an object by by ID.

        This query uses caches and might return an existing instance if
        the object has been recently retrieved.

        Arguments:
            id_: The unique id of the object.
            client: The client through which to perform the request.

        Returns:
            The object matching the given ID or ``None`` if no match
            was found.

        """
        _log.debug('<%s:%d> requested', cls.__name__, id_)
        if (instance := cls._cache.get(id_)) is not None:
            _log.debug('%r restored from cache', instance)
            return instance  # type: ignore
        _log.debug('<%s:%d> not cached, generating API query...',
                   cls.__name__, id_)
        return await super().get_by_id(id_, client=client)  # type: ignore


class Named(Cached, cache_size=0, cache_ttu=0.0, metaclass=abc.ABCMeta):
    """Mix-in class for named objects.

    This extends the functionality provided by :class:`Cached` to also
    cache objects retrieved via :meth:`Named.get_by_name()`. The cache
    will also store the locale used for the request.

    """

    _cache: ClassVar[TLRUCache[Union[int, str], Any]]  # type: ignore

    def __init__(self, *args: Any, locale: Optional[str] = None,
                 **kwargs: Any) -> None:
        """Initialise the named object.

        This sets the object's id attribute and adds it to the cache.

        Arguments:
            locale: The locale under which to cache this object.
            *args: Any extra positional arguments are forwarded to the
                :class:`Cached` class's initialiser.
            **kwargs: Any keyword arguments are forwarded to the
                :class:`Cached` class's initialiser.

        """
        super().__init__(*args, **kwargs)
        if (locale is not None
                and (name := getattr(self.name, locale, None)) is not None):
            key = f'{locale}_{name.lower()}'
            self._cache.add(key, self)

    def __repr__(self) -> str:
        """Return the unique string representation of the faction.

        This will take the form of ``<class:id:name>``, e.g.
        ``<Item:2:NC4 Mag-Shot>``.

        Returns:
            A string representing the object.

        """
        return (f'<{self.__class__.__name__}:{self.id}:'
                f'\'{self.name}\'>')

    def __str__(self) -> str:
        """Return the string representation of this object.

        This retrieves the :atr:``Named.name`` attribute for the
        English locale.

        Returns:
            A string representation of the object.

        """
        return str(self.name)

    @classmethod
    @deprecated('0.3', replacement='Client.get()')
    async def get_by_name(cls: Type[NamedT], name: str, *, locale: str = 'en',
                          client: RequestClient) -> Optional[NamedT]:
        """Retrieve an object by its unique name.

        If the same query has been performed recently, it may be
        restored from cache instead.

        This query is always case-insensitive.

        Arguments:
            name: The name to search for.
            locale (optional): The locale of the search key. Defaults
                to ``'en'``.
            client: The client through which to perform the request.

        Returns:
            The entry with the matching name, or ``None`` if not found.

        """
        # NOTE: The following is a runtime-only compatibility hack and violates
        # type hinting. This is scheduled for removal as per the decorator.
        return client.get_by_name(cls, name, locale=locale)  # type: ignore


class ImageMixin(Ps2Object, metaclass=abc.ABCMeta):
    """A mixin class for types supporting image access."""

    def image(self) -> str:
        """Return the default image for this type."""
        image_id: int = self.data.image_id  # type: ignore
        return self._image_url(image_id)

    @staticmethod
    def _image_url(image_id: int) -> str:
        """Return the URL for a given image ID."""
        url = 'https://census.daybreakgames.com/files/ps2/images/static/'
        return url + f'{image_id}.png'
