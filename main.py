"""
CZSU MCP SQLite Server - Standalone FastMCP Server for SQLite Queries

This is a standalone FastMCP server that exposes SQLite query capabilities
for the CZSU statistical database. It's designed to be deployed separately
from the main application (e.g., on Railway.com) and accessed via HTTP.

NO IMPORTS FROM PARENT PROJECT - This is completely standalone!

Features:
- Single tool: sqlite_query for executing SQL queries
- Read-only access to SQLite database
- FastMCP-based MCP server with HTTP transport
- Environment-based configuration
- Error handling and logging

Usage:
    python main.py

Environment Variables:
    PORT - Server port (default: 8100)
    DB_PATH - Path to SQLite database (default: ./data/czsu_data.db)
    DEBUG - Enable debug logging (default: 0)
"""

import os
import sqlite3
from pathlib import Path

from dotenv import load_dotenv
from fastmcp import FastMCP
from starlette.responses import JSONResponse

# Load environment variables
load_dotenv()

# Configuration
PORT = int(os.getenv("PORT", "8100"))
DB_PATH = os.getenv("DB_PATH", "./data/czsu_data.db")
DEBUG = int(os.getenv("DEBUG", "0"))

# Create FastMCP server
mcp = FastMCP(
    name="CZSU-SQLite-Server",
    instructions="""
        This server provides access to the CZSU (Czech Statistical Office) SQLite database.
        Use the sqlite_query tool to execute SQL queries against the database.
        The database contains Czech statistical data organized in various tables.
    """,
)


def get_db_path() -> Path:
    """Get the absolute path to the SQLite database."""
    database_path = Path(DB_PATH)

    # If relative path, make it relative to this file's directory
    if not database_path.is_absolute():
        database_path = Path(__file__).parent / database_path

    if not database_path.exists():
        raise FileNotFoundError(f"Database not found at: {database_path}")

    return database_path


@mcp.tool()
def sqlite_query(query: str) -> str:
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
    if DEBUG:
        print(f"[DEBUG] Executing query: {query}")

    # Get database path
    database_path = get_db_path()

    if DEBUG:
        print(f"[DEBUG] Using database: {database_path}")

    # Execute query
    with sqlite3.connect(str(database_path)) as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()

    # Format result
    if not result:
        result_value = "No results found"
    elif len(result) == 1 and len(result[0]) == 1:
        result_value = str(result[0][0])
    else:
        result_value = str(result)

    if DEBUG:
        print(f"[DEBUG] Query result: {result_value}")

    return result_value


@mcp.custom_route("/health", methods=["GET"])
async def health_check(_request):
    """Health check endpoint for monitoring."""
    try:
        database_path = get_db_path()
        # Try a simple query to verify database is accessible
        with sqlite3.connect(str(database_path)) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()

        return JSONResponse(
            {
                "status": "healthy",
                "database": "connected",
                "db_path": str(database_path),
            }
        )
    except (FileNotFoundError, sqlite3.Error) as e:
        return JSONResponse(
            {"status": "unhealthy", "database": "disconnected", "error": str(e)},
            status_code=503,
        )


if __name__ == "__main__":
    # This block is for local testing only
    # FastMCP Cloud will ignore this and use the mcp object directly

    # Print startup information
    print("=" * 60)
    print("🚀 Starting CZSU FastMCP SQLite Server (Local Mode)")
    print("=" * 60)

    try:
        db_path = get_db_path()
        print(f"✓ Database found: {db_path}")
        print(f"✓ Server port: {PORT}")
        print(f"✓ Debug mode: {'ON' if DEBUG else 'OFF'}")
        print("✓ Transport: HTTP")
        print()
        print("Note: When deployed to FastMCP Cloud, this startup")
        print("      block is ignored and the 'mcp' object is used directly.")
    except FileNotFoundError as e:
        print(f"✗ ERROR: {e}")
        print("✗ Server will not function correctly without the database!")

    print("=" * 60)

    # Run the FastMCP server with HTTP transport (local testing only)
    mcp.run(transport="http", host="0.0.0.0", port=PORT)
