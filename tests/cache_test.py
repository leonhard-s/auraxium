"""Unit tests for the auraxium.cache sub module."""

import logging
import time
import unittest

from auraxium.cache import TLRUCache

# Logger added with no handlers to trigger debug clauses in the code
log = logging.getLogger('auraxium.cache')
log.setLevel(logging.DEBUG)


class TestCacheInterface(unittest.TestCase):
    """Test the class interface of the TLRUCache."""

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
        cache: TLRUCache[int, str] = TLRUCache(10, .01)
        cache.add(0, 'Bogus')
        self.assertEqual(cache.get(0), 'Bogus')
        time.sleep(0.01)
        self.assertIsNone(cache.get(0))

    def test_lru(self) -> None:
        """Test TLRUCache.lru()"""
        cache: TLRUCache[int, str] = TLRUCache(10, -1)
        cache.add(0, 'Apple')
        cache.add(1, 'Banana')
        _ = cache.get(0)
        cache.remove_lru(count=1)
        self.assertIsNone(cache.get(0))
        self.assertEqual(cache.get(1), 'Banana')

    def test_size(self) -> None:
        """Test TLRUCache.size()"""
        test_dict = {i: f'Item {i}' for i in range(1, 11)}
        cache: TLRUCache[int, str] = TLRUCache(10, -1)
        cache.add(0, 'Item 0')
        cache.add_many(test_dict.items())
        self.assertDictEqual(cache.items(), test_dict)
