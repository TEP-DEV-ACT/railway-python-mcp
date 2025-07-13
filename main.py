import asyncio
import os
from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import JSONResponse
import uvicorn

# Create FastMCP instance
mcp = FastMCP("Railway Python MCP")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

# Health check endpoint for Railway
async def health_check(request):
    return JSONResponse({"status": "healthy", "service": "Railway Python MCP"})

# Create Starlette app for Railway
app = Starlette(routes=[
    Route("/health", health_check),
])

# Add MCP SSE endpoint
mcp.add_sse_endpoint(app, "/mcp")

if __name__ == "__main__":
    # Get port from environment (Railway sets this)
    port = int(os.environ.get("PORT", 8080))
    
    # For local testing, use stdio
    if os.environ.get("RAILWAY_ENVIRONMENT") is None:
        print("Running locally with stdio...")
        mcp.run()
    else:
        # For Railway deployment, run web server
        print(f"Running on Railway on port {port}...")
        uvicorn.run(app, host="0.0.0.0", port=port)