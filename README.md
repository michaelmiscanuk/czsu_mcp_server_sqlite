# CZSU MCP SQLite Cloud Server

Standalone FastMCP server providing SQLite query capabilities for CZSU (Czech Statistical Office) data using SQLite Cloud.

This is a standalone FastMCP server that provides SQLite query capabilities for the CZSU Multi-Agent Text-to-SQL project using **SQLite Cloud** for database hosting.



## Features

- **FastMCP 2.0** framework with native MCP protocol
- Single tool: `sqlite_query` for executing SQL queries
- **SQLite Cloud** database hosting (no local files needed)
- HTTP transport for remote access
- Health check endpoint

- FastMCP Cloud ready (zero configuration)- Uses `@mcp.tool()` decorator for tool definition

- HTTP transport for remote access

## Quick Start- Automatic OpenAPI documentation

- Built-in health check endpoint

### Local Development- **FastMCP Cloud ready** - no special configuration files needed!



```bash## Structure

# 1. Install dependencies

cd czsu_mcp_server_sqlite```

uv pip install .czsu_mcp_server_sqlite/

├── main.py              # FastMCP server implementation (entrypoint: main.py:mcp)

# 2. Copy database (if needed)├── pyproject.toml       # Python dependencies (preferred, auto-detected by FastMCP Cloud)

copy ..\data\czsu_data.db .\data\├── requirements.txt     # Python dependencies (legacy, for backward compatibility)

├── .env.example        # Environment variable template

# 3. Run server├── README.md           # This file

python main.py└── data/

```    └── czsu_data.db    # SQLite database

```

Server starts on `http://localhost:8100`

## Setup for Local Development

1. **Install dependencies:**
   ```bash
   # Using uv (recommended - faster and better dependency resolution)
   uv pip install .
   
   # Or using pip
   pip install .
   ```

2. **Configure environment:**
   ```bash
   # Copy and edit .env file
   copy .env.example .env
   # Edit .env with your SQLite Cloud connection string
   ```

3. **Run server:**
   ```bash
   python main.py
   ```

Server starts on `http://localhost:8100`

   

### FastMCP Cloud (Recommended)   **Note**: See `PACKAGE_MANAGEMENT.md` for detailed guide on dependency management.



1. Visit https://fastmcp.cloud3. **Configure environment (optional):**

2. Sign in with GitHub   ```bash

3. Create project:   # Copy and edit .env file if needed

   - **Entrypoint**: `main.py:mcp`   copy .env.example .env

   - **Repository**: Your GitHub repo   ```

4. Deploy!

4. **Run locally:**

Your server will be at: `https://your-project-name.fastmcp.app/mcp`   ```bash

   python main.py

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for details.   ```



## Structure   The server will start on `http://localhost:8100`



```## Deployment to FastMCP Cloud

czsu_mcp_server_sqlite/

├── main.py              # FastMCP server (entrypoint: main.py:mcp)FastMCP Cloud is the **official managed platform** for hosting MCP servers. It's free during beta!

├── pyproject.toml       # Dependencies

├── .env.example         # Environment template### Prerequisites

├── README.md            # This file

├── docs/                # Documentation- GitHub account

│   ├── DEPLOYMENT.md- This folder in a GitHub repository (public or private)

│   └── PACKAGE_MANAGEMENT.md- Database file included in the repo

└── data/

    └── czsu_data.db     # SQLite database### Deployment Steps

```

1. **Visit FastMCP Cloud**: Go to https://fastmcp.cloud

## Configuration

2. **Sign in with GitHub**: Authenticate your GitHub account

Environment variables (optional):

3. **Create a Project**:

```env   - Name: Choose a name (e.g., "czsu-mcp-sqlite")

PORT=8100                          # Server port   - Repository: Select your GitHub repo

DB_PATH=./data/czsu_data.db       # Database path   - **Entrypoint**: `main.py:mcp` (this is the FastMCP server object)

DEBUG=0                            # Debug mode   - Authentication: Enable or disable (your choice)

```

4. **Deploy**: FastMCP Cloud will automatically:

## Dependencies

- `fastmcp>=2.0.0` - MCP server framework
- `python-dotenv>=1.0.0` - Environment variables
- `starlette>=0.45.0` - Web framework
- `sqlitecloud>=1.0.0` - SQLite Cloud connectivity

   ```

## Documentation   https://your-project-name.fastmcp.app/mcp

   ```

- **Deployment Guide**: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

