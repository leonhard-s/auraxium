"""Base classes used by the Auraxium object model."""

import abc
import logging
import warnings
from typing import (Any, ClassVar, List, Optional, Tuple, Type, TYPE_CHECKING,
                    TypeVar, Union)

from .cache import TLRUCache
from .census import Query
from .errors import BadPayloadError
from .request import extract_payload, extract_single, run_query
from .types import CensusData, CensusInfo
from .utils import nested_dict_get, nested_dict_pop

if TYPE_CHECKING:
    # This is only imported when type checking is performed to avoid a circular
    # import
    from .client import Client

__all__ = ['Ps2Object', 'Cached', 'Named']

CachedT = TypeVar('CachedT', bound='Cached')
NamedT = TypeVar('NamedT', bound='Named')
Ps2ObjectT = TypeVar('Ps2ObjectT', bound='Ps2Object')
log = logging.getLogger('auraxium.ps2')


class Ps2Object(metaclass=abc.ABCMeta):
    """Common base class for all PS2-related objects.

    Subclasses must implement the abstract Ps2Object._extract_fields()
    method used to validate Census API responses before storage.
    """

    # NOTE: These names will be overwritten by the abstract class properties
    # below, but mypy seems to be confused by them, typing them as
    # Callable[[], str].
    # This is redundant but ensures mypy can supply correct type hints for
    # these attributes while still requiring subclasses to overwrite them.
    _collection: ClassVar[str] = ''
    _id_field: ClassVar[str] = ''
    _census_info: ClassVar[CensusInfo]

    @property  # type: ignore
    @classmethod
    @abc.abstractmethod
    def _collection(cls) -> str:
        raise NotImplementedError

    @property  # type: ignore
    @classmethod
    @abc.abstractmethod
    def _id_field(cls) -> str:
        raise NotImplementedError

    def __init__(self, payload: CensusData, client: 'Client'):
        """Initialise the object.

        This sets the object's id attribute and populates it using the
        provided payload.

        Args:
            payload: The census response dictionary to populate the
                object with.
            client (optional): The client object to use for requests
                performed via this object. Defaults to None.

        """
        id_ = int(payload.pop(self._id_field))
        log.debug('Instantiating <%s:%d> using payload: %s',
                  self.__class__.__name__, id_, payload)
        self.id = id_  # pylint: disable=invalid-name
        self._client = client
        try:
            self._data = self._process_payload(payload)
        except KeyError as err:
            raise BadPayloadError(
                f'Unable to populate {self.__class__.__name__} due to a '
                f'missing key: {err.args[0]}') from err
        if payload:
            warnings.warn(f'Encountered {len(payload)} unexpected keys while '
                          f'instantiating {self}: {", ".join(payload.keys())}')

    def __repr__(self) -> str:
        """Return the unique string representation of this object.

        This will take the form of <Class:id>, e.g. <Faction:2>.

        Returns:
            A string representing the object.

        """
        return f'<{self.__class__.__name__}:{self.id}>'

    @classmethod
    async def count(cls: Type[Ps2ObjectT], client: 'Client',
                    **kwargs: Any) -> int:
        """Return the number of items matching the given terms.

        Args:
            client: The client through which to perform the request.
            **kwargs: Any number of filters to apply.

        Returns:
            The number of entries entries.

        """
        service_id = 's:example' if client is None else client.service_id
        query = Query(cls._collection, service_id=service_id, **kwargs)
        result = await run_query(query, verb='count')
        try:
            return int(result['count'])
        except KeyError as err:
            raise BadPayloadError(
                'Missing key "count" in API response') from err
        except ValueError as err:
            raise BadPayloadError(f'Invalid count: {result["count"]}') from err

    @classmethod
    async def find(cls: Type[Ps2ObjectT], results: int = 10, *,
                   offset: int = 0,
                   promote_exact: bool = False, check_case: bool = True,
                   client: 'Client', **kwargs: Any) -> List[Ps2ObjectT]:
        """Return a list of entries matching the given terms.

        This returns up to as many entries as indicated by the results
        argument. Note that it may be fewer.

        Args:
            results (optional): The maximum number of results. Defaults
                to 10.
            offset (optional): The number of entries to skip. Useful
                for paginated views. Defaults to 0.
            promote_exact (optional): If enabled, exact matches to
                non-exact searches will always come first in the return
                list. Defaults to False.
            check_case (optional): Whether to check case when comparing
                strings. Note that case-insensitive searches are much
                more expensive. Defaults to True.
            client: The client through which to perform the request.
            **kwargs: Any number of filters to apply.

        Returns:
            A list of matching entries.

        """
        kwargs = dict(cls._translate_field(k, v) for k, v in kwargs.items())
        service_id = 's:example' if client is None else client.service_id
        query = Query(cls._collection, service_id=service_id, **kwargs)
        query.limit(results)
        if offset > 0:
            query.offset(offset)
        query.exact_match_first(promote_exact).case(check_case)
        matches = await run_query(query, verb='get')
        return [cls(i, client=client) for i in extract_payload(
            matches, cls._collection)]

    @classmethod
    async def get(cls: Type[Ps2ObjectT], client: 'Client',
                  check_case: bool = True, **kwargs: Any
                  ) -> Optional[Ps2ObjectT]:
        """Return the first entry matching the given terms.

        Like Ps2Object.get(), but will only return one item.

        Args:
            client: The client through which to perform the request.
            check_case (optional): Whether to check case when comparing
                strings. Note that case-insensitive searches are much
                more expensive. Defaults to True.

        Returns:
            A matching entry, or None if not found.

        """
        results = await cls.find(client=client, results=1,
                                 check_case=check_case, **kwargs)
        if results:
            return results[0]
        return None

    @classmethod
    async def get_by_id(cls: Type[Ps2ObjectT], id_: int, *, client: 'Client'
                        ) -> Optional[Ps2ObjectT]:
        """Retrieve an object by its unique Census ID.

        Args:
            id_: The unique ID of the object.
            client: The client through which to perform the request.

        Returns:
            The entry with the matching ID, or None if not found.

        """
        filters: CensusData = {cls._id_field: id_}
        results = await cls.find(
            client=client, results=1, **filters)
        if results:
            return results[0]
        return None

    @classmethod
    def _process_payload(cls, payload: CensusData) -> CensusData:
        data: CensusData = {}
        for census_name, arx_name in cls._census_info.fields.items():
            value = nested_dict_pop(payload, census_name)
            if census_name in cls._census_info.converter:
                value = cls._census_info.converter[census_name]
            data[arx_name] = value
        # for census_name in cls._census_info.exclude:
        #     _ = nested_dict_pop(payload, census_name)
        return data

    @classmethod
    def _translate_field(cls, arx_name: str, value: Any) -> Tuple[str, Any]:
        inverted = {v: k for k, v in cls._census_info.fields.items()}
        try:
            census_name = inverted[arx_name]
        except KeyError:
            census_name = arx_name
        if arx_name in cls._census_info.converter:
            value = cls._census_info.converter[arx_name](value)
        return census_name, value


