# Package Management Guide# MCP Server - Package Management Guide



This MCP server uses **`pyproject.toml`** for dependency management, compatible with `uv` and `pip`.## Overview



## InstallationThe MCP server now uses **`pyproject.toml`** for dependency management, aligning with the main project and modern Python packaging standards.



### Using uv (Recommended)## Why pyproject.toml?



```bash✅ **Consistency**: Same approach as main project  

cd czsu_mcp_server_sqlite✅ **Modern Standard**: PEP 621 compliant  

✅ **uv Compatible**: Works with faster package manager  

# Install dependencies✅ **Better Metadata**: Project info, authors, version in one place  

uv pip install .✅ **FastMCP Cloud Compatible**: Auto-detected by deployment platform  



# Install with dev dependencies## Installation Methods

uv pip install .[dev]

```### Using uv (Recommended - Fastest)



**Why uv?**```bash

- 10-100x faster than pipcd czsu_mcp_server_sqlite

- Better dependency resolution

- Consistent with main project# Install project dependencies

uv pip install .

### Using pip

# Install with dev dependencies

```bashuv pip install .[dev]

cd czsu_mcp_server_sqlite```



# Install dependencies**Benefits**:

pip install .- 10-100x faster than pip

- Better dependency resolution

# Install with dev dependencies- Consistent with main project setup

pip install .[dev]

```### Using pip (Traditional)



## Dependencies```bash

cd czsu_mcp_server_sqlite

### Production

# Install from pyproject.toml

```tomlpip install .

dependencies = [

    "fastmcp>=2.0.0",      # MCP server framework# Install with dev dependencies

    "python-dotenv>=1.0.0", # Environment variables  pip install .[dev]

    "starlette>=0.45.0",   # Web framework```

]

```### Using requirements.txt (Legacy)



SQLite is built into Python - no extra dependency needed!```bash

cd czsu_mcp_server_sqlite

### Development

# Still works for backward compatibility

```tomlpip install -r requirements.txt

[project.optional-dependencies]```

dev = [

    "pytest>=7.0.0",       # Testing**Note**: We keep `requirements.txt` for backward compatibility, but **`pyproject.toml` is preferred**.

    "httpx>=0.25.0",       # HTTP client

]## Dependencies

```

### Production Dependencies

## Local Development Setup

The MCP server has minimal dependencies:

```bash

# Navigate to MCP server folder```toml

cd czsu_mcp_server_sqlitedependencies = [

    "fastmcp>=2.0.0",      # MCP server framework (includes FastAPI & Uvicorn)

# Install with uv    "python-dotenv>=1.0.0", # Environment variables

uv pip install .    "starlette>=0.45.0",   # Web framework (included with FastMCP)

]

# Run server```

python main.py

```SQLite is built into Python - no extra dependency needed!



## FastMCP Cloud Deployment### Development Dependencies



FastMCP Cloud automatically detects and installs dependencies from `pyproject.toml`.```toml

[project.optional-dependencies]

No configuration needed!dev = [

    "pytest>=7.0.0",       # Testing framework

## Updating Dependencies    "httpx>=0.25.0",       # HTTP client for testing

]

### Add a New Dependency```



1. Edit `pyproject.toml`:## Local Development Setup

   ```toml

   dependencies = [### Full Setup with uv

       "fastmcp>=2.0.0",

       "python-dotenv>=1.0.0",```bash

       "starlette>=0.45.0",# 1. Navigate to MCP server folder

       "your-new-package>=1.0.0",  # Add herecd czsu_mcp_server_sqlite

   ]

   ```# 2. Create virtual environment (optional but recommended)

python -m venv .venv

2. Reinstall:

   ```bash# 3. Activate virtual environment

   uv pip install .# Windows:

   ```.venv\Scripts\activate

# Unix/Linux/macOS:

## Troubleshootingsource .venv/bin/activate



### "No module named 'fastmcp'"# 4. Install with uv

uv pip install .

```bash

cd czsu_mcp_server_sqlite# 5. Run server

uv pip install .python main.py

``````



### Changes not taking effect### Quick Start (No venv)



```bash```bash

