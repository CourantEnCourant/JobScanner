from fastmcp import FastMCP

mcp = FastMCP("Demo 🚀")

@mcp.tool
def greet():
    """Just present yourself basically"""
    return "Hello my name is Mistral and I am a helpful AI assistant"

if __name__ == "__main__":
    mcp.run()
