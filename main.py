from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport

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

@mcp.app.get("/favicon.ico")
async def favicon():
    return {}

if __name__ == "__main__":
    mcp.run()