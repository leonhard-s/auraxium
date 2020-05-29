"""Unit tests for the auraxium.cache sub module."""

import time
import unittest
from auraxium.cache import TLRUCache


class TestCache(unittest.TestCase):
    """Tests for the TLRUCache class and associated methods."""

    def test_add(self) -> None:
        """Test the addition of objects into the cache."""
        cache: TLRUCache[int, str] = TLRUCache(10, -1)
        cache.add(0, 'Bogus')
        self.assertDictEqual(cache.items(), {0: 'Bogus'})

    def test_add_many(self) -> None:
        """Test the addition of multiple objects into the cache."""
        test_dict = {i: f'Item {i}' for i in range(10)}
        cache: TLRUCache[int, str] = TLRUCache(10, -1, )
        cache.add_many(test_dict.items())
        self.assertDictEqual(cache.items(), test_dict)

    def test_clear(self) -> None:
        """Test the cache clearing function."""
        cache: TLRUCache[int, str] = TLRUCache(10, -1)
        cache.add(0, 'Bogus')
        cache.clear()
        self.assertDictEqual(cache.items(), {})

    def test_lru(self) -> None:
        """Test the cache freeing method."""
        test_dict = {i: f'Item {i}' for i in range(1, 11)}
        cache: TLRUCache[int, str] = TLRUCache(10, -1)
        cache.add(0, 'Item 0')
        cache.add_many(test_dict.items())
        self.assertDictEqual(cache.items(), test_dict)

    def test_get(self) -> None:
        """Test the cache's item retrieval method."""
        test_dict = {i: f'Item {i}' for i in range(1, 11)}
        cache: TLRUCache[int, str] = TLRUCache(10, -1)
        cache.add_many(test_dict.items())
        item = cache.get(5)
        self.assertEqual(item, 'Item 5')
        self.assertEqual(cache.values()[-1], 'Item 5')

    def test_items(self) -> None:
        """Test the items view method."""
        test_dict = {i: f'Item {i}' for i in range(1, 11)}
        cache: TLRUCache[int, str] = TLRUCache(10, -1)
        cache.add_many(test_dict.items())
        self.assertEqual(cache.items(), test_dict)

    def test_expired(self) -> None:
        """Test the expiration feature."""
        cache: TLRUCache[int, str] = TLRUCache(10, .1)
        cache.add(0, 'Bogus')
        self.assertEqual(cache.get(0), 'Bogus')
        time.sleep(0.1)
        self.assertIsNone(cache.get(0))

    def rest_lru(self) -> None:
        """Test the LRU discarding feature."""
        cache: TLRUCache[int, str] = TLRUCache(10, -1)
        cache.add(0, 'Apple')
        cache.add(1, 'Banana')
        _ = cache.get(0)
        cache.remove_lru(count=1)
        self.assertIsNone(cache.get(0))
        self.assertEqual(cache.get(1), 'Banana')
