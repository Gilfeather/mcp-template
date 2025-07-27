import os
import time
from typing import Any, Optional
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("company-api")

# Configuration - Replace with your API details
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.example.com")
API_KEY = os.getenv("API_KEY", "your-api-key-here")
USER_AGENT = "company-mcp-server/1.0"
CACHE_TTL = int(os.getenv("CACHE_TTL", "300"))  # 5 minutes default

# Simple in-memory cache
_cache = {}

def get_cache_key(endpoint: str, params: dict = None) -> str:
    """Generate a cache key for the request."""
    params_str = str(sorted(params.items())) if params else ""
    return f"{endpoint}:{params_str}"

def get_from_cache(cache_key: str) -> Optional[dict]:
    """Get data from cache if not expired."""
    if cache_key in _cache:
        data, timestamp = _cache[cache_key]
        if time.time() - timestamp < CACHE_TTL:
            return data
        else:
            del _cache[cache_key]
    return None

def set_cache(cache_key: str, data: dict) -> None:
    """Store data in cache with timestamp."""
    _cache[cache_key] = (data, time.time())

async def make_api_request(
    endpoint: str, 
    method: str = "GET", 
    params: dict = None, 
    json_data: dict = None
) -> dict[str, Any] | None:
    """Make a request to your company API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    url = f"{API_BASE_URL}/{endpoint.lstrip('/')}"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=json_data,
                timeout=30.0
            )
            response.raise_for_status()
            
            # Handle empty responses
            if response.status_code == 204 or not response.content:
                return {"success": True, "message": "Operation completed successfully"}
            
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP {e.response.status_code}: {e.response.text}"}
        except Exception as e:
            return {"error": f"Request failed: {str(e)}"}

@mcp.tool()
async def get_user_info(user_id: str) -> str:
    """Get user information from the API.

    Args:
        user_id: The unique identifier for the user
    """
    data = await make_api_request(f"users/{user_id}")
    
    if not data:
        return "Unable to fetch user information."
    
    if "error" in data:
        return f"Error: {data['error']}"
    
    # Format the response - adjust based on your API response structure
    return f"""
User ID: {data.get('id', 'Unknown')}
Name: {data.get('name', 'Unknown')}
Email: {data.get('email', 'Unknown')}
Status: {data.get('status', 'Unknown')}
Created: {data.get('created_at', 'Unknown')}
"""

@mcp.tool()
async def search_items(query: str, limit: int = 10) -> str:
    """Search for items using the API.

    Args:
        query: Search query string
        limit: Maximum number of results to return (default: 10)
    """
    params = {
        "q": query,
        "limit": limit
    }
    
    data = await make_api_request("search", params)
    
    if not data:
        return "Unable to perform search."
    
    if "error" in data:
        return f"Error: {data['error']}"
    
    # Format the search results - adjust based on your API response structure
    items = data.get('items', [])
    if not items:
        return "No items found for the given query."
    
    results = []
    for item in items:
        result = f"""
ID: {item.get('id', 'Unknown')}
Title: {item.get('title', 'Unknown')}
Description: {item.get('description', 'No description')}
"""
        results.append(result)
    
    return "\n---\n".join(results)

@mcp.tool()
async def create_item(title: str, description: str = "") -> str:
    """Create a new item via the API.

    Args:
        title: Title of the item to create
        description: Optional description of the item
    """
    json_data = {
        "title": title,
        "description": description
    }
    
    data = await make_api_request("items", method="POST", json_data=json_data)
    
    if not data:
        return "Unable to create item."
    
    if "error" in data:
        return f"Error: {data['error']}"
    
    return f"""
Item created successfully!
ID: {data.get('id', 'Unknown')}
Title: {data.get('title', title)}
Description: {data.get('description', description)}
Created: {data.get('created_at', 'Unknown')}
"""

@mcp.tool()
async def update_item(item_id: str, title: str = None, description: str = None) -> str:
    """Update an existing item via the API.

    Args:
        item_id: ID of the item to update
        title: New title (optional)
        description: New description (optional)
    """
    json_data = {}
    if title:
        json_data["title"] = title
    if description:
        json_data["description"] = description
    
    if not json_data:
        return "No updates provided. Please specify title or description."
    
    data = await make_api_request(f"items/{item_id}", method="PUT", json_data=json_data)
    
    if not data:
        return "Unable to update item."
    
    if "error" in data:
        return f"Error: {data['error']}"
    
    return f"""
Item updated successfully!
ID: {data.get('id', item_id)}
Title: {data.get('title', 'Unknown')}
Description: {data.get('description', 'Unknown')}
Updated: {data.get('updated_at', 'Unknown')}
"""

@mcp.tool()
async def delete_item(item_id: str) -> str:
    """Delete an item via the API.

    Args:
        item_id: ID of the item to delete
    """
    data = await make_api_request(f"items/{item_id}", method="DELETE")
    
    if not data:
        return "Unable to delete item."
    
    if "error" in data:
        return f"Error: {data['error']}"
    
    return f"Item {item_id} deleted successfully."

@mcp.tool()
async def get_api_status() -> str:
    """Check the API status and health."""
    # Try a simple health check endpoint
    data = await make_api_request("health")
    
    if not data:
        return "API appears to be down or unreachable."
    
    if "error" in data:
        return f"API Status: Error - {data['error']}"
    
    status = data.get('status', 'unknown')
    version = data.get('version', 'unknown')
    uptime = data.get('uptime', 'unknown')
    
    return f"""
API Status: {status}
Version: {version}
Uptime: {uptime}
Cache entries: {len(_cache)}
"""

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')