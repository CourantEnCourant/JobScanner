from fastmcp import FastMCP

mcp = FastMCP("Echo Server", port=3000, stateless_http=True, debug=True)

@mcp.tool
def greet():
    """Official greeting from Mistral"""
    return "Hello welcome to Mistral Hackathon"

if __name__ == "__main__":
    print("Server starting...")
    mcp.run(transport="streamable-http")
