from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport
import asyncio
import logging

# Set up logging to see more detailed information
logging.basicConfig(level=logging.DEBUG)

async def main():
    try:
        print("Connecting to HTTP server at http://127.0.0.1:8081/mcp...")
        
        # Create the transport explicitly for more control
        transport = StreamableHttpTransport(
            url="http://127.0.0.1:8081/mcp",
            # Uncomment to add custom headers if needed
            # headers={"User-Agent": "MCP-Test-Client"}
        )
        client = Client(transport)
        
        print("Client created, attempting to connect...")
        async with client:
            print("Connection established!")
            
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
    except Exception as e:
        print(f"Error: {e}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
