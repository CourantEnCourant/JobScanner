from fastmcp import FastMCP

mcp = FastMCP("Demo 🚀")

@mcp.tool
def greet():
    """Official greeting from Mistral"""
    return "Hello welcome to Mistral Hackathon"

if __name__ == "__main__":
    print("Server starting...")
    mcp.run()
