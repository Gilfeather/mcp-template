# Company API MCP Server Template

A template for creating Model Context Protocol (MCP) servers that integrate with your company's API using FastMCP.

## Overview

This template provides a starting point for building MCP servers that can interact with your company's REST API. It includes:

- Authentication handling (Bearer token)
- Comprehensive error handling and logging
- In-memory caching for improved performance
- Rate limiting to prevent API abuse
- Full CRUD operations (Create, Read, Update, Delete)
- Health check and status monitoring
- Docker support for easy deployment
- Comprehensive test suite
- CI/CD pipeline with GitHub Actions
- Example tools for common API operations
- Environment variable configuration
- Proper async/await patterns

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   # Production dependencies
   pip install -e .
   
   # Or with development dependencies
   make install-dev
   ```

3. Set environment variables:
   ```bash
   export API_BASE_URL="https://your-api.example.com"
   export API_KEY="your-api-key-here"
   export CACHE_TTL="300"  # Optional: cache TTL in seconds
   export RATE_LIMIT_REQUESTS="100"  # Optional: rate limit
   ```

### Docker Setup

Alternatively, use Docker:

```bash
# Build and run with docker-compose
docker-compose up --build

# Or build and run manually
docker build -t company-api-mcp .
docker run -e API_BASE_URL="https://your-api.example.com" \
           -e API_KEY="your-api-key" \
           company-api-mcp
```

## Configuration

The server can be configured using environment variables:

- `API_BASE_URL`: Base URL of your company's API
- `API_KEY`: API key for authentication
- `CACHE_TTL`: Cache time-to-live in seconds (default: 300)
- `RATE_LIMIT_REQUESTS`: Maximum requests per minute (default: 100)

## Usage

### Running the server

```bash
python server.py
```

### Available Tools

The template includes six example tools:

1. **get_user_info(user_id)**: Retrieve user information by ID
2. **search_items(query, limit)**: Search for items with optional limit
3. **create_item(title, description)**: Create a new item
4. **update_item(item_id, title, description)**: Update an existing item
5. **delete_item(item_id)**: Delete an item
6. **get_api_status()**: Check API health and status

### Customization

To adapt this template for your API:

1. Update the `API_BASE_URL` and authentication method in `server.py`
2. Modify the existing tools or add new ones based on your API endpoints
3. Update the response formatting to match your API's data structure
4. Add any additional error handling specific to your API

## Example Tools Implementation

### Basic Tool Template
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

### CRUD Operations Examples

```python
# Create
@mcp.tool()
async def create_resource(name: str, data: str) -> str:
    json_data = {"name": name, "data": data}
    result = await make_api_request("resources", method="POST", json_data=json_data)
    return format_response(result)

# Read
@mcp.tool()
async def get_resource(resource_id: str) -> str:
    result = await make_api_request(f"resources/{resource_id}")
    return format_response(result)

# Update
@mcp.tool()
async def update_resource(resource_id: str, name: str = None) -> str:
    json_data = {}
    if name:
        json_data["name"] = name
    result = await make_api_request(f"resources/{resource_id}", method="PUT", json_data=json_data)
    return format_response(result)

# Delete
@mcp.tool()
async def delete_resource(resource_id: str) -> str:
    result = await make_api_request(f"resources/{resource_id}", method="DELETE")
    return format_response(result)
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

## Features

### Caching
The server includes an in-memory cache to improve performance and reduce API calls. Cache entries expire after the configured TTL (default: 5 minutes).

### Rate Limiting
Built-in rate limiting prevents API abuse by limiting the number of requests per minute (default: 100 requests/minute).

### Logging
Comprehensive logging for debugging and monitoring:
- Request/response logging
- Cache hit/miss logging
- Error logging with details
- Rate limit warnings

### Error Handling
Comprehensive error handling for:
- HTTP status errors
- Network timeouts
- JSON parsing errors
- API authentication failures
- Rate limit exceeded

### Flexible HTTP Methods
Support for all common HTTP methods:
- GET: Retrieve data (with caching)
- POST: Create new resources
- PUT: Update existing resources
- DELETE: Remove resources

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

### Testing

Run the test suite:

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_server.py -v
```

### Code Quality

Using ruff for linting and formatting:

```bash
# Install development dependencies
make install-dev

# Run all checks
make check

# Fix linting issues automatically
make fix

# Run individual tools
make lint      # Check for issues
make format    # Format code
make test      # Run tests
make test-cov  # Run tests with coverage
```

Or run commands directly:

```bash
# Lint code
ruff check .

# Format code
ruff format .

# Type checking
mypy server.py --ignore-missing-imports
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.