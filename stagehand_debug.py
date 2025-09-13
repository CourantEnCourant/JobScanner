# Generated script for workflow 58342cff-2401-41fc-9a48-4a941bc45b65
# Generated at 2025-09-13T17:14:05.442Z


import asyncio
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from stagehand import StagehandConfig, Stagehand

# Load environment variables
load_dotenv()
import os
import tempfile
import pathlib

async def run_workflow():
    stagehand = None

    config = StagehandConfig(
        env="BROWSERBASE",
        api_key=os.getenv("BROWSERBASE_API_KEY"),
        project_id=os.getenv("BROWSERBASE_PROJECT_ID"),
        model_name="google/gemini-2.5-flash-preview-05-20",
        model_api_key=os.getenv("MODEL_API_KEY"),
    )

    try:
        # Initialize Stagehand
        print("Initializing Stagehand...")
        stagehand = Stagehand(config)
        await stagehand.init()
        print("Stagehand initialized successfully.")

        print(f"Stagehand environment: {stagehand.env}")

        # Always return the browser URL early since we're always in BROWSERBASE mode
        browser_url = f"https://www.browserbase.com/sessions/{stagehand.session_id}"
        print(f"🌐 View your live browser: {browser_url}")

        # Get the page instance
        page = stagehand.page
        if not page:
            raise Exception("Failed to get page instance from Stagehand")

        # Step 1: Navigate to URL
        print(
            "Navigating to: https://jobs.lever.co/mistral/7894fd8a-ffc9-4c89-87f0-f8a7b695cf01/apply"
        )
        await page.goto(
            "https://jobs.lever.co/mistral/7894fd8a-ffc9-4c89-87f0-f8a7b695cf01/apply"
        )

        # Step 2: upload resume PDF to the Resume/CV field
        print("Preparing file upload...")

        # Download file from URL
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

        # # Upload to form
        # print("Uploading file to form...")
        # await page.set_input_files(
        #     "xpath=/html[1]/body[1]/div[2]/div[1]/div[2]/form[1]/div[1]/ul[1]/li[1]/label[1]/div[2]/a[1]/input[1]",
        #     str(temp_file_path)
        # )
        # print("File uploaded successfully")

        # Filter results
        resume_field_input = await page.observe("find all <input type='file'> input for a pdf resume file")
        print(f"Resume field input: {resume_field_input}")
        first_resume_field_input = resume_field_input[0]
        print(f"First resume field input: {first_resume_field_input}")
        await page.set_input_files(
            first_resume_field_input.selector,
            str(temp_file_path)
        )
        print("File uploaded successfully")

        # actions = await page.observe(f"apply for the job offer with dummy data with the resume file {str(temp_file_path)}")
        # print(f"Actions: {actions}")
        # for action in actions:
        #     acted = await page.act(action)
        #     print(f"Acted: {acted}")

        # Clean up
        temp_file_path.unlink()


        # sleep 1 second)
        await asyncio.sleep(10)

        print("Workflow completed successfully")
        return {"success": True}

    except Exception as error:
        print("Workflow failed:", str(error))
        return {"success": False, "error": str(error)}

    finally:
        # Clean up
        if stagehand:
            print("Closing Stagehand connection.")
            try:
                await stagehand.close()
            except Exception as err:
                print("Error closing Stagehand:", str(err))

# Single execution
if __name__ == "__main__":
    import asyncio
    import httpx

    result = asyncio.run(run_workflow())
    print("Execution result:", result)
    exit(0 if result["success"] else 1)
