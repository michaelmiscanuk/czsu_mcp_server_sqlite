"""
CZSU MCP SQLite Server - LangChain-Compatible FastMCP Server for SQLite Queries

This is a standalone FastMCP server that exposes SQLite query capabilities
for the CZSU statistical database using SQLite Cloud. It's designed to be
compatible with langchain-mcp-adapters library.

CHANGES FOR LANGCHAIN COMPATIBILITY:
- Uses "streamable-http" transport (recommended by langchain-mcp-adapters)
- Maintains backward compatibility with SSE transport
- Optimized for MultiServerMCPClient integration

NO IMPORTS FROM PARENT PROJECT - This is completely standalone!

Features:
- Single tool: sqlite_query for executing SQL queries
- Read-only access to SQLite Cloud database
- FastMCP-based MCP server with streamable-http transport
- Environment-based configuration
- Error handling and logging
- LangChain-MCP-Adapters compatibility

Usage:
    python main.py

Environment Variables:
    PORT - Server port (default: 8100)
    SQLITE_CLOUD_CONNECTION_STRING - SQLite Cloud connection string (required)
    DEBUG - Enable debug logging (default: 0)
    TRANSPORT - Transport type: "streamable-http" (default) or "sse" for legacy
"""

import os
import asyncio
import json
import urllib.parse

from dotenv import load_dotenv
from fastmcp import FastMCP, Context
from starlette.responses import JSONResponse

# Load environment variables
load_dotenv()

# Configuration
PORT = int(os.getenv("PORT", "8100"))
DATABASE_TYPE = os.getenv("DATABASE_TYPE", "turso").lower()
SQLITE_CLOUD_CONNECTION_STRING = os.getenv("SQLITE_CLOUD_CONNECTION_STRING", "")
TURSO_CONNECTION_STRING = os.getenv("TURSO_CONNECTION_STRING", "")
DEBUG = int(os.getenv("DEBUG", "0"))
TRANSPORT = os.getenv(
    "TRANSPORT", "streamable-http"
)  # Default to streamable-http for langchain compatibility

# Create FastMCP server with enhanced configuration for LangChain compatibility
mcp = FastMCP(
    name="CZSU-SQLite-Server",
    instructions="""
        This server provides access to the CZSU (Czech Statistical Office) SQLite database.
        Use the sqlite_query tool to execute SQL queries against the database.
        The database contains Czech statistical data organized in various tables.
        
        This server is optimized for LangChain MCP Adapters compatibility using streamable-http transport.
    """,
)


def get_sqlitecloud_connection():
    """Get a connection to the SQLite Cloud database."""
    if not SQLITE_CLOUD_CONNECTION_STRING:
        raise ValueError(
            "SQLITE_CLOUD_CONNECTION_STRING environment variable is required for SQLite Cloud"
        )

    try:
        import sqlitecloud

        connection = sqlitecloud.connect(SQLITE_CLOUD_CONNECTION_STRING)
        return connection
    except ImportError:
        raise ImportError(
            "sqlitecloud package is required for SQLite Cloud connections. Install with: pip install sqlitecloud"
        )
    except Exception as e:
        raise ConnectionError(f"Failed to connect to SQLite Cloud: {e}") from e


def get_turso_connection():
    """Get a connection to the Turso database."""
    if not TURSO_CONNECTION_STRING:
        raise ValueError(
            "TURSO_CONNECTION_STRING environment variable is required for Turso"
        )

    try:
        import libsql

        # Parse the connection string to extract URL and auth token
        parsed = urllib.parse.urlparse(TURSO_CONNECTION_STRING)
        query_params = urllib.parse.parse_qs(parsed.query)
        auth_token = query_params.get("authToken", [None])[0]

        # Reconstruct URL without query parameters
        url = urllib.parse.urlunparse(parsed._replace(query=""))

        connection = libsql.connect(
            url, auth_token=auth_token
        )  # pylint: disable=no-member
        return connection
    except ImportError:
        raise ImportError(
            "libsql package is required for Turso connections. Install with: pip install libsql"
        )
    except Exception as e:
        raise ConnectionError(f"Failed to connect to Turso: {e}") from e


def get_db_connection():
    """Get a connection to the configured database."""
    if DATABASE_TYPE == "sqlitecloud":
        return get_sqlitecloud_connection()
    elif DATABASE_TYPE == "turso":
        return get_turso_connection()
    else:
        raise ValueError(
            f"Unsupported DATABASE_TYPE: {DATABASE_TYPE}. Supported types: sqlitecloud, turso"
        )


