from fastmcp import Client

async def main():
    # Connect to the SSE server
    async with Client("http://127.0.0.1:8080/sse") as client:
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
        
        # Test the context-aware tool
        result = await client.call_tool("echo_with_context", {"message": "Hello MCP!"})
        print(f"Echo response: {result}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
