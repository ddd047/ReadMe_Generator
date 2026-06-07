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
