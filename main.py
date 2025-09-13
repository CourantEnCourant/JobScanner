from fastmcp import FastMCP

from pathlib import Path
import os

mcp = FastMCP("Echo Server", port=3000, stateless_http=True, debug=True)

@mcp.tool(description="Create a .tex file from the given LaTeX source and save it to ./cv/cv.tex")
def create_tex(latex: str) -> str:
    try:
        with open(Path("./cv/cv.tex"), "w") as f:
            f.write(latex)
        return "Tex created successfully"
    except Exception as e:
        return f"Tex creation failed: {e}"

@mcp.tool(description="Not implemented yet")
def compile_tex(tex_path: str) -> str:
    with open(tex_path, "r") as f:
        tex = f.read()
    return ""


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
