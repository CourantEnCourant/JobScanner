from typing import Any, List, Dict
import httpx
import os
import csv
import json
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from io import StringIO
import logging

# Load environment variables from .env file
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("jobscanner", port=3000, stateless_http=True, debug=True)

# Global variables
result = ""

@mcp.tool()
async def search_jobs(query: str, location: str = "", country: str = "us", date_posted: str = "all", limit: int = 10) -> str:
    """
    Search for jobs online based on the job-related queries. Do not use web queries, use this tool instead. Then create a downloadable CSV file with the results.
    Parameters:
    - query: The job title or keywords to search for.
    - location: The location to filter jobs (optional).
    - country: The country code to filter jobs (default is "us").
    - date_posted: Filter jobs by date posted (e.g., "last_24_hours", "last_7_days", "all").
    - limit: The maximum number of jobs to return (default is 10).
    Returns: A formatted string containing job listings.
    1. Use the RapidAPI JSearch API to search for jobs based on the provided query and location.
    2. Format the results to include job title, company name, location, a brief description, and application link.
    3. Return the formatted job listings as a string.
    Example: search_jobs("software engineer", "San Francisco, CA", "us", "last_7_days", 5)
    Note: Ensure to handle API errors and edge cases where no jobs are found.
    """
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
            global result
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
                result += f"   Apply: {job_url}\n\n\n"

            logging.debug(f"{result}")
            return result

    except httpx.HTTPStatusError as e:
        return f"API Error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error searching jobs: {str(e)}"

@mcp.tool()
def get_more_job_details(employer_name:str, result:str) -> str:
    """
    When user asks about a specific employer, must use this tool to scrape detailed job information from the provided job search results for a specific employer.
    Always use this tool when user asks for more details about a specific employer.
    Parameters:
    - employer_name: The name of the employer to filter job details.
    - result: The job search results string to scrape details from.
    Returns: A formatted string containing detailed job information for the specified employer.
    1. Parse the job search results to find jobs related to the specified employer.
    2. Scrape additional details such as job description, requirements, and salary from the application link.
    3. Return the detailed job information as a string.
    Example: scrape_job_details("Google", result)
    Note: Ensure to handle cases where no jobs are found for the specified employer.
    """
    if not result:
        return "Error: No job search results available. Please perform a job search first."
    else:
        logging.debug(f"Scraping job details for employer: {employer_name} from results.")
    lines = result.split("\n\n\n")

    for line in lines:
        if employer_name.lower() in line.lower():
            # return the link after "Apply:"
            apply_link = line.split("Apply:")[-1].strip()
            logging.debug(f"Found job details for {employer_name}: {apply_link}")
            return f"Job details for {employer_name}:\n at: {apply_link}"

    return f"No job details found for employer: '{employer_name}'"

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='streamable-http')