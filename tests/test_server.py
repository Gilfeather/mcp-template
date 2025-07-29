from unittest.mock import patch

import pytest

from server import (
    _cache,
    get_cache_key,
    get_from_cache,
    set_cache,
)


class TestCacheFunctions:
    def setup_method(self):
        """Clear cache before each test."""
        _cache.clear()

    def test_get_cache_key(self):
        """Test cache key generation."""
        key1 = get_cache_key("users/123")
        key2 = get_cache_key("users/123", {"limit": 10})
        key3 = get_cache_key("users/123", {"limit": 10, "sort": "name"})

        assert key1 == "users/123:"
        assert key2 == "users/123:[('limit', 10)]"
        assert key3 == "users/123:[('limit', 10), ('sort', 'name')]"

    def test_cache_operations(self):
        """Test cache set and get operations."""
        cache_key = "test_key"
        test_data = {"id": 1, "name": "test"}

        # Initially empty
        assert get_from_cache(cache_key) is None

        # Set and get
        set_cache(cache_key, test_data)
        cached_data = get_from_cache(cache_key)

        assert cached_data == test_data

    def test_cache_expiry(self):
        """Test cache expiry functionality."""
        cache_key = "test_key"
        test_data = {"id": 1, "name": "test"}

        # Mock time to test expiry
        with patch("time.time") as mock_time:
            # Set initial time
            mock_time.return_value = 1000
            set_cache(cache_key, test_data)

            # Data should be available
            assert get_from_cache(cache_key) == test_data

            # Move time forward beyond TTL
            mock_time.return_value = 1400  # 400 seconds later (> 300 TTL)

            # Data should be expired
            assert get_from_cache(cache_key) is None


if __name__ == "__main__":
    pytest.main([__file__])