class Cached(Ps2Object, metaclass=abc.ABCMeta):
    """Base class for cachable data types.

    This generates a cache for each subclass that allows the storage
    and retrieval of objects by ID. This cache can be customised using
    keyword arguments as part of the class definition.

    This customisation is done via two parameters: the cache size and
    the TTU.

    The cache size defines the maximum number of items the
    cache may bold before it will discard the least recently used item
    for every new item added.

    The TTU (time-to-use) will independently
    discard items that are older than the given number of seconds to
    ensure data does not go too far out of date.
    """

    _cache: ClassVar[TLRUCache[int, Any]]

    def __init__(self, payload: CensusData,
                 client: 'Client') -> None:
        """Initialise the cached object."""
        super().__init__(payload=payload, client=client)
        self._cache.add(self.id, self)

    @classmethod
    def __init_subclass__(cls: Type[CachedT], cache_size: int,
                          cache_ttu: float = 0.0) -> None:
        """Initialise a cachable subclass.

        This sets up the TLRU cache for the given subclass using the
        keyword arguments provided.

        Args:
            cache_size: The maximum number of items in the cache. Once
                the cache reaches this number of items, it will delete
                the  least recently used item for every new item added.
            cache_ttu (optional): The time-to-use for cache items. If
                an item is older than its TTU allows, it will be
                re-fetched regardless of how often it is accessed.
                Defaults to 0.0.

        """
        super().__init_subclass__()
        log.debug('Setting up cache for %s (size: %d, ttu: %.1f sec.)',
                  cls.__name__, cache_size, cache_ttu)
        cls._cache = TLRUCache(size=cache_size, ttu=cache_ttu,
                               name=f'{cls.__name__}_Cache')

    @classmethod
    def alter_cache(cls, size: int, ttu: Optional[float] = None) -> None:
        """Modify the class cache to use a new size and TTU.

        This will update and clear the cache for the current class.

        Args:
            size: The new cache size.
            ttu (optional): The new item TTU. Defaults to None.

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

        If the item cannot be found, None will be returned instead.

        Args:
            id_: The unique identifier the item is cached by.

        Returns:
            An existing instance if found, or None if the object has
            not been retrieved before or expired.

        """
        return cls._cache.get(id_)

    @classmethod
    async def get_by_id(cls: Type[CachedT], id_: int, *, client: 'Client'
                        ) -> Optional[CachedT]:
        """Retrieve an object by by ID.

        This query uses caches and might return an existing instance if
        the object has been recently retrieved. Use the no_cache flag
        to force retrieval of fresh data.

        If no session is provided, one will be created locally. It is
        highly recommended to always specify a session object.

        Args:
            id_: The unique id of the object.
            client: The client through which to perform the request.

        Returns:
            The object matching the given ID or None if no match was
            found.

        """
        filters: CensusData = {cls._id_field: id_}
        log.debug('<%s:%d> requested', cls.__name__, id_)
        if (instance := cls._cache.get(id_)) is not None:
            log.debug('%r restored from cache', instance)
            return instance  # type: ignore
        log.debug('<%s:%d> not cached, generating API query...',
                  cls.__name__, id_)
        return await cls.get(client=client, **filters)


