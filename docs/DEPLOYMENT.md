# FastMCP Cloud Deployment Guide# FastMCP Cloud Deployment Guide for MCP Server



This guide covers deploying the CZSU MCP SQLite Server to FastMCP Cloud.## Pre-Deployment Checklist



## Prerequisites### ✅ Verify Files in `czsu_mcp_server_sqlite/`



- GitHub account- [ ] `main.py` - FastMCP server implementation with `mcp` object exported

- SQLite database file in `data/czsu_data.db`- [ ] `pyproject.toml` - Dependencies file (recommended)

- `main.py` with `mcp` object exported- [ ] `requirements.txt` - Dependencies file (legacy, for backward compatibility)

- `pyproject.toml` with dependencies- [ ] `data/czsu_data.db` - Database file exists (IMPORTANT!)

- [ ] `.gitignore` - Git ignore rules exist

## Quick Deployment- [ ] `README.md` - Documentation exists



### 1. Push to GitHub**Note:** No `railway.toml` or `start.sh` needed - FastMCP Cloud is zero-config!

**Note:** FastMCP Cloud auto-detects `pyproject.toml` (preferred) or `requirements.txt`

```bash

# Commit your code### ✅ Verify Database

git add czsu_mcp_server_sqlite/

git commit -m "Add MCP server"```bash

git push# Check database file exists and is not empty

```cd czsu_mcp_server_sqlite

dir data\czsu_data.db

### 2. Deploy to FastMCP Cloud

# Should show file size (e.g., several MB)

1. Visit **https://fastmcp.cloud**# If file is 0 bytes, re-copy from parent project:

2. Sign in with GitHubcopy ..\data\czsu_data.db .\data\

3. Create new project:```

   - **Name**: `czsu-mcp-sqlite` (or your choice)

   - **Repository**: Select your GitHub repo### ✅ Test Locally First

   - **Entrypoint**: `main.py:mcp`

   - **Authentication**: Enable if needed```bash

4. Click **Deploy**# Start server

cd czsu_mcp_server_sqlite

FastMCP Cloud will automatically:python main.py

- Detect dependencies from `pyproject.toml`

- Build and deploy your server# In another terminal, test it works

- Assign URL: `https://your-project-name.fastmcp.app/mcp`curl http://localhost:8100/health

- Auto-redeploy on push to `main` branch

# Test with FastMCP Client

### 3. Update Main Applicationpython

>>> from fastmcp import Client

Edit `.env` in your main project:>>> import asyncio

>>> async def test():

```env...     async with Client("http://localhost:8100/mcp") as client:

MCP_SERVER_URL=https://your-project-name.fastmcp.app/mcp...         result = await client.call_tool("sqlite_query", {"query": "SELECT COUNT(*) FROM sqlite_master"})

USE_LOCAL_SQLITE_FALLBACK=1...         print(result)

```>>> asyncio.run(test())

```

## Testing Deployment

All tests should return successful responses.

### Health Check

## Deployment Steps

```bash

curl https://your-project-name.fastmcp.app/health### Step 1: Push to GitHub

```

**Option A: Separate Repository (Recommended)**

Expected response:```bash

```json# Create new directory for MCP server repo

{mkdir czsu-mcp-server

  "status": "healthy",xcopy /E /I czsu_mcp_server_sqlite czsu-mcp-server

  "database": "connected",cd czsu-mcp-server

  "db_path": "/app/data/czsu_data.db"

}# Initialize Git

```git init

git add .

### Test with FastMCP Clientgit commit -m "Initial MCP server for FastMCP Cloud deployment"



