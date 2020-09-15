"""Object caching system.

This defines a generic cache that can be used to keep local copies of
remote data. This is especially useful for small but expensive queries
like character name resolution.

"""

import dataclasses
import datetime
import logging
import sys
from collections import OrderedDict
from typing import (Any, Dict, Generic, Hashable, Iterable, Iterator, List,
                    Optional, Tuple, TypeVar)

__all__ = [
    'TLRUCache'
]

K = TypeVar('K', bound=Hashable)  # pylint: disable=invalid-name
V = TypeVar('V', bound=Any)  # pylint: disable=invalid-name
log = logging.getLogger('auraxium.cache')


@dataclasses.dataclass()
class CacheItem(Generic[V]):
    """Small dataclass for cache items.

    This can be thought of as a mutable named tuple.

    Attributes:
        value: The instance being cached
        access_counter: The number of times the item has been retrieved
            from the cache.
        first_added: The time the object was added. Used to calculate
            the age of the entry with respect to a :class:`TLRUCache`'s
            :attr`~TLRUCache.ttu` attribute.
        last_accessed: The last time the object was added. Used for the
            least-recently-used component of the cache.

    """

    value: V
    access_counter: int
    first_added: datetime.datetime
    last_accessed: datetime.datetime


class TLRUCache(Generic[K, V]):
    """Basic time-aware Least Recently Used (TLRU) cache.

    This will hold on to a given item for a set amount of time while
    also discarding the least recently used item if the cache is full.

    This uses two parameters: size and ttu (time-to-use). The size
    defines the maximum number of objects the cache may hold at any
    given time. The time-to-use is the number of seconds an object is
    valid in the cache before it expires and must be re-queried.

    Attributes:
        size: The maximum number of items the cache may hold.
        ttu: The time in seconds that a cache item will be valid. If
            set to zero or less, the cache will behave like a regular
            LRU cache.

    """

    def __init__(self, size: int, ttu: float,
                 name: Optional[str] = None) -> None:
        """Initialise a new, empty TLRU cache.

        Arguments:
            size: The maximum number of items in the cache.
            ttu: The time-to-use for items in this cache. Set to zero
                or less to cache objects indefinitely.
            name (optional): A display name to use for this cache.
                Useful for debugging as this name will be used by the
                logs. Defaults to ``None``.

        """
        # NOTE: Mypy currently does not support type hinting the OrderedDict
        # object in-code, hence the string literal type.
        self._data: 'OrderedDict[K, CacheItem[V]]' = OrderedDict()
        self.name = name or 'TLRUCache'
        self.size = size
        self.ttu = ttu

    def __contains__(self, key: str) -> bool:
        """Return whether the given key exists in the cache."""
        return key in self._data.keys()

    def __iter__(self) -> Iterator[K]:
        """Return an iterator over the cache keys."""
        return iter(self._data)

    def __len__(self) -> int:
        """Return the number of elements in the cache.

        This will remove any expired keys before calculation.
        """
        self.remove_expired()
        return len(self._data)

    def add(self, key: K, item: V) -> None:
        """Add a new item to the cache.

        If the cache is full, this will clear any expired items (i.e.
        items who's age is greater than the TTU set for the cache)
        before removing the least recently used item.

        Arguments:
            key: The unique identifier of the object added.
            item: The object to store in the cache.

        """
        now = datetime.datetime.now()
        log.debug('%s: Adding %s instance under key %d',
                  self.name, item.__class__.__name__, key)
        self.free(count=1)
        self._data[key] = CacheItem(item, 0, now, now)

    def add_many(self, items: Iterable[Tuple[K, V]]) -> None:
        """Add multiple items to the cache.

        If the cache is full, this will clear any expired items (i.e.
        items who's age is greater than the TTU set for the cache)
        before removing the necessary number of least recently used
        items.

        Arguments:
            items: An iterable of tuples containing the ID/object pairs
                to add to the cache.

        Raises:
            ValueError: Raised if the number of items to add exceeds
                the size of the cache.

        """
        now = datetime.datetime.now()
        data = {k: CacheItem(v, 0, now, now) for k, v in items}
        if not data:
            log.debug('%s: add_many called with empty iterable', self.name)
            return
        count = len(data)
        if log.isEnabledFor(logging.DEBUG):
            item = next(iter(data.values()))
            log.debug('%s: Adding %d %s instances',
                      self.name, count, item.value.__class__.__name__)
        self.free(count=count)
        self._data.update(data)

    def clear(self) -> None:
        """Clear the cache, removing all items."""
        if log.isEnabledFor(logging.DEBUG):
            count = len(self._data)
            log.debug('%s: Clearing cache: %d item%s will be removed',
                      self.name, count, 's' if count > 1 else '')
        self._data.clear()

    def footprint(self) -> int:
        """Return the size of the cache items in bytes.

        Note that this is not an exact value, but can still be useful
        for profiling.

        Returns:
            The size of the cache in bytes.

        """
        return sys.getsizeof(self._data)

    def free(self, count: int = 1) -> int:
        """Release items from the cache.

        This will clear any expired items, followed by as many of the
        least recently used items as required to accommodate the number
        of items specified via the ``count`` argument.

        The number of slots freed may exceed the number of slots
        requested due to all expired items being cleared.

        Arguments:
            count (optional): The number of free slots to request.
                Defaults to ``1``.

        Raises:
            ValueError: Raised if the number of requested free slots
                exceeds the size of the cache.

        Returns:
            The number of available slots in the cache. This may be
            greater than the number of slots requested.

        """
        if count > self.size:
            raise ValueError(f'Unable to provide {count} available slots, '
                             f'{self.name} can only hold {self.size} items')
        available = self.size - len(self._data)
        if log.isEnabledFor(logging.DEBUG):
            log.debug('%s: %d slot%s requested (available: %d)',
                      self.name, count, 's' if count > 1 else '', available)
        if self.ttu > 0:
            available += self.remove_expired()
        if available >= count:
            return available
        self.remove_lru(count=count-available)
        return count

    def get(self, key: K) -> Optional[V]:
        """Retrieve an item from the cache.

        Arguments:
            key: The unique identifier of the object to retrieve.

        Returns:
            The object stored under the given identifier, or ``None``
            if it is not found or expired (i.e. its age exceeds the TTU
            set for the cache).

        """
        now = datetime.datetime.now()
        try:
            item = self._data[key]
        except KeyError:
            log.debug('%s: Key %s not found', self.name, key)
            return None
        item.access_counter += 1
        if self.ttu > 0:
            age = now - item.first_added
            if age.total_seconds() > self.ttu:
                log.info('%s: Key %d expired, age: %.1f sec. (max: %.1f sec.)',
                         self.name, key, age.total_seconds(), self.ttu)
                del self._data[key]
                return None
        else:
            log.debug('%s: Skipping expiration check (TTU %d)',
                      self.name, self.ttu)
        log.debug('%s: Key %d found, moving to top', self.name, key)
        self._data.move_to_end(key, last=True)
        item.last_accessed = now
        self._data[key] = item
        return item.value

    def items(self) -> Dict[K, V]:
        """Return a mapping of all key/value pairs in the cache.

        Note that this is mostly intended for introspection and
        troubleshooting, you should only use :meth:`TLRUCache.get()` to
        retrieve items from the cache.

        This method will not update the items'
        :attr:`CacheItem.last_accessed` value or increment their
        :attr:`CacheItem.access_counter`.

        Returns:
            A dictionary containing all items in the cache, with more
            recently accessed items first.

        """
        return {k: v.value for k, v in self._data.items()}

    def last_accessed(self, key: K) -> datetime.datetime:
        """Return the time the given item was last accessed.

        Unlike :meth:`TLRUCache.get()`, this does not perform an
        expiration check and also will not push the retrieved item to
        the top of the cache.

        This method is intended for introspection and troubleshooting,
        but is also not very expensive.

        Arguments:
            key: The unique identifier of the item to check.

        Raises:
            ValueError: Raised if the given identifier is not found.

        Returns:
            The time the given item was last accessed.

        """
        try:
            item = self._data[key]
        except KeyError as err:
            raise ValueError(f'Key not found: {key}') from err
        return item.last_accessed

    def remove_expired(self) -> int:
        """Remove any expired items from the cache.

        Returns:
            The number of items removed from the cache.

        """
        if self.ttu <= 0:
            logging.warning('%s: remove_expired called with TTU disabled',
                            self.name)
            return 0
        now = datetime.datetime.now()
        keys_to_remove: List[K] = []
        for key, data in self._data.items():
            age = now - data.first_added
            if age.total_seconds() > self.ttu:
                keys_to_remove.append(key)
        _ = [self._data.pop(k) for k in keys_to_remove]
        count = len(keys_to_remove)
        log.debug('%s: Removed %d expired items', self.name, count)
        return count

    def remove_lru(self, count: int = 1) -> None:
        """Remove the given number of items from the cache.

        This will remove the least recently used (LRU) items first.

        Arguments:
            count (optional): The number of items to remove. Defaults
            to ``1``.

        Raises:
            ValueError: raised if the number of items to remove is
                negative
            ValueError: Raised if the number of items to remove exceeds
                the size of the cache.

        """
        if count < 0:
            raise ValueError('count may not be negative')
        if count > self.size:
            raise ValueError(f'Unable to remove {count} items from '
                             f'{self.name}, cache size is set to {self.size} '
                             'items')
        log.debug('%s: Removing %d LRU items', self.name, count)
        for _ in range(count):
            _ = self._data.popitem(last=True)

    def values(self) -> List[V]:
        """Return a list of all items in the cache.

        Note that this is mostly intended for introspection and
        troubleshooting, you should only use TLRUCache.get() to
        retrieve items from the cache.

        Returns:
            A list of all items in the cache.

        """
        return [v.value for v in self._data.values()]
