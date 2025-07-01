from fastmcp import FastMCP, Context
import logging

# Set up logging to see more detailed information
logging.basicConfig(level=logging.DEBUG)

# Create a server instance
mcp = FastMCP("Simple Test Server 🚀")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers together.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        The sum of the two numbers
    """
    return a + b

@mcp.tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        The product of the two numbers
    """
    return a * b

@mcp.resource("greeting://welcome")
def welcome_message():
    """Return a welcome message."""
    return "Welcome to the Simple Test Server!"

@mcp.resource("info://{topic}")
def get_info(topic: str):
    """Get information about a specific topic.
    
    Args:
        topic: The topic to get information about
    """
    topics = {
        "server": "This is a simple MCP server created for testing purposes.",
        "mcp": "MCP (Model Context Protocol) is a standardized way to provide context and tools to LLMs.",
        "fastmcp": "FastMCP is a Python framework for building MCP servers and clients easily."
    }
    return topics.get(topic, f"No information available about '{topic}'")

@mcp.tool
async def echo_with_context(message: str, ctx: Context) -> str:
    """Echo a message with some context information.
    
    Args:
        message: The message to echo
        ctx: The MCP context
        
    Returns:
        The echoed message with context information
    """
    await ctx.info(f"Received message: {message}")
    return f"You said: {message}"

if __name__ == "__main__":
    print("Starting HTTP server on http://127.0.0.1:8081/mcp")
    # Run the server using HTTP transport (streamable) with explicit path
    mcp.run(transport="http", host="127.0.0.1", port=8081, path="/mcp")
