import sys
from datetime import datetime


_cache_list = []  # Used for iterating over all caches


class Cache():
    """A cache stores instances of other objects.

    Caches are used to reduce the number of times an object needs to be
    re-created to reduce network traffic. They can be size-limited (only keep
    x items and discard the oldest ones), age-limited (keep items for y seconds
    before discarding them) or both.

    """

    def __init__(self, max_size=None, max_age=None):
        self._contents = {}
        self.max_age = max_age  # Rename to something like "idle time"?
        self.max_size = max_size
        self._meta_list = []  # Contains tuples like (<id>, <last_used>)

        # Add the cache to the cache list
        _cache_list.append(self)

    def __contains__(self, item):
        return True if item in self._contents.keys() else False

    def __getitem__(self, key):
        return self._contents[key]

    def __len__(self):
        return len(self._meta_list)

    def add(self, item):
        """Adds a new item to the cache."""
        # No caching of non-existing objects
        if item is None:
            return

        # Only proceed if the item has not already been cached
        if item.id in self._contents.keys():
            return

        try:
            # If the cache is full, delete the oldest item
            if len(self._meta_list) >= self.max_size:
                del self._contents[self._meta_list.pop(0)[0]]
        except TypeError:
            # The TypeError is raised in case max_size has not been set
            pass

        self._contents[str(item.id)] = item
        self._meta_list.append((str(item.id), datetime.utcnow()))

    def clear(self):
        """Removes all stored items from the cache."""
        self._contents = {}
        self._meta_list = []

    def _get_size(self):
        """Returns the size of the cache."""
        return sys.getsizeof(self._contents)

    def load(self, id_):
        """Returns an item."""
        return self._contents[id_]

    def trim(self):
        """Checks if any items are scheduled for deletion."""
        now = datetime.utcnow()
        trim_list = [t for t in self._meta_list if now > t[1] + self.max_age]
        for t in trim_list:
            del self._contents[t[0]]
            self._meta_list.remove(t)


def trim_caches():
    _ = [c.trim() for c in _cache_list]
