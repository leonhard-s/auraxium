"""Unit tests for the auraxium.cache sub module."""

import datetime
import logging
import unittest
from typing import Any

from auraxium._cache import TLRUCache


class CacheFilter(logging.Filter):
    """This filter hides the cache debug statements from the user.

    For testing reasons, these are always enabled, but they should not
    propagate out into the unit testing script.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        """Return whether the given record should be recorded."""
        return record.name != 'auraxium.cache'


# Logger added with no handlers to trigger debug clauses in the code
log = logging.getLogger('auraxium.cache')
log.setLevel(logging.DEBUG)
log.addFilter(CacheFilter())


class TestCacheInterface(unittest.TestCase):
    """Test the class interface of the TLRUCache class."""

    def test_iter(self) -> None:
        """Test TLRUCache.__iter__()"""
        cache: TLRUCache[int, str] = TLRUCache(10, -1)
        cache.add(0, 'Bogus')
        keys = list(cache)
        self.assertListEqual(keys, [0])

    def test_add(self) -> None:
        """Test TLRUCache.add()"""
        cache: TLRUCache[int, str] = TLRUCache(10, -1)
        cache.add(0, 'Bogus')
        self.assertDictEqual(cache.items(), {0: 'Bogus'})

    def test_add_many(self) -> None:
        """Test TLRUCache.add_many()"""
        input_data = {i: f'Item {i}' for i in range(10)}
        cache: TLRUCache[int, str] = TLRUCache(10, -1)
        cache.add_many(input_data.items())
        self.assertDictEqual(cache.items(), input_data)
        cache.add_many([])  # Trigger the fail-early clause

    def test_clear(self) -> None:
        """Test TLRUCache.clear()"""
        cache: TLRUCache[int, str] = TLRUCache(10, -1)
        cache.add(0, 'Bogus')
        self.assertNotEqual(len(cache), 0)
        cache.clear()
        self.assertDictEqual(cache.items(), {})

    def test_contains(self) -> None:
        """Test TLRUCache.__contains__()"""
        cache: TLRUCache[int, int] = TLRUCache(5, -1)
        self.assertFalse(1 in cache)
        cache.add(1, 2)
        self.assertTrue(1 in cache)

    def test_footprint(self) -> None:
        """Test TLRUCache.footprint()"""
        # NOTE: Since sys.getsizeof() is an estimate, there is no way of
        # ensuring the actual value returned is accurate.
        # This only checks that the internal OrderedDict gets larger or smaller
        # as items are added or removed.
        cache: TLRUCache[int, int] = TLRUCache(10, -1)
        cache.add(0, 1)
        size = cache.footprint()  # Initial reading
        cache.add(0, 2)  # Replace the initial item
        self.assertEqual(size, cache.footprint())  # Size should not change
        cache.add(1, 3)
        self.assertGreater(cache.footprint(), size)  # Size should increase
        size = cache.footprint()
        cache.remove_lru(1)
        self.assertLess(cache.footprint(), size)  # Size should decrease

    def test_free(self) -> None:
        """Test TLRUCache.free()"""
        cache: TLRUCache[int, str] = TLRUCache(16, -1)
        cache.add_many({i: str(i) for i in range(16)}.items())
        self.assertEqual(len(cache), 16)
        cache.free(2)
        self.assertEqual(len(cache), 14)
        with self.assertRaises(ValueError):
            cache.free(20)  # Freeing more than the cache size is not possible
        cache.free(16)
        self.assertEqual(len(cache), 0)

    def test_get(self) -> None:
        """Test TLRUCache.get()"""
        input_data = {i: f'Item {i}' for i in range(1, 11)}
        cache: TLRUCache[int, str] = TLRUCache(10, -1)
        cache.add_many(input_data.items())
        item = cache.get(3)
        self.assertEqual(item, 'Item 3')
        self.assertEqual(cache.values()[-1], 'Item 3')

    def test_items(self) -> None:
        """Test TLRUCache.items()"""
        test_dict = {i: f'Item {i}' for i in range(1, 11)}
        cache: TLRUCache[int, str] = TLRUCache(10, -1)
        cache.add_many(test_dict.items())
        self.assertEqual(cache.items(), test_dict)

    def test_expired(self) -> None:
        """Test TLRUCache.expired()"""
        cache: TLRUCache[int, str] = TLRUCache(10, 1.0)
        cache.add(0, 'Bogus')
        self.assertEqual(cache.get(0), 'Bogus')
        _age_up(cache, 0, 10.0)
        self.assertIsNone(cache.get(0))

    def test_last_accessed(self) -> None:
        """Test TLRUCache.last_accessed()"""
        cache: TLRUCache[int, str] = TLRUCache(10, -1)
        cache.add(0, 'Bogus')
        offset = datetime.timedelta(0.1)
        start = datetime.datetime.now() - offset
        _ = cache.get(0)
        end = datetime.datetime.now() + offset
        self.assertTrue(start < cache.last_accessed(0) < end)
        # Test ValueError
        with self.assertRaises(ValueError):
            _ = cache.last_accessed(1)

    def test_lru(self) -> None:
        """Test TLRUCache.get"""
        cache: TLRUCache[int, str] = TLRUCache(10, -1)
        cache.add(0, 'Apple')
        cache.add(1, 'Banana')
        _ = cache.get(0)
        cache.remove_lru(count=1)
        self.assertIsNone(cache.get(0))
        self.assertEqual(cache.get(1), 'Banana')

    def test_remove_expired(self) -> None:
        """Test TLRUCache.remove_expired()"""
        # Test the auto-discard feature for outdated items
        cache: TLRUCache[int, str] = TLRUCache(10, 4.0)
        cache.add(0, 'Apple')
        _age_up(cache, 0, 3.0)
        self.assertEqual(cache.remove_expired(), 0)
        cache.add(1, 'Banana')
        _age_up(cache, 0, 5.0)
        self.assertEqual(cache.remove_expired(), 1)
        _age_up(cache, 1, 10.0)
        self.assertEqual(cache.remove_expired(), 1)

    def test_remove_lru(self) -> None:
        """Test TLRUCache.remove_lru()"""
        cache: TLRUCache[int, str] = TLRUCache(10, -1)
        cache.add(0, 'Apple')
        cache.add(1, 'Banana')
        _ = cache.get(0)
        cache.remove_lru(count=1)
        self.assertIsNone(cache.get(0))
        self.assertEqual(cache.get(1), 'Banana')
        # Check errors
        with self.assertRaises(ValueError):
            cache.remove_lru(-1)
        with self.assertRaises(ValueError):
            cache.remove_lru(cache.size+1)

    def test_size(self) -> None:
        """Test TLRUCache.size()"""
        test_dict = {i: f'Item {i}' for i in range(1, 11)}
        cache: TLRUCache[int, str] = TLRUCache(10, -1)
        cache.add(0, 'Item 0')
        cache.add_many(test_dict.items())
        self.assertDictEqual(cache.items(), test_dict)


def _age_up(cache: TLRUCache[Any, Any], item: int, age: float) -> None:
    """Set a cache item's age to the given number of seconds.

    This mutates the associated cache entry, allowing to pretend time
    having passed without needing to slow down execution with sleeps.
    """
    mock_time = datetime.datetime.now() - datetime.timedelta(seconds=age)
    # pylint: disable=protected-access
    cache._data[item].first_added = mock_time  # type: ignore
