# Company API MCP Server Template

A template for creating Model Context Protocol (MCP) servers that integrate with your company's API using FastMCP.

## Overview

This template provides a starting point for building MCP servers that can interact with your company's REST API. It includes:

- Authentication handling (Bearer token)
- Error handling and logging
- Example tools for common API operations
- Environment variable configuration
- Proper async/await patterns

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -e .
   ```

3. Set environment variables:
   ```bash
   export API_BASE_URL="https://your-api.example.com"
   export API_KEY="your-api-key-here"
   ```

## Configuration

The server can be configured using environment variables:

- `API_BASE_URL`: Base URL of your company's API
- `API_KEY`: API key for authentication

## Usage

### Running the server

```bash
python server.py
```

### Available Tools

The template includes two example tools:

1. **get_user_info(user_id)**: Retrieve user information by ID
2. **search_items(query, limit)**: Search for items with optional limit

### Customization

To adapt this template for your API:

1. Update the `API_BASE_URL` and authentication method in `server.py`
2. Modify the existing tools or add new ones based on your API endpoints
3. Update the response formatting to match your API's data structure
4. Add any additional error handling specific to your API

## Example Tools Implementation

```python
@mcp.tool()
async def your_custom_tool(param: str) -> str:
    """Description of what your tool does.
    
    Args:
        param: Description of the parameter
    """
    data = await make_api_request(f"your-endpoint/{param}")
    
    if not data or "error" in data:
        return "Error message"
    
    # Format and return your data
    return formatted_response
```

## MCP Integration

To use this server with an MCP client, add it to your MCP configuration:

```json
{
  "mcpServers": {
    "company-api": {
      "command": "python",
      "args": ["/path/to/server.py"],
      "env": {
        "API_BASE_URL": "https://your-api.example.com",
        "API_KEY": "your-api-key"
      }
    }
  }
}
```

## Development

### Project Structure

```
.
├── server.py           # Main MCP server implementation
├── main.py            # Simple CLI entry point
├── pyproject.toml     # Project configuration
├── README.md          # This file
└── .gitignore         # Git ignore rules
```

### Adding New Tools

1. Define your tool function with the `@mcp.tool()` decorator
2. Use `make_api_request()` to call your API
3. Handle errors appropriately
4. Format the response for the user

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]