class Named(Cached, cache_size=0, cache_ttu=0.0, metaclass=abc.ABCMeta):
    """Mix-in class for named objects."""

    _cache: ClassVar[TLRUCache[Union[int, str], Any]]  # type: ignore

    def __init__(self, *args: Any, locale: Optional[str] = None,
                 **kwargs: Any) -> None:
        """Initialise the named object.

        This sets the object's id attribute and adds it to the cache.

        Args:
            locale: The locale under which to cache this object.
            *args: Any extra positional argumetns are forwarded to the
                Cached class's initialiser.
            **kwargs: Any keyword arguments are forwarded to the
                Cached class's initialiser.

        """
        super().__init__(*args, **kwargs)
        if locale is not None:
            key = f'{locale}_{self.name(locale=locale).lower()}'
            self._cache.add(key, self)

    def __str__(self) -> str:
        """Return the string representation of this object.

        This calls the Named.name() method for the English locale.

        Returns:
            A string representaiton of the object.

        """
        return self.name(locale='en')

    @classmethod
    async def get_by_name(cls: Type[NamedT], name: str, *, locale: str = 'en',
                          client: 'Client') -> Optional[NamedT]:
        """Retrieve an object by its unique name.

        This query is always case-insensitive.

        Args:
            name: The name to search for.
            locale (optional): The locale of the search key. Defaults
                to 'en'.
            client: The client through which to perform the request.

        Returns:
            The entry with the matching name, or None if not found.

        """
        key = f'{locale}_{name.lower()}'
        log.debug('%s "%s"[%s] requested', cls.__name__, name, locale)
        if (instance := cls._cache.get(key)) is not None:
            log.debug('%r restored from cache', instance)
            return instance  # type: ignore
        log.debug('%s "%s"[%s] not cached, generating API query...',
                  cls.__name__, name, locale)
        query = Query(cls._collection).case(False).add_term(
            field=f'name.{locale}', value=name)
        payload = await run_query(query)
        payload = extract_single(payload, cls._collection)
        return cls(payload, locale=locale, client=client)

    def name(self, locale: str = 'en') -> str:
        """Return the localised name of the object.

        Args:
            locale (optional): The locale identifier to return.
                Defaults to 'en'.

        Raises:
            ValueError: Raised if the given locale is unknown.

        Returns:
            The localised name of the object.

        """
        try:
            return str(self._data['name'][locale])
        except KeyError as err:
            raise ValueError(f'Invalid locale: {locale}') from err
