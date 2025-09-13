import asyncio
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from stagehand import StagehandConfig, Stagehand

# Load environment variables
load_dotenv()

# Define Pydantic models for structured data extraction
class Company(BaseModel):
    name: str = Field(..., description="Company name")
    description: str = Field(..., description="Brief company description")

class Companies(BaseModel):
    companies: list[Company] = Field(..., description="List of companies")
    
async def main():
    # Create configuration
    config = StagehandConfig(
        env = "BROWSERBASE", # or LOCAL
        api_key=os.getenv("BROWSERBASE_API_KEY"),
        project_id=os.getenv("BROWSERBASE_PROJECT_ID"),
        model_name="google/gemini-2.5-flash-preview-05-20",
        model_api_key=os.getenv("MODEL_API_KEY"),
    )
    
    stagehand = Stagehand(config)
    
    try:
        print("\nInitializing 🤘 Stagehand...")
        # Initialize Stagehand
        await stagehand.init()

        if stagehand.env == "BROWSERBASE":    
            print(f"🌐 View your live browser: https://www.browserbase.com/sessions/{stagehand.session_id}")

        page = stagehand.page

        await page.goto("https://jobs.lever.co/mistral/7894fd8a-ffc9-4c89-87f0-f8a7b695cf01/apply")

        actions = await page.observe("apply for the job offer with dummy data, we are in france, feel all the fields in the form")
        print(f"Actions: {actions}")
        for action in actions:
            acted = await page.act(action)
            print(f"Acted: {acted}")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        raise
    finally:
        # Close the client
        print("\nClosing 🤘 Stagehand...")
        await stagehand.close()

if __name__ == "__main__":
    asyncio.run(main())