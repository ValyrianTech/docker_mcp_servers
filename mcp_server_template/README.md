# Simple MCP Test Server

A basic MCP (Model Context Protocol) server built with FastMCP for testing purposes.

## Features

- Basic arithmetic tools: `add` and `multiply`
- Static resource: `greeting://welcome`
- Dynamic resource template: `info://{topic}`
- Context-aware tool: `echo_with_context`

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Server

Run the server using:

```bash
python server.py
```

This starts the server using the SSE transport on `http://127.0.0.1:8000/sse/`. You can access the server at this URL.

## Testing the Server

You can test this server with any MCP client. Here's an example using FastMCP's client:

```python
from fastmcp import Client

async def main():
    # Connect to the SSE server
    async with Client("http://127.0.0.1:8000/sse/") as client:
        # List available tools
        tools = await client.list_tools()
        print(f"Available tools: {tools}")
        
        # Call the add tool
        result = await client.call_tool("add", {"a": 5, "b": 3})
        print(f"5 + 3 = {result}")
        
        # Call the multiply tool
        result = await client.call_tool("multiply", {"a": 4, "b": 2.5})
        print(f"4 * 2.5 = {result}")
        
        # Read the welcome resource
        welcome = await client.read_resource("greeting://welcome")
        print(f"Welcome message: {welcome}")
        
        # Read a dynamic resource
        info = await client.read_resource("info://mcp")
        print(f"MCP info: {info}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

Save this as `test_client.py` and run it to test your server.

## Alternative Transport Options

If you want to use a different transport, you can modify the `server.py` file:

### For STDIO (default)
```python
mcp.run()  # or explicitly: mcp.run(transport="stdio")
```

### For HTTP
```python
mcp.run(transport="http", host="127.0.0.1", port=8000, path="/mcp")
