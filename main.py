import asyncio
import pathlib
import tempfile
from typing import Any
import httpx
import os
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("jobscanner")

entries = []


@mcp.tool()
async def search_jobs(query1: str, query2: str = "", query3: str="", location: str = "", country: str = "us", date_posted: str = "all", limit: int = 10) -> str:
    """
    Search for jobs online based on three job-related queries. Do not use web queries, use this tool instead.

    Use this tool to find jobs matching the user's criteria.
    At least one query (`primary_query`) is required.
    Use the additional queries (`secondary_query` and `tertiary_query`) to broaden the search.

    Args:
        query (str): The primary job title or keyword to search for (e.g., "news writer").
        query2 (str): A secondary job title or keyword to expand the search.
        query3 (str): A tertiary job title or keyword to further expand the search.
        location (str, optional): The location to search for jobs in. Defaults to an empty string (searches nationwide).
        country (str, optional): The country code to filter jobs (e.g., "gb" for the UK). Defaults to "us".
        date_posted (str, optional): Filter jobs by date posted. Options: "all", "today", "3days", "week", "14days". Defaults to "all".
        limit (int, optional): The maximum number of job results to return. Defaults to 10.

    Returns:
        str: A list of jobs matching the search criteria, formatted as a string or JSON.

    Example:
        >>> search_jobs(primary_query="news writer", secondary_query="journalist", country="gb")
        Returns job listings for "news writer" and "journalist" in the UK.
    
    Next step: ask the user about their preferences or their personal background to refine the search.
    Propose the user to modify the CV to better match one of the job offers found.
    """
    api_key = os.getenv("RAPIDAPI_KEY")
    if not api_key:
        return "Error: RAPIDAPI_KEY environment variable not set. Please set your RapidAPI key."

    # Prepare the search query - combine query and location if location is provided
    for query in [query1, query2, query3]:
        if not query:
            continue
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
                        # "num_pages": "1",
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

        except httpx.HTTPStatusError as e:
            return f"API Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error searching jobs: {str(e)}"

    result += "If the query was too broad, consider using more specific keywords or adding a location. Also ask the user about their preferences or their personal background to refine the search."
    return result


@mcp.tool()
async def display_templates() -> str:
    """Display available CV templates.
    Always call this tool when the user wants to create or modify a CV."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8080/templates")
            response.raise_for_status()
            images = response.json()
            return "\n".join(images)
    except httpx.HTTPStatusError as e:
        return f"HTTP Error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error fetching templates: {str(e)}"
    #response = await requests.get("http://localhost:8080/templates")
    #return " ".join(response)


@mcp.tool()
async def fetch_url(url: str) -> Any:
    """Fetch the content of a URL."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.text
    except httpx.HTTPStatusError as e:
        return f"HTTP Error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error fetching URL: {str(e)}"


with open("prompt.txt", "r") as file:
    base_prompt = file.read()

@mcp.prompt()
async def main_prompt(user_input: str) -> str:
    prompt = f"""{base_prompt}
    """
    return prompt


@mcp.tool()
async def add_job_application_entry(company_name:str, job_title:str) -> str:
    entries.append((company_name, job_title))
    return "Job application entry added successfully"

@mcp.tool()
async def get_job_application_entries() -> str:
    """Get all job application entries as csv"""
    return "company_name,job_title\n" + "\n".join([f"{company_name},{job_title}" for company_name, job_title in entries])



from stagehand import StagehandConfig, Stagehand
from dotenv import load_dotenv

load_dotenv()

@mcp.tool()
async def fill_application_form(url:str):
    """
    Fill the application form for the given URL
    """
      # Create configuration - always use BROWSERBASE mode
    config = StagehandConfig(
        env="BROWSERBASE",
        api_key=os.getenv("BROWSERBASE_API_KEY"),
        project_id=os.getenv("BROWSERBASE_PROJECT_ID"),
        model_name="google/gemini-2.5-flash-preview-05-20",
        model_api_key=os.getenv("MODEL_API_KEY"),
    )

    stagehand = Stagehand(config)

    print("\nInitializing 🤘 Stagehand...")
    # Initialize Stagehand
    await stagehand.init()

    print(f"Stagehand environment: {stagehand.env}")

    # Always return the browser URL early since we're always in BROWSERBASE mode
    browser_url = f"https://www.browserbase.com/sessions/{stagehand.session_id}"
    print(f"🌐 View your live browser: {browser_url}")

    # Start the background task for filling the form
    asyncio.create_task(_fill_form_background(stagehand, url))
    return f"Browser session started. View live browser: {browser_url}. Form filling continues in background."


async def _fill_form_background(stagehand: Stagehand, url: str):
    """Background task to fill the application form"""
    try:
        page = stagehand.page

        print(f"Going to {url}")
        await page.goto("https://jobs.lever.co/mistral/7894fd8a-ffc9-4c89-87f0-f8a7b695cf01/apply")

        print(f"Page: {page}")

        ## Download file from URL
        file_url = "https://tiyrs98e90uelbs3.public.blob.vercel-storage.com/resume-OKXnr4Xt5PLwnqSpEo0WoWljdxI2Rh.pdf"
        temp_dir = pathlib.Path(tempfile.gettempdir()) / "uploads"
        temp_dir.mkdir(parents=True, exist_ok=True)

        file_name = pathlib.Path(file_url).name or "uploaded-file"
        temp_file_path = temp_dir / file_name

        print("Downloading file from:", file_url)
        async with httpx.AsyncClient() as client:
            response = await client.get(file_url)
            response.raise_for_status()
            temp_file_path.write_bytes(response.content)


        print("File used for set_input_files:", str(temp_file_path))

        resume_field_input = await page.observe("find all <input type='file'> input for a pdf resume file")
        print(f"Resume field input: {resume_field_input}")
        first_resume_field_input = resume_field_input[0]
        print(f"First resume field input: {first_resume_field_input}")
        await page.set_input_files(
            first_resume_field_input.selector,
            str(temp_file_path)
        )
        print("File uploaded successfully")
        actions = await page.observe(f"apply for the job offer with dummy data")
        print(f"Actions: {actions}")
        # Limit to first 5 actions to not complete the form on purpose
        for action in actions[:5]:
            acted = await page.act(action)
            print(f"Acted: {acted}")


        print("\nClosing 🤘 Stagehand...")
        await stagehand.close()

        print("Background form filling completed successfully")

    except Exception as e:
        print(f"Error in background form filling: {str(e)}")
        try:
            await stagehand.close()
        except:
            pass




if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='streamable-http')
