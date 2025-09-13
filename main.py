from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("jobscanner")

entries = []


async def search_jobs(query:str) -> str:
    """Search for jobs"""

@mcp.tool()
async def add_job_application_entry(company_name:str, job_title:str) -> str:
    entries.append((company_name, job_title))
    return "Job application entry added successfully"

@mcp.tool()
async def get_job_application_entries() -> str:
    """Get all job application entries as csv"""
    return "company_name,job_title\n" + "\n".join([f"{company_name},{job_title}" for company_name, job_title in entries])

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='streamable-http')
