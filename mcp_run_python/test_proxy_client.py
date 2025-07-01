#!/usr/bin/env python3
from mcp import ClientSession
from mcp.client.sse import sse_client
import asyncio
import json

async def main():
    print("Connecting to MCP Run Python proxy server...")
    try:
        # Connect to the proxy server using SSE transport
        async with sse_client("http://localhost:8080/sse/") as (read, write):
            print("Connected to MCP Run Python proxy server")
            
            # Create a client session
            async with ClientSession(read, write) as session:
                print("Initializing session...")
                await session.initialize()
                print("Session initialized")
                
                # List available tools
                print("\nListing tools...")
                tools = await session.list_tools()
                print(f"Number of tools: {len(tools.tools)}")
                for tool in tools.tools:
                    print(f"Tool name: {tool.name}")
                    print(f"Tool schema: {json.dumps(tool.inputSchema, indent=2)}")
                
                # Run a simple Python code example
                print("\nRunning Python code...")
                python_code = """
import numpy as np
a = np.array([1, 2, 3])
print("Hello from Python!")
print(f"NumPy array: {a}")
a * 2
"""
                result = await session.call_tool('run_python_code', {'python_code': python_code})
                print("Result:")
                print(json.dumps(result.content[0].text, indent=2))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
