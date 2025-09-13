from fastmcp import FastMCP
import boto3

from pathlib import Path
from dotenv import load_dotenv


load_dotenv()

mcp = FastMCP("Echo Server", port=3000, stateless_http=True, debug=True)


@mcp.tool(description="Update user's professional information")
async def update_user_info(user_info: str) -> str:
    with open("user_info.txt", "w") as f:
        try:
            f.write(user_info)
            return "Update success"
        except Exception as e:
            return f"Update failed with following exception: {e}"


@mcp.tool(description="Read user's professional information")
async def read_user_info() -> str:
    with open("user_info.txt", "r") as f:
        try:
            return f.read()
        except Exception as e:
            return f"Reading failed with following exception: {e}"


@mcp.tool(description="List all existing cv templates")
async def list_templates() -> list[str] | str:
    try:
        template_dir = Path(__file__).parent / "cv_templates"
        return [str(p) for p in template_dir.glob("*.tex")]
    except Exception as e:
        return f"An error occurred: {e}"


@mcp.tool(description="Read a local .tex file for cv template")
async def read_template(template_path: str) -> str:
    with open(template_path) as f:
        return f.read()


@mcp.tool(description="Upload a .tex file on aws and return a overleaf link for manual compilation")
async def upload_tex_then_compile_with_overleaf(file_path: str) -> str:
    bucket_name = "mistral-mcp-hackathon"
    local_file = file_path
    object_name = Path(local_file).name

    try:
        s3 = boto3.client("s3")
        s3.upload_file(local_file, bucket_name, object_name)
        tex_url = f"https://{bucket_name}.s3.eu-north-1.amazonaws.com/{object_name}"
        return f"https://www.overleaf.com/docs?snip_uri={tex_url}"
    except Exception as e:
        return f"An error occurred: {e}"


@mcp.tool(description="Create a .tex file from the given LaTeX source and save it to ./cv/cv.tex")
async def create_tex(latex: str) -> str:
    try:
        with open(Path("./cv/cv.tex"), "w") as f:
            f.write(latex)
        return "Tex created successfully"
    except Exception as e:
        return f"Tex creation failed: {e}"


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
