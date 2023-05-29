"""Unit tests for custom types implemented by Auraxium."""

import unittest

from auraxium.types import LocaleData


class TestLocaleData(unittest.TestCase):
    """Test that the LocaleData class members are behaving."""

    _LOCALES = ['de', 'en', 'es', 'fr', 'it']

    def test_dunder_str(self) -> None:
        """Test the __str__ dunder method."""
        loc = LocaleData(**{s: f'Test_{s}' for s in self._LOCALES})
        self.assertEqual(str(loc), 'Test_en')
        # Test repr fallback when no locale is set
        loc = LocaleData(**{s: None for s in self._LOCALES})
        self.assertEqual(str(loc), repr(loc))

    def test_empty_factory(self) -> None:
        """Test the dummy data factory method."""
        loc = LocaleData.empty()
        self.assertEqual(loc, LocaleData(**{s: None for s in self._LOCALES}))
