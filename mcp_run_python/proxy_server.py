#!/usr/bin/env python3
from fastmcp import FastMCP, Context
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio
import sys
import json
from typing import Dict, Any, Optional

# Create a server instance
mcp = FastMCP("MCP Run Python Proxy Server")

# Configure the stdio server parameters
stdio_server_params = StdioServerParameters(
    command='deno',
    args=[
        'run',
        '-N',
        '-R=node_modules',
        '-W=node_modules',
        '--node-modules-dir=auto',
        'jsr:@pydantic/mcp-run-python',
        'stdio',
    ],
)

# Global variables to store the client session and stdio streams
client_session = None
client_initialized = False
read_stream = None
write_stream = None

async def initialize_stdio_client():
    """Initialize the stdio client and return a session."""
    global client_session, client_initialized, read_stream, write_stream
    
    if client_initialized:
        return client_session
    
    print("Connecting to MCP Run Python stdio server...")
    try:
        # Use the context manager properly
        async with stdio_client(stdio_server_params) as (read, write):
            read_stream = read
            write_stream = write
            
            print("Connected to MCP Run Python stdio server")
            
            session = ClientSession(read, write)
            await session.initialize()
            print("Session initialized")
            
            # List available tools for debugging
            tools = await session.list_tools()
            print(f"Number of tools available: {len(tools.tools)}")
            for tool in tools.tools:
                print(f"Tool name: {tool.name}")
                print(f"Tool schema: {tool.inputSchema}")
            
            client_initialized = True
            client_session = session
            return session
    except Exception as e:
        print(f"Error initializing stdio client: {e}")
        sys.exit(1)

@mcp.tool
async def run_python_code(python_code: str, ctx: Context) -> Dict[str, Any]:
    """Run Python code in a secure sandbox using Pyodide.
    
    Args:
        python_code: The Python code to execute
        ctx: The MCP context
        
    Returns:
        The result of executing the Python code
    """
    global client_session
    
    # Initialize the client session if it hasn't been initialized yet
    if not client_session:
        await ctx.info("Initializing stdio client...")
        client_session = await initialize_stdio_client()
    
    try:
        # Forward the request to the stdio server
        await ctx.info("Forwarding Python code execution request to stdio server")
        result = await client_session.call_tool('run_python_code', {'python_code': python_code})
        
        # Parse the result text to extract components
        text = result.content[0].text
        
        # Extract status, dependencies, output, and return value
        status = extract_tag_content(text, "status")
        dependencies = extract_tag_content(text, "dependencies")
        output = extract_tag_content(text, "output")
        return_value = extract_tag_content(text, "return_value")
        
        # Try to parse dependencies and return_value as JSON
        try:
            dependencies = json.loads(dependencies) if dependencies else []
        except:
            dependencies = []
            
        try:
            return_value = json.loads(return_value) if return_value else None
        except:
            return_value = return_value
        
        return {
            "status": status,
            "dependencies": dependencies,
            "output": output,
            "return_value": return_value
        }
    except Exception as e:
        await ctx.error(f"Error executing Python code: {str(e)}")
        return {"error": str(e)}

def extract_tag_content(text: str, tag: str) -> Optional[str]:
    """Extract content between XML-like tags."""
    start_tag = f"<{tag}>"
    end_tag = f"</{tag}>"
    
    start_pos = text.find(start_tag)
    if start_pos == -1:
        return None
    
    start_pos += len(start_tag)
    end_pos = text.find(end_tag, start_pos)
    
    if end_pos == -1:
        return None
    
    return text[start_pos:end_pos].strip()

if __name__ == "__main__":
    # Run the server using SSE transport
    # Use 0.0.0.0 in Docker to allow external connections
    import os
    # Check if we're running in Docker
    if os.environ.get('DOCKER_CONTAINER', ''):
        host = '0.0.0.0'
    else:
        host = '127.0.0.1'
    
    mcp.run(transport="sse", host=host, port=8080)
