import os
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("company-api")

# Configuration - Replace with your API details
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.example.com")
API_KEY = os.getenv("API_KEY", "your-api-key-here")
USER_AGENT = "company-mcp-server/1.0"

async def make_api_request(endpoint: str, params: dict = None) -> dict[str, Any] | None:
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
            response = await client.get(url, headers=headers, params=params, timeout=30.0)
            response.raise_for_status()
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

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')