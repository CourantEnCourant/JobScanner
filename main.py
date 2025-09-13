import asyncio
from typing import Any
import httpx
import os
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("jobscanner")

entries = []


@mcp.tool()
async def search_jobs(query: str, location: str = "", country: str = "us", date_posted: str = "all", limit: int = 10) -> str:
    """Search for jobs using JSearch API based on query and location"""
    api_key = os.getenv("RAPIDAPI_KEY")
    if not api_key:
        return "Error: RAPIDAPI_KEY environment variable not set. Please set your RapidAPI key."

    # Prepare the search query - combine query and location if location is provided
    search_query = query
    if location:
        search_query = f"{query} in {location}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://jsearch.p.rapidapi.com/search",
                headers={
                    "x-rapidapi-host": "jsearch.p.rapidapi.com",
                    "x-rapidapi-key": api_key
                },
                params={
                    "query": search_query,
                    "page": "1",
                    "num_pages": "1",
                    "country": country,
                    "date_posted": date_posted
                }
            )
            response.raise_for_status()
            data = response.json()

            jobs = data.get("data", [])
            if not jobs:
                return f"No jobs found matching query: '{query}' in location: '{location}' (country: {country})"

            # Limit results
            jobs = jobs[:limit]

            # Format results
            result = f"Found {len(jobs)} job(s) matching '{query}'"
            if location:
                result += f" in '{location}'"
            result += f" (country: {country}):\n\n"

            for i, job in enumerate(jobs, 1):
                employer_name = job.get("employer_name", "Unknown Company")
                job_title = job.get("job_title", "Unknown Title")
                job_city = job.get("job_city", "")
                job_country = job.get("job_country", "")
                location_str = f"{job_city}, {job_country}" if job_city and job_country else job_city or job_country or "Location not specified"
                job_description = job.get("job_description", "")[:200] + "..." if len(job.get("job_description", "")) > 200 else job.get("job_description", "")
                job_url = job.get("job_apply_link", "No URL available")

                result += f"{i}. **{job_title}** at {employer_name}\n"
                result += f"   Location: {location_str}\n"
                if job_description:
                    result += f"   Description: {job_description}\n"
                result += f"   Apply: {job_url}\n\n"

            return result

    except httpx.HTTPStatusError as e:
        return f"API Error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error searching jobs: {str(e)}"
    

@mcp.tool()
async def add_job_application_entry(company_name:str, job_title:str) -> str:
    entries.append((company_name, job_title))
    return "Job application entry added successfully"

@mcp.tool()
async def get_job_application_entries() -> str:
    """Get all job application entries as csv"""
    return "company_name,job_title\n" + "\n".join([f"{company_name},{job_title}" for company_name, job_title in entries])


from dotenv import load_dotenv

load_dotenv()


from browser_use import Agent, ChatGoogle
import asyncio

async def run_agent(agent:Agent):
    await agent.run(max_steps=5) # 5 for now so we on purpose do not loop forever


@mcp.tool()
async def fill_applcation_form(url:str):
    """
    Fill the application form for the given URL
    """
    llm = ChatGoogle(model="gemini-2.5-flash") # requires GEMINI_API_KEY
    file_path = "/Users/titouv/Developer/JobScanner/resume.pdf"
    url = "https://jobs.lever.co/mistral/7894fd8a-ffc9-4c89-87f0-f8a7b695cf01/apply" # harcoded for now
    task = f"Fill the form from {url} with file {file_path}, start with the file field the others after"
    agent = Agent(task=task, llm=llm,available_file_paths=[file_path])
    asyncio.create_task(run_agent(agent))
    return agent.task_id

if __name__ == "__main__":

    # Initialize and run the server
    mcp.run(transport='streamable-http')
