# Automated GitHub README Generator 🤖📝

An automated CI/CD pipeline that uses the official Google GenAI SDK and Gemini API (`gemini-2.5-flash`) to dynamically document your project. Whenever you push Python (`.py`) or Jupyter Notebook (`.ipynb`) files to GitHub, the pipeline automatically updates or appends file documentation to your `README.md` in real-time.

---

## 🚀 How it Works
1. **GitHub Action Trigger**: The workflow monitors the repository and triggers automatically on a `push` containing `.py` or `.ipynb` file changes.
2. **Code Extraction**: The script reads the updated code. For Jupyter Notebooks, it parses the file using standard JSON tools and strips out complex cell and notebook metadata, extracting only code and markdown.
3. **Gemini API Analysis**: The file content is analyzed by the Gemini model alongside the existing `README.md`.
4. **Style-Preserving Commit**: The bot appends a contextually relevant section explaining the new files at the bottom, matching the existing document's tone, styling, and formatting, and commits it back to the branch.

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

You can test the generation script locally before pushing to GitHub.

1. Ensure the Google GenAI SDK is installed:
   ```bash
   pip install google-genai
   ```
2. Export your Gemini API Key:
   ```bash
   export GEMINI_API_KEY="your-gemini-api-key"
   ```
3. Run the script:
   ```bash
   python3 script/generate_readme.py
   ```
   *(Note: The script compares the latest commit with its parent using git. To run a dry-run test, commit your python/notebook files first!)*
