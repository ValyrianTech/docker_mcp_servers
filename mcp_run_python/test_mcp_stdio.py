#!/usr/bin/env python3
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio
import sys

# Use the same code example from the documentation
code = """
import numpy
a = numpy.array([1, 2, 3])
print(a)
a
"""

server_params = StdioServerParameters(
    command='docker',
    args=[
        'run',
        '--rm',
        '-i',
        'mcp-run-python',
    ],
)

async def main():
    print("Connecting to MCP server...")
    try:
        async with stdio_client(server_params) as (read, write):
            print("Connected to MCP server")
            async with ClientSession(read, write) as session:
                print("Initializing session...")
                await session.initialize()
                print("Session initialized")
                
                print("Listing tools...")
                tools = await session.list_tools()
                print(f"Number of tools: {len(tools.tools)}")
                print(f"Tool name: {tools.tools[0].name}")
                print(f"Tool schema: {tools.tools[0].inputSchema}")
                
                print("\nRunning Python code...")
                result = await session.call_tool('run_python_code', {'python_code': code})
                print("Result:")
                print(result.content[0].text)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