uv pip install . --force-reinstallcd czsu_mcp_server_sqlite

```uv pip install .

python main.py

### Want to use pip instead of uv```



```bash## FastMCP Cloud Deployment

pip install .

```FastMCP Cloud automatically detects dependencies:



## Quick Reference1. **Looks for `pyproject.toml` first** ✅ (preferred)

2. Falls back to `requirements.txt` if no pyproject.toml

```bash

# Install**No changes needed** - both files are included in the repository!

uv pip install .                    # Recommended

pip install .                       # Also works## Updating Dependencies



# Install with dev tools### Add a New Dependency

uv pip install .[dev]

1. Edit `pyproject.toml`:

# Run server   ```toml

python main.py   dependencies = [

       "fastmcp>=2.0.0",

# Update dependencies       "python-dotenv>=1.0.0",

uv pip install . --upgrade       "starlette>=0.45.0",

```       "your-new-package>=1.0.0",  # Add here

   ]
   ```

2. Reinstall:
   ```bash
   uv pip install .
   ```

3. Also update `requirements.txt` for backward compatibility:
   ```txt
   your-new-package>=1.0.0
   ```

### Sync requirements.txt with pyproject.toml

If you update `pyproject.toml`, you can regenerate `requirements.txt`:

```bash
# Install pip-tools
pip install pip-tools

# Generate requirements.txt from pyproject.toml
pip-compile pyproject.toml -o requirements.txt
```

Or manually keep them in sync (recommended for this small project).

## Comparison: Main Project vs MCP Server

### Main Project Dependencies (70+)
- FastAPI, Uvicorn
- LangChain ecosystem
- PostgreSQL + SQLAlchemy
- OpenAI, Anthropic
- ChromaDB, Cohere
- Data processing (pandas, numpy)
- PDF parsing (llama-parse)
- Authentication (JWT, OAuth)
- And many more...

### MCP Server Dependencies (3!)
- fastmcp
- python-dotenv
- starlette

**Result**: MCP server is lightweight and focused! 🎯

## Troubleshooting

### "No module named 'fastmcp'"

**Solution**:
```bash
cd czsu_mcp_server_sqlite
uv pip install .
```

### "pyproject.toml not found"

**Solution**: Make sure you're in the `czsu_mcp_server_sqlite` folder:
```bash
cd czsu_mcp_server_sqlite
ls pyproject.toml  # Should exist
```

### Changes not taking effect

**Solution**: Reinstall after editing pyproject.toml:
```bash
uv pip install . --force-reinstall
```

### Want to use pip instead of uv

**Solution**: Just use `pip install .` instead of `uv pip install .`

## Validation

To verify your `pyproject.toml` is valid:

```bash
cd czsu_mcp_server_sqlite
python validate_pyproject.py
```

Should output:
```
✓ pyproject.toml is valid!
Project: czsu-mcp-server-sqlite
Version: 1.0.0
Python: >=3.10
Dependencies: 3
```

## Summary

| Feature | pyproject.toml | requirements.txt |
|---------|----------------|------------------|
| **Status** | ✅ Recommended | ⚠️ Legacy |
| **uv Compatible** | ✅ Yes | ⚠️ Partial |
| **FastMCP Cloud** | ✅ Auto-detected | ✅ Auto-detected |
| **Metadata** | ✅ Rich | ❌ None |
| **Modern Standard** | ✅ PEP 621 | ❌ Old format |
| **Main Project** | ✅ Same approach | ❌ Different |

**Recommendation**: Use `pyproject.toml` with `uv pip install .` for best experience!

## Quick Commands Reference

```bash
# Install dependencies
uv pip install .                    # Recommended
pip install .                       # Traditional
pip install -r requirements.txt     # Legacy

# Install with dev tools
uv pip install .[dev]

# Run MCP server
python main.py

# Validate pyproject.toml
python validate_pyproject.py

# Update all dependencies
uv pip install . --upgrade
```

---

**Need Help?**
- Main project uses the same approach - check `pyproject.toml` in root
- See `README.md` for full MCP server documentation
- See `FASTMCP_CLOUD_DEPLOYMENT_GUIDE.md` for deployment
