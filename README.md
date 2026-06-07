<<<<<<< HEAD
# Auto README Updater

This repository demonstrates an automated system for keeping your `README.md` file up-to-date using GitHub Actions and an AI-powered script.

## How it Works

The core of this system is a GitHub Actions workflow that automatically triggers a README generation process whenever specific file types are pushed to the repository. This ensures that documentation remains fresh and reflects the latest changes without manual intervention.

## Files

### `auto-readme.yml`

This GitHub Actions workflow file (`.github/workflows/auto-readme.yml`) defines the automation pipeline for updating the `README.md`.

*   **Trigger**: The workflow is configured to run automatically on `push` events that involve changes to Python (`.py`) or Jupyter Notebook (`.ipynb`) files.
*   **Permissions**: It's granted `contents: write` permissions, which is essential for the action to be able to commit and push the updated `README.md` back to the repository.
*   **Steps**:
    *   **Checkout Code**: Fetches the repository code, including recent history for change detection.
    *   **Set up Python**: Configures the environment with Python 3.10.
    *   **Install Dependencies**: Installs necessary Python packages, specifically `google-genai`, indicating that the README generation leverages an AI model.
    *   **Generate README**: Executes a Python script (`script/generate_readme.py`) which is responsible for analyzing the repository's changes and generating the new README content. This step requires an `AI_API_KEY` secret for authentication with the AI service.
    *   **Commit and Push Changes**: If the `generate_readme.py` script produces changes to `README.md`, this step stages, commits, and pushes the updated file back to the repository. It uses a dedicated "ReadmeBot" user for clarity in commit history.
=======
# Automated GitHub README Generator 🤖📝

An automated CI/CD pipeline that uses the official Google GenAI SDK and Gemini API (`gemini-2.5-flash`) to dynamically document your project. Whenever you push files to GitHub, the pipeline automatically updates or appends file documentation to your `README.md` in real-time.

---

## 🚀 How it Works
1. **GitHub Action Trigger**: The workflow monitors the repository and triggers automatically on **any** push event.
2. **Scan Strategy**: 
   - **Initial / Empty Setup**: If `README.md` is missing (or if you run with the `--all` flag), the script does a **full repository sweep** to document all existing files from scratch.
   - **Incremental Updates**: If a `README.md` already exists, the script reads it and only scans the files modified or added in the **most recent commit** to document incremental changes.
3. **Safe File Extraction**: The script reads files securely:
   - For Jupyter Notebooks (`.ipynb`), it extracts code and markdown cells while discarding heavy metadata.
   - For generic files, it limits payload sizes (skips files > 1MB) and handles binary/non-text files safely (checking for null bytes) to keep prompts clean.
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
>>>>>>> 88cea93 (readme updated)
