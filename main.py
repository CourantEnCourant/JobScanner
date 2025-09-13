from fastmcp import FastMCP
import boto3

from pathlib import Path
import os

mcp = FastMCP("Echo Server", port=3000, stateless_http=True, debug=True)

@mcp.tool(description="Upload a file on aws and give a link to the user")
def send_file(file_path: str) -> str:
    bucket_name = "mistral-mcp-hackathon"
    local_file = file_path
    object_name = Path(local_file).name

    try:
        s3 = boto3.client("s3")
        s3.upload_file(local_file, bucket_name, object_name)
        return f"https://{bucket_name}.s3.eu-north-1.amazonaws.com/{object_name}"
    except Exception as e:
        return f"An error occurred: {e}"

@mcp.tool(description="Create a .tex file from the given LaTeX source and save it to ./cv/cv.tex")
def create_tex(latex: str) -> str:
    try:
        with open(Path("./cv/cv.tex"), "w") as f:
            f.write(latex)
        return "Tex created successfully"
    except Exception as e:
        return f"Tex creation failed: {e}"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
