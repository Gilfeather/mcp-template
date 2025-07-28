import pytest
import asyncio
from unittest.mock import AsyncMock, patch
import httpx

from server import (
    make_api_request,
    get_cache_key,
    get_from_cache,
    set_cache,
    _cache
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
        with patch('time.time') as mock_time:
            # Set initial time
            mock_time.return_value = 1000
            set_cache(cache_key, test_data)
            
            # Data should be available
            assert get_from_cache(cache_key) == test_data
            
            # Move time forward beyond TTL
            mock_time.return_value = 1400  # 400 seconds later (> 300 TTL)
            
            # Data should be expired
            assert get_from_cache(cache_key) is None


class TestAPIRequest:
    @pytest.mark.asyncio
    async def test_successful_get_request(self):
        """Test successful GET request."""
        mock_response_data = {"id": 1, "name": "test user"}
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_response_data
            mock_response.raise_for_status.return_value = None
            
            mock_client.return_value.__aenter__.return_value.request = AsyncMock(
                return_value=mock_response
            )
            
            result = await make_api_request("users/1")
            
            assert result == mock_response_data

    @pytest.mark.asyncio
    async def test_successful_post_request(self):
        """Test successful POST request."""
        mock_response_data = {"id": 1, "name": "created user"}
        json_data = {"name": "new user"}
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.status_code = 201
            mock_response.json.return_value = mock_response_data
            mock_response.raise_for_status.return_value = None
            
            mock_client.return_value.__aenter__.return_value.request = AsyncMock(
                return_value=mock_response
            )
            
            result = await make_api_request("users", method="POST", json_data=json_data)
            
            assert result == mock_response_data

    @pytest.mark.asyncio
    async def test_empty_response_handling(self):
        """Test handling of empty responses (204 No Content)."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.status_code = 204
            mock_response.content = b""
            mock_response.raise_for_status.return_value = None
            
            mock_client.return_value.__aenter__.return_value.request = AsyncMock(
                return_value=mock_response
            )
            
            result = await make_api_request("users/1", method="DELETE")
            
            assert result == {"success": True, "message": "Operation completed successfully"}

    @pytest.mark.asyncio
    async def test_http_error_handling(self):
        """Test HTTP error handling."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.status_code = 404
            mock_response.text = "Not Found"
            
            http_error = httpx.HTTPStatusError(
                "404 Not Found", 
                request=AsyncMock(), 
                response=mock_response
            )
            
            mock_client.return_value.__aenter__.return_value.request = AsyncMock(
                side_effect=http_error
            )
            
            result = await make_api_request("users/999")
            
            assert "error" in result
            assert "HTTP 404" in result["error"]

    @pytest.mark.asyncio
    async def test_network_error_handling(self):
        """Test network error handling."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.request = AsyncMock(
                side_effect=httpx.ConnectError("Connection failed")
            )
            
            result = await make_api_request("users/1")
            
            assert "error" in result
            assert "Request failed" in result["error"]


if __name__ == "__main__":
    pytest.main([__file__])