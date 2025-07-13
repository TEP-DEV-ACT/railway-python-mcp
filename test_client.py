#!/usr/bin/env python3
"""
Simple test client for the MCP server
"""
import asyncio
import json
import subprocess
import sys

async def test_mcp_server():
    """Test the MCP server by sending JSON-RPC messages"""
    
    # Start the server process
    process = await asyncio.create_subprocess_exec(
        sys.executable, "main.py",
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    # Initialize the server
    init_message = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {},
                "resources": {}
            },
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        }
    }
    
    # Send initialization message
    message = json.dumps(init_message) + '\n'
    process.stdin.write(message.encode())
    await process.stdin.drain()
    
    # Read response
    response_line = await process.stdout.readline()
    if response_line:
        response = json.loads(response_line.decode())
        print("Server initialized successfully!")
        print(f"Server capabilities: {response.get('result', {}).get('capabilities', {})}")
    
    # Test the add tool
    tool_call = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "add",
            "arguments": {
                "a": 5,
                "b": 3
            }
        }
    }
    
    message = json.dumps(tool_call) + '\n'
    process.stdin.write(message.encode())
    await process.stdin.drain()
    
    # Read tool response
    response_line = await process.stdout.readline()
    if response_line:
        response = json.loads(response_line.decode())
        print(f"Tool call result: {response}")
    
    # Clean up
    process.stdin.close()
    await process.wait()

if __name__ == "__main__":
    print("Testing MCP Server...")
    asyncio.run(test_mcp_server())
