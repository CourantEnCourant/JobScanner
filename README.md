# JobScanner

Job dating app for Mistral MCP Hackathon - An MCP server that helps users find jobs, personalize their CV, and automate job applications.

## Setup & API Keys

### Required API Keys

| Service         | Key                                               | How to Get                                                                                                                    | Purpose                             |
| --------------- | ------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ----------------------------------- |
| **RapidAPI**    | `RAPIDAPI_KEY`                                    | 1. Visit [RapidAPI](https://rapidapi.com/)<br>2. Sign up/login<br>3. Subscribe to JSearch API<br>4. Get your API key          | Job search functionality            |
| **Browserbase** | `BROWSERBASE_API_KEY`<br>`BROWSERBASE_PROJECT_ID` | 1. Visit [Browserbase](https://browserbase.com/)<br>2. Create account<br>3. Create a project<br>4. Get API key and project ID | Browser automation for form filling |
| **Google AI**   | `MODEL_API_KEY`                                   | 1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)<br>2. Create API key                                    | AI-powered form completion          |
| **AWS**         | `AWS_ACCESS_KEY_ID`<br>`AWS_SECRET_ACCESS_KEY`    | 1. AWS Console → IAM<br>2. Create user with S3 permissions<br>3. Generate access keys                                         | File storage for CV templates       |

### Environment Setup

1. Create a `.env` file in the project root:

```bash
RAPIDAPI_KEY=your-rapidapi-key-here
BROWSERBASE_API_KEY=your-browserbase-key-here
BROWSERBASE_PROJECT_ID=your-project-id-here
MODEL_API_KEY=your-gemini-key-here
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
```

2. Load environment variables:

```bash
# Option 1: Load from .env file (if using python-dotenv)
python -c "from dotenv import load_dotenv; load_dotenv()"

# Option 2: Export manually
export RAPIDAPI_KEY="your-key"
export BROWSERBASE_API_KEY="your-key"
# ... etc
```

## External Tools & Services

| Service           | Library/Package | Purpose                      |
| ----------------- | --------------- | ---------------------------- |
| **JSearch API**   | `httpx`         | Job search and listings      |
| **Browserbase**   | `browserbase`   | Headless browser automation  |
| **Stagehand**     | `stagehand-py`  | AI-powered form filling      |
| **Google Gemini** | `stagehand-py`  | AI model for form completion |
| **AWS S3**        | `boto3`         | File storage and hosting     |
| **Overleaf**      | -               | LaTeX compilation service    |
| **Vercel Blob**   | `httpx`         | Resume file storage          |

## Available Tools

| Tool                                    | Description                                  | External Dependencies          |
| --------------------------------------- | -------------------------------------------- | ------------------------------ |
| `search_jobs`                           | Search for job offers using multiple queries | RapidAPI JSearch               |
| `fetch_url`                             | Fetch content from any URL                   | None                           |
| `fill_application_form`                 | Auto-fill job application forms              | Browserbase, Stagehand, Gemini |
| `add_job_application_entry`             | Track job applications locally               | None                           |
| `get_job_application_entries`           | Export tracked applications as CSV           | None                           |
| `update_user_info`                      | Update professional information              | None                           |
| `read_user_info`                        | Read stored professional info                | None                           |
| `list_templates`                        | List available CV templates                  | None                           |
| `read_template`                         | Read LaTeX CV template files                 | None                           |
| `upload_tex_then_compile_with_overleaf` | Upload LaTeX to AWS and create Overleaf link | AWS S3                         |
| `create_tex`                            | Generate LaTeX files from content            | None                           |

## Running

```bash
python main.py
```

## Architecture

This MCP server integrates multiple services to provide end-to-end job search assistance:

- **Job Discovery**: Uses RapidAPI's JSearch for comprehensive job listings
- **CV Personalization**: LaTeX templates with Overleaf integration
- **Application Automation**: Browserbase + Stagehand for automated form filling
- **File Storage**: AWS S3 for CV hosting, Vercel Blob for resume storage
- **AI Enhancement**: Google Gemini for intelligent form completion
