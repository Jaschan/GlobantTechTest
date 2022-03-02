import unittest
from unittest.mock import patch, MagicMock, Mock
import tools

class TestCache(unittest.TestCase):
    @patch('tools.weather._timestamp', MagicMock(return_value=123456))
    def test_store_in_cache(self):
        key = ("city", "country")
        item = {"fake": "item"}
        tools.weather._store_in_cache(key, item)
        self.assertEqual(tools.weather._cache[key], (123456, item))
        assert tools.weather._timestamp.called

    @patch('tools.weather._timestamp', MagicMock(return_value=123456))
    def test_retrieve_from_cache(self):
        key = ("city", "country")
        item = {"fake": "item"}

        # Same time
        with patch.dict(tools.weather._cache, {key: (123456, item)}, clear=True):
            assert tools.weather._cache == {key: (123456, item)}
            self.assertEqual(tools.weather._retrieve_from_cache(key), item)
            assert tools.weather._timestamp.called
        assert tools.weather._cache == {}

        # Exactly 2 minutes
        with patch.dict(tools.weather._cache, {key: (123456 - 120, item)}, clear=True):
            assert tools.weather._cache == {key: (123456 - 120, item)}
            self.assertEqual(tools.weather._retrieve_from_cache(key), item)
            assert tools.weather._timestamp.called
        assert tools.weather._cache == {}

        # Exactly 2 minutes and 1 second
        with patch.dict(tools.weather._cache, {key: (123456 - 121, item)}, clear=True):
            assert tools.weather._cache == {key: (123456 - 121, item)}
            self.assertEqual(tools.weather._retrieve_from_cache(key), None)
            assert tools.weather._timestamp.called
        assert tools.weather._cache == {}

        # Very old cache
        with patch.dict(tools.weather._cache, {key: (1, item)}, clear=True):
            assert tools.weather._cache == {key: (1, item)}
            self.assertEqual(tools.weather._retrieve_from_cache(key), None)
            assert tools.weather._timestamp.called
        assert tools.weather._cache == {}

        # Future cache (should not happen, hence it should return None)
        with patch.dict(tools.weather._cache, {key: (float('inf'), item)}, clear=True):
            assert tools.weather._cache == {key: (float('inf'), item)}
            self.assertEqual(tools.weather._retrieve_from_cache(key), None)
            assert tools.weather._timestamp.called
        assert tools.weather._cache == {}
