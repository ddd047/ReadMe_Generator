# Project Instructions

Initialize a new project to build an automated GitHub README generator. The goal is to create a system that automatically updates or appends to a repository's README.md file whenever Python files (.py) or Jupyter Notebooks (.ipynb) are pushed or uploaded to GitHub.

Please build the project according to the following technical blueprint:

1. Directory Structure:
   - Create a workflow file at: `.github/workflows/auto-readme.yml`
   - Create the core script at: `script/generate_readme.py`
   - Ensure a clean, logical project layout.

2. Python Script Logic (`script/generate_readme.py`):
   - Check if an existing 'README.md' file exists in the root directory. If it does, read and store its contents.
   - Scan the repository for modified or new `.py` and `.ipynb` files. 
   - For `.ipynb` files, parse them safely using Python's core `json` library to extract text from code and markdown cells only, stripping out complex metadata.
   - Connect to the Gemini API using the official `google-genai` SDK.
   - Construct a structured prompt for the AI that passes:
     a) The existing README content (if any).
     b) The extracted content of the new/modified code files.
   - Instruct the LLM using strict guidelines: "Analyze the new code. Do not rewrite, alter, or delete the existing content of the README.md. Append a new, contextually relevant section explaining the new files at the bottom. Mirror the exact same markdown style, headers, and linguistic tone as the existing document."
   - Overwrite the local 'README.md' with the unified response returned by the API.

3. GitHub Actions Configuration (`.github/workflows/auto-readme.yml`):
   - Set the trigger to execute automatically `on: push`.
   - Implement path filters (`paths:`) so the action only triggers if files ending in `**.py` or `**.ipynb` are updated or added. (This naturally catches terminal pushes and browser drag-and-drop web uploads).
   - Configure the environment to check out the code, set up a Python 3.10 environment, and install dependencies (`google-genai`).
   - Securely map an environment variable `AI_API_KEY` using GitHub Repository Secrets (`${{ secrets.AI_API_KEY }}`).
   - Add a final step to automatically configure a git user (e.g., 'ReadmeBot'), stage the updated `README.md`, commit the change with a message like 'docs: auto-updated README', and push it back to the branch. Implement an `|| exit 0` safeguard so the workflow doesn't fail if no changes were made.

4. Execution Guardrails:
   - Use clean, well-commented Python code.
   - Implement robust error handling (e.g., if a file is empty or the API fails to respond).
   - Provide an implementation plan and a detailed task checklist before writing the files..