- **Package Management**: [docs/PACKAGE_MANAGEMENT.md](docs/PACKAGE_MANAGEMENT.md)6. **Update Main Project**: In your main project's `.env`:

   ```env

## Integration   MCP_SERVER_URL=https://your-project-name.fastmcp.app/mcp

   USE_LOCAL_SQLITE_FALLBACK=1

This server is designed to work with the main CZSU Multi-Agent Text-to-SQL project.   ```



Configure main project's `.env`:### Auto-Deployment



```envFastMCP Cloud automatically redeploys your server whenever you:

MCP_SERVER_URL=https://your-project-name.fastmcp.app/mcp- Push changes to the `main` branch

USE_LOCAL_SQLITE_FALLBACK=1- Open a pull request (deploys preview version)

```

No CI/CD configuration needed!

## Standalone Design

## API Endpoints

This folder has **no dependencies** on the parent project. All imports are self-contained, making it easy to deploy separately.

The FastMCP server exposes:

## License

- **MCP Protocol Endpoint** - `/mcp/v1/*` (automatically created by FastMCP)

Part of the CZSU Multi-Agent Text-to-SQL project.  - Handles all MCP protocol operations

  - Tool: `sqlite_query` - Execute SQLite query
  
- **Health Check** - `GET /health` (custom route)
  - Returns server and database status
  - Useful for monitoring and uptime checks

## FastMCP Features

- **Type-safe tool definitions** with Python decorators
- **Automatic schema generation** from function signatures
- **Built-in error handling** and validation
- **HTTP transport** for web-based deployments
- **Custom routes** for additional endpoints (like health checks)

## Security Notes

- This server is designed for internal use only
- Consider adding authentication if exposing publicly
- The database is read-only (tool prevents modifications)

## Environment Variables

- `PORT` - Server port (default: 8100)
- `SQLITE_CLOUD_CONNECTION_STRING` - SQLite Cloud connection string (required)
- `DEBUG` - Enable debug logging (default: 0)

## Testing

### Local Testing

1. **Start the server locally:**
   ```bash
   python main.py
   ```

2. **Test health endpoint:**
   ```bash
   curl http://localhost:8100/health
   ```

3. **Test with FastMCP Client** (from main project):
   ```python
   from fastmcp import Client
   
   async def test_query():
       async with Client("http://localhost:8100/mcp") as client:
           result = await client.call_tool("sqlite_query", {
               "query": "SELECT * FROM SELECTION LIMIT 5"
           })
           print(result)
   
   import asyncio
   asyncio.run(test_query())
   ```

### Testing on FastMCP Cloud

Once deployed, use the same client code with your cloud URL:
```python
async with Client("https://your-project-name.fastmcp.app/mcp") as client:
    # ... same as above
```

## Troubleshooting

### Local Development Issues

**Server won't start:**
- Check Python version (needs 3.10+)
- Verify all dependencies installed: `pip install -r requirements.txt`
- Check if port 8100 is available
- Verify SQLite Cloud connection string is set in `.env`

**Database errors:**
- Check SQLite Cloud connection string format
- Verify API key is valid
- Check network connectivity to SQLite Cloud
- Ensure database exists in your SQLite Cloud account

### FastMCP Cloud Deployment Issues

**Build fails:**
- Check FastMCP Cloud logs for error messages
- Verify `requirements.txt` has all dependencies with correct versions
- Ensure `main.py` exports `mcp` object at module level
- Check entrypoint is exactly: `main.py:mcp`

**Server starts but tool doesn't work:**
- Check SQLite Cloud connection string is properly configured
- Verify database exists in your SQLite Cloud account
- Check FastMCP Cloud logs for runtime errors

**Connection timeouts:**
- FastMCP Cloud might be cold-starting (first request takes longer)
- Check your internet connection
- Verify the URL format: `https://your-project-name.fastmcp.app/mcp`

**Cannot find tool:**
- Ensure the `@mcp.tool()` decorator is applied correctly
- Check that the function is async (`async def`)
- Verify FastMCP version is 2.0 or higher

### Getting Help

- **FastMCP Docs**: https://fastmcp.com/docs
- **FastMCP Cloud Support**: Contact via https://fastmcp.cloud
- **MCP Protocol Spec**: https://spec.modelcontextprotocol.io/

## Separation from Main Project

This folder is designed to be **moved out** of the main project and maintained as a separate Git repository. It has no dependencies on the main project's code - all imports are self-contained.
