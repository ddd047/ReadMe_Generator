<<<<<<< HEAD
# Automated GitHub README Generator 🤖📝

An automated CI/CD pipeline that uses the official Google GenAI SDK and Gemini API (`gemini-2.5-flash`) to dynamically document your project. Whenever you push files to GitHub, the pipeline automatically updates or appends file documentation to your `README.md` in real-time.

---

## 🚀 How it Works
1. **GitHub Action Trigger**: The workflow monitors the repository and triggers automatically on **any** push event.
2. **Scan Strategy**: 
   - **Initial Setup**: If `README.md` is missing (or if you run with the `--all` flag), the script does a **full repository sweep** to document all existing files from scratch.
   - **Incremental Updates**: If a `README.md` already exists, the script reads it and only scans the files modified or added in the **most recent commit** to document incremental changes.
3. **Safe File Extraction**: The script reads files securely and ignores irrelevant or unreadable content:
   - **Path Exclusions**: Automatically ignores files located inside `__pycache__`, `.git`, `.github`, `venv`, `.venv`, `node_modules`, `build`, and `dist` folders (even when nested).
   - **Binary Exclusions**: Automatically skips binary, compiled, or media formats (like `.pyc`, `.pdf`, `.png`, `.jpg`, `.zip`, `.db`, etc.).
   - **Size Guard**: Limits payload sizes (skips files > 1MB) and inspects for null bytes to ensure only valid text is sent to the API.
   - **Jupyter Notebook Parsing**: Safely parses `.ipynb` files to extract markdown and code cells while discarding bulky cell metadata.
4. **Resilient AI Call**: Queries the Gemini API using `gemini-2.5-flash`. The script includes built-in **retry logic with exponential backoff** to handle transient API errors (like HTTP 503 or 429 rate limits) gracefully.
5. **Style-Preserving Commit**: The bot appends a contextually relevant section explaining the new files at the bottom, matching the existing document's tone, styling, and formatting, and commits it back to the branch.

---

## 🛠 Setup & Installation

To initialize this automated readme generator in a new or existing repository, follow these steps:

### 1. Copy the Codebase Structure
Ensure your repository has the following files in the exact same directories:
* `.github/workflows/auto-readme.yml` — The GitHub Actions workflow file.
* `script/generate_readme.py` — The core script executing parsing and API calls.

### 2. Configure GitHub Permissions
Since the bot commits the updated `README.md` back to your repository, ensure the workflow has write permissions:
1. Go to your repository settings: **Settings** > **Actions** > **General**.
2. Under **Workflow permissions**, select **Read and write permissions**.
3. Click **Save**.

### 3. Add your Gemini API Key
Create a repository secret so the workflow can safely access the Gemini API:
1. Go to **Settings** > **Secrets and variables** > **Actions**.
2. Click **New repository secret**.
3. Name it **`AI_API_KEY`**.
4. Set the value as your Gemini API key (you can obtain one from [Google AI Studio](https://aistudio.google.com/)).
5. Click **Add secret**.

---

## 💻 Running Locally

You can run the generation script locally to build or force-rebuild your documentation:

Ensure the Google GenAI SDK is installed:
```bash
pip install google-genai
```
Export your Gemini API Key:
```bash
export GEMINI_API_KEY="your-gemini-api-key"
```

### Regular Scan (Incremental Changes)
Compares the last commit with its parent:
```bash
python3 script/generate_readme.py
```

### Full Scan (All Repository Files)
Forces a documentation scan of all files, even if `README.md` already exists:
```bash
python3 script/generate_readme.py --all
```
=======
# Automated README Generator

## Project Overview
This repository implements an automated system for keeping its `README.md` up-to-date using Artificial Intelligence (AI). A GitHub Actions workflow is configured to monitor changes within the repository, trigger a Python script to interact with an AI model for documentation generation, and automatically update the README.

The goal is to ensure that the project documentation remains current with the codebase, reducing manual effort and potential for outdated information.

## Core Components

### `.github/workflows/auto-readme.yml`
This GitHub Actions workflow is the central orchestrator for the automated README update process.

*   **Trigger:** The workflow is configured to run automatically on every `push` event to the repository. This ensures that the `README.md` is reviewed and potentially updated whenever new code is committed.
*   **Workflow Steps:**
    1.  **Checkout Code:** The repository's content is fetched, allowing the workflow to access the latest files and historical diffs.
    2.  **Set up Python:** A Python 3.10 environment is configured, which is necessary for running the README generation script.
    3.  **Install Dependencies:** Essential Python packages, specifically `google-genai`, are installed. This library is crucial for enabling communication with the AI model used for content generation.
    4.  **Generate README:** The `script/generate_readme.py` script is executed. This script utilizes an AI model (powered by an `AI_API_KEY` securely passed as an environment variable) to analyze recent code changes and generate or update the `README.md` content based on these modifications.
    5.  **Commit and Push Changes:** After the README generation, this step checks if the `README.md` file has been modified. If changes are detected, the workflow automatically commits the updated file with a standardized message ("docs: auto-updated README") and pushes these changes back to the repository, effectively updating the documentation.
*   **Permissions:** The workflow requires `contents: write` permission to be able to successfully commit and push changes back to the repository.
>>>>>>> 18d39b38fa041e555faab791ac35852565d18746