@mcp.tool()
async def sqlite_query(query: str, ctx: Context) -> str:
    """
    Execute a SQL query against the CZSU SQLite database.

    This tool allows you to run SELECT queries and retrieve data from the
    Czech Statistical Office database. The database contains various tables
    with statistical data.

    Args:
        query: SQL query string to execute (SELECT statements only)

    Returns:
        String representation of query results. Returns "No results found"
        if the query returns an empty result set.

    Examples:
        - sqlite_query("SELECT name FROM sqlite_master WHERE type='table' LIMIT 5")
        - sqlite_query("SELECT * FROM your_table LIMIT 10")

    Note:
        Only read operations are supported. Write operations will fail.
    """
    await ctx.info(f"Executing SQL query: {query}")

    # Define sync query execution
    def _execute_query(q):
        db_connection = get_db_connection()
        try:
            if DATABASE_TYPE == "turso":
                # For libsql, execute returns a cursor
                cursor = db_connection.execute(q)
                result = cursor.fetchall()
            else:
                # For sqlitecloud
                with db_connection:
                    cursor = db_connection.cursor()
                    cursor.execute(q)
                    result = cursor.fetchall()
        finally:
            if DATABASE_TYPE != "turso":
                db_connection.close()
        return result

    # Execute query in thread
    result = await asyncio.to_thread(_execute_query, query)

    # Format result for LangChain compatibility
    if not result:
        result_value = "No results found"
    elif len(result) == 1 and len(result[0]) == 1:
        # Single value result
        result_value = str(result[0][0])
    else:
        # Multi-row/multi-column result - format as JSON for better LangChain parsing
        result_value = json.dumps(result, ensure_ascii=False)

    await ctx.info(f"Query completed, result summary: {len(result)} rows returned")
    await ctx.info(f"Query result: {result_value}")

    return result_value


@mcp.custom_route("/health", methods=["GET"])
async def health_check(_request):
    """Health check endpoint for monitoring."""
    try:
        health_connection = get_db_connection()
        # Try a simple query to verify database is accessible
        if DATABASE_TYPE == "turso":
            cursor = health_connection.execute("SELECT 1")
            cursor.fetchone()
        else:
            with health_connection:
                cursor = health_connection.cursor()
                cursor.execute("SELECT 1")
                cursor.fetchone()

        return JSONResponse(
            {
                "status": "healthy",
                "database": "connected",
                "database_type": "SQLite Cloud",
                "transport": TRANSPORT,
                "langchain_compatible": True,
            }
        )
    except (ValueError, ConnectionError, ImportError) as e:
        return JSONResponse(
            {
                "status": "unhealthy",
                "database": "disconnected",
                "error": str(e),
                "transport": TRANSPORT,
                "langchain_compatible": True,
            },
            status_code=503,
        )


@mcp.custom_route("/mcp-info", methods=["GET"])
async def mcp_info(_request):
    """MCP server information endpoint for debugging."""
    return JSONResponse(
        {
            "server_name": "CZSU-SQLite-Server",
            "transport": TRANSPORT,
            "langchain_compatible": True,
            "tools": ["sqlite_query"],
            "version": "2.0",
            "description": "CZSU Statistical Database MCP Server with LangChain compatibility",
        }
    )


if __name__ == "__main__":
    # This block is for local testing only
    # FastMCP Cloud will ignore this and use the mcp object directly

    # Print startup information
    print("=" * 60)
    print("🚀 Starting CZSU FastMCP SQLite Server (LangChain Compatible)")
    print("=" * 60)

    try:
        # Test database connection
        test_connection = get_db_connection()
        test_connection.close()
        print(f"✓ {DATABASE_TYPE.title()} connection successful")
        print(f"✓ Server port: {PORT}")
        print(f"✓ Debug mode: {'ON' if DEBUG else 'OFF'}")
        print(f"✓ Transport: {TRANSPORT}")
        print("✓ LangChain MCP Adapters: COMPATIBLE")
        print()

        if TRANSPORT == "streamable-http":
            print(
                "🔗 Optimized for langchain-mcp-adapters with streamable-http transport"
            )
            print("   This is the recommended transport for LangChain integration")
        else:
            print(
                "⚠️  Using legacy SSE transport - consider switching to streamable-http"
            )

        print()
        print("Note: When deployed to FastMCP Cloud, this startup")
        print("      block is ignored and the 'mcp' object is used directly.")
        print()

        # Configuration for LangChain MCP Adapters
        print("📋 LangChain MCP Adapters Configuration:")
        print("   Client config:")
        print("   {")
        print(f'     "your-server-name": {{')
        print(f'       "transport": "{TRANSPORT}",')
        print(f'       "url": "http://localhost:{PORT}"')
        print("     }")
        print("   }")

    except (ValueError, ConnectionError, sqlitecloud.Error) as e:
        print(f"✗ ERROR: {e}")
        print("✗ Server will not function correctly without database connection!")

    print("=" * 60)

    # Run the FastMCP server with the configured transport
    mcp.run(transport=TRANSPORT, host="0.0.0.0", port=PORT)