```python# Create GitHub repo and push

from fastmcp import Clientgit remote add origin https://github.com/yourusername/czsu-mcp-server.git

import asynciogit branch -M main

git push -u origin main

async def test():```

    async with Client("https://your-project-name.fastmcp.app/mcp") as client:

        result = await client.call_tool("sqlite_query", {**Option B: In Current Repository**

            "query": "SELECT name FROM sqlite_master WHERE type='table' LIMIT 3"```bash

        })# Just ensure czsu_mcp_server_sqlite/ is committed

        print(result)git add czsu_mcp_server_sqlite/

git commit -m "Add MCP server for FastMCP Cloud deployment"

asyncio.run(test())git push

``````



## Local Testing### Step 2: Deploy to FastMCP Cloud



Before deploying, test locally:1. **Visit FastMCP Cloud**: Go to https://fastmcp.cloud



```bash2. **Sign In**: Click "Sign in with GitHub"

# Install dependencies

cd czsu_mcp_server_sqlite3. **Create New Project**:

uv pip install .   - Click "New Project" or "Deploy"

   - **Name**: Choose a project name (e.g., `czsu-mcp-sqlite`)

# Run server   - **Repository**: Select your GitHub repository

python main.py   - **Root Directory** (if option B): Set to `czsu_mcp_server_sqlite`

   - **Entrypoint**: Enter `main.py:mcp` (this is critical!)

# Test in another terminal   - **Authentication**: Enable or disable based on your needs

curl http://localhost:8100/health

```4. **Deploy**:

   - Click "Deploy" or "Create Project"

## Auto-Deployment   - FastMCP Cloud will automatically:

     - Clone your repository

FastMCP Cloud automatically redeploys when you:     - Detect Python and install from `requirements.txt`

- Push to `main` branch     - Find the `mcp` object in `main.py`

- Open a pull request (creates preview deployment)     - Build and deploy your server

     - Assign a URL: `https://your-project-name.fastmcp.app`

## Troubleshooting

5. **Wait for Build**:

### Database Not Found   - Watch build logs in the dashboard

   - Should complete in 1-2 minutes

**Check**: Database file is committed to Git   - Look for: "✓ Deployment successful"



```bash### Step 3: Get Your Deployment URL

git ls-files | findstr czsu_data.db

```Your MCP server will be available at:

```

**Fix**: Commit the database filehttps://your-project-name.fastmcp.app/mcp

```

```bash

git add data/czsu_data.db**Important:** Note the `/mcp` path at the end - this is the MCP protocol endpoint.

git commit -m "Add database"

git push### Step 4: Test Your Deployment

```

1. **Test Health Endpoint**:

### Build Fails```bash

curl https://your-project-name.fastmcp.app/health

**Check**: FastMCP Cloud logs in dashboard```



**Common issues**:Expected response:

- Entrypoint wrong - must be exactly `main.py:mcp````json

- `mcp` object not exported at module level{

- Missing dependencies in `pyproject.toml`  "status": "healthy",

  "database": "connected",

### Connection Fails  "db_path": "/app/data/czsu_data.db"

}

**Check**: URL format includes `/mcp` at the end```



```2. **Test with FastMCP Client**:

✅ https://your-project-name.fastmcp.app/mcp```python

❌ https://your-project-name.fastmcp.appfrom fastmcp import Client

```import asyncio



## Configurationasync def test():

    async with Client("https://your-project-name.fastmcp.app/mcp") as client:

### Environment Variables        # List available tools

        tools = await client.list_tools()

Set in FastMCP Cloud dashboard if needed:        print("Available tools:", tools)

- `PORT` - Server port (auto-set by FastMCP Cloud)        

- `DB_PATH` - Database path (default: `./data/czsu_data.db`)        # Test sqlite_query tool

- `DEBUG` - Debug logging (default: `0`)        result = await client.call_tool("sqlite_query", {

            "query": "SELECT name FROM sqlite_master WHERE type='table' LIMIT 3"

### Security        })

        print("Query result:", result)

For public access:

- Enable authentication in FastMCP Cloud settingsasyncio.run(test())

- Use environment variables for sensitive data```

- Monitor logs for suspicious activity

3. **Check FastMCP Cloud Dashboard**:

## Monitoring   - View logs for any errors

   - Check deployment status

### FastMCP Cloud Dashboard   - Monitor resource usage



Monitor:### Step 5: Update Main Application

- **Build Status**: Success/failure

- **Logs**: Real-time server output1. **Edit `.env` in main project**:

- **Deployments**: History and rollback```env

- **Settings**: Environment variablesMCP_SERVER_URL=https://your-project-name.fastmcp.app/mcp

USE_LOCAL_SQLITE_FALLBACK=1

### Health Checks```



Set up monitoring (optional):2. **Test Main Application**:

   - Restart your main application

```powershell   - Execute a query

# Simple PowerShell health check script   - Check logs for: "🌐 Using REMOTE MCP server at: https://your-project-name.fastmcp.app/mcp"

while ($true) {   - Verify queries execute correctly

    try {

        $response = Invoke-WebRequest -Uri "https://your-project-name.fastmcp.app/health"3. **Deploy Main Application** (if needed):

        Write-Host "✓ Server healthy" -ForegroundColor Green   - Push changes to your main app repo

    } catch {   - Deploy to your hosting platform (Railway, Vercel, etc.)

        Write-Host "✗ Health check failed!" -ForegroundColor Red

    }## Post-Deployment Verification

    Start-Sleep -Seconds 300

}### ✅ Check MCP Server

```

- [ ] Health endpoint returns "healthy"

## Rollback- [ ] FastMCP Client can connect and list tools

- [ ] Query tool executes successfully

If deployment fails:- [ ] No errors in FastMCP Cloud logs



1. **Main App**: Switch to local mode temporarily### ✅ Check Main Application

   ```env

   MCP_SERVER_URL=- [ ] Connects to remote MCP server

   USE_LOCAL_SQLITE_FALLBACK=1- [ ] Queries execute successfully

   ```- [ ] Console shows remote mode active

- [ ] Fallback works if MCP server is temporarily unavailable

2. **Debug**: Check FastMCP Cloud logs

### ✅ Check FastMCP Cloud Dashboard

3. **Fix and Redeploy**: Push fixes to GitHub

- [ ] Build completed successfully

4. **Or Rollback**: Use FastMCP Cloud dashboard to revert to previous deployment- [ ] Deployment status is "Active"

- [ ] No error logs

## Cost- [ ] Response times reasonable (<2 seconds)



- **Free during beta** 🎉## Troubleshooting

- No credit card required

- Check https://fastmcp.cloud for current pricing### ❌ "Database not found" Error



## Resources**Cause**: Database file not included in deployment or path is wrong



- **FastMCP Cloud**: https://fastmcp.cloud**Fix**:

- **FastMCP Docs**: https://gofastmcp.com/1. Check `.gitignore` doesn't exclude `data/czsu_data.db`

- **MCP Protocol**: https://spec.modelcontextprotocol.io/2. Verify file is committed to Git: `git ls-files | findstr czsu_data.db`

- **Package Management**: See `PACKAGE_MANAGEMENT.md`3. Push to GitHub and FastMCP Cloud will auto-redeploy

4. Check entrypoint is exactly: `main.py:mcp`

## Support

### ❌ "Cannot find 'mcp' in main.py"

For issues:

- Check FastMCP Cloud dashboard logs**Cause**: Entrypoint misconfigured or `mcp` object not exported

- Review this guide

- Contact FastMCP Cloud support via their website**Fix**:

1. Verify `main.py` has: `mcp = FastMCP("CZSU-SQLite-Server", ...)`
2. Ensure `mcp` is at module level (not inside if __name__ block)
3. Set entrypoint in FastMCP Cloud to exactly: `main.py:mcp`
4. Redeploy

### ❌ "Import Error" or "Module Not Found"

**Cause**: Missing dependencies in requirements.txt

**Fix**:
1. Check `pyproject.toml` has `fastmcp>=2.0.0` in dependencies
2. Verify all dependencies listed
3. Check FastMCP Cloud build logs for specific missing module
4. Update pyproject.toml (or requirements.txt) and push

### ❌ FastMCP Client Connection Fails

**Cause**: Wrong URL or server not running

**Fix**:
1. Verify URL format: `https://your-project-name.fastmcp.app/mcp` (note `/mcp` at end)
2. Test health endpoint: `https://your-project-name.fastmcp.app/health`
3. Check FastMCP Cloud dashboard for deployment status
4. Look for errors in FastMCP Cloud logs

### ❌ "Port Already in Use" (Local Testing)

**Cause**: Another process using port 8100

**Fix**:
```bash
# Windows:
netstat -ano | findstr :8100
taskkill /PID <PID> /F

# Or change port in .env:
PORT=8101
```

### ❌ FastMCP Cloud Build Fails

**Check**:
1. Build logs in FastMCP Cloud dashboard for specific error
2. Python version compatibility (needs 3.10+)
3. All files committed and pushed to GitHub
4. Entrypoint format correct

**Common fixes**:
- Ensure `requirements.txt` has correct versions
- Check for typos in `main.py`
- Verify database file size is reasonable (<100MB)
- Make sure repository is public or FastMCP Cloud has access

### ❌ Auto-deployment Not Working

**Cause**: GitHub webhook not configured or disabled

**Fix**:
1. Check FastMCP Cloud project settings
2. Verify GitHub repository access
3. Try manual redeploy in dashboard
4. Check if you're pushing to the correct branch (should be `main`)

## Auto-Deployment Features

FastMCP Cloud provides seamless CI/CD:

### Main Branch Auto-Deployment

- **Trigger**: Push to `main` branch
- **Action**: Automatic build and deploy
- **Time**: Usually 1-2 minutes
- **Notification**: Check dashboard for status

### Pull Request Previews

- **Trigger**: Open a pull request
- **Action**: Deploys preview environment
- **URL**: Temporary preview URL provided
- **Use**: Test changes before merging

### Manual Deployment

- Click "Redeploy" in FastMCP Cloud dashboard
- Use for troubleshooting or forcing a rebuild
- Does not require code changes

## Monitoring

### FastMCP Cloud Dashboard

Monitor in the dashboard:
- **Build Status**: Success/failure of deployments
- **Logs**: Real-time server logs
- **Deployments**: History of all deployments
- **Settings**: Configuration and environment variables

### Health Checks

Set up automated monitoring (optional):
```bash
# Simple PowerShell script
while ($true) {
    $response = Invoke-WebRequest -Uri "https://your-project-name.fastmcp.app/health" -UseBasicParsing
    if ($response.StatusCode -ne 200) {
        Write-Host "Health check failed!" -ForegroundColor Red
    } else {
        Write-Host "Server healthy" -ForegroundColor Green
    }
    Start-Sleep -Seconds 300  # Check every 5 minutes
}
```

### Application Logs

Check logs from main application:
- Connection successful: "🌐 Using REMOTE MCP server at: ..."
- Query execution times
- Fallback activation (if server unavailable)

## Cost & Pricing

**FastMCP Cloud Pricing**:
- **Free during beta period** 🎉
- No credit card required during beta
- Check https://fastmcp.cloud for current pricing

**Future Considerations**:
- Monitor usage as product exits beta
- Free tier may be available for small projects
- For high-traffic production use, check pricing page

## Rollback Plan

If deployment fails or issues occur:

1. **Main App**: Change `.env` back to local mode:
   ```env
   MCP_SERVER_URL=
   USE_LOCAL_SQLITE_FALLBACK=1
   ```

2. **Main App**: Restart - will automatically use local SQLite

3. **Debug MCP Server**: 
   - Review FastMCP Cloud logs in dashboard
   - Fix issues in code
   - Push to GitHub (auto-redeploys)

4. **Rollback Deployment**:
   - FastMCP Cloud dashboard shows deployment history
   - Can revert to previous successful deployment if needed

## Security Notes

### ⚠️ Current Setup

The current implementation has **NO authentication** by default. This is fine for:
- Internal use only
- Private network access
- Development/testing

### 🔒 For Production (Public Access)

If enabling FastMCP Cloud authentication:
1. Enable authentication in project settings
2. Use API keys provided by FastMCP Cloud
3. Configure main application with credentials

Additional security measures:
- Enable HTTPS enforcement (FastMCP Cloud provides automatically)
- Use environment variables for sensitive data
- Monitor logs for suspicious activity
- Consider IP restrictions if available

### 🔐 Database Security

- Database is read-only (queries only, no writes)
- No SQL injection risk (parameterized queries)
- Database included in deployment (not external connection)
- No sensitive credentials stored in database

## Success Criteria

Your deployment is successful when:

✅ MCP server running on FastMCP Cloud  
✅ Health endpoint returns "healthy"  
✅ FastMCP Client can connect and list tools  
✅ Main application connects successfully  
✅ Queries execute and return results  
✅ Fallback mechanism works when tested  
✅ No errors in FastMCP Cloud logs  
✅ Response times acceptable (<2 seconds)  
✅ Auto-deployment working (push triggers redeploy)  

## Next Steps After Deployment

1. **Monitor for 24 hours**: Watch FastMCP Cloud dashboard and logs
2. **Test fallback**: Temporarily disable MCP server in dashboard, verify main app falls back to local SQLite
3. **Update documentation**: Note the production MCP URL in your team docs
4. **Share with team**: Provide MCP server URL to team members
5. **Set up monitoring**: Configure alerts if needed (health check scripts)
6. **Test auto-deployment**: Make a small change, push to `main`, verify auto-redeploy works

## Additional Resources

### Documentation
- **FastMCP Docs**: https://gofastmcp.com/
- **FastMCP Cloud**: https://fastmcp.cloud
- **MCP Protocol Spec**: https://spec.modelcontextprotocol.io/
- **Main Project Docs**: See `MCP_IMPLEMENTATION_SUMMARY.md`
- **Testing Guide**: See `TESTING_MCP_SETUP.md`
- **MCP Server README**: See `czsu_mcp_server_sqlite/README.md`

### Support
- **FastMCP Cloud Support**: Contact via https://fastmcp.cloud
- **FastMCP Community**: Join discussions on GitHub
- **Issues**: Report bugs or request features

---

**Ready to Deploy?** Follow the checklist above and you'll have your MCP server running on FastMCP Cloud in minutes! 🚀

Good luck with your deployment!
