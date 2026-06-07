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
