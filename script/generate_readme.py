#!/usr/bin/env python3
import os
import sys
import subprocess
import json

try:
    from google import genai
except ImportError:
    genai = None


def get_changed_files():
    """
    Get a list of modified or added files in the latest commit.
    Falls back to listing all files in the repository if git diff fails.
    """
    # 1. Try git diff HEAD~1 HEAD
    try:
        res = subprocess.run(
            ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        files = res.stdout.splitlines()
        return [f.strip() for f in files if f.strip()]
    except Exception:
        pass

    # 2. Try git show HEAD
    try:
        res = subprocess.run(
            ["git", "show", "--name-only", "--pretty=format:", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        files = res.stdout.splitlines()
        return [f.strip() for f in files if f.strip()]
    except Exception:
        pass

    # 3. Try git ls-files
    try:
        res = subprocess.run(
            ["git", "ls-files"], capture_output=True, text=True, check=True
        )
        files = res.stdout.splitlines()
        return [f.strip() for f in files if f.strip()]
    except Exception:
        pass

    # 4. Fallback to recursive directory walk
    files = []
    exclude_dirs = {".git", ".github", "__pycache__", "venv", ".venv", "node_modules"}
    for root, dirs, filenames in os.walk("."):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for filename in filenames:
            rel_path = os.path.relpath(os.path.join(root, filename), ".")
            files.append(rel_path)
    return files


def parse_ipynb(filepath):
    """
    Parse Jupyter Notebook files to extract code and markdown cells,
    stripping complex cell and file metadata.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        content = []
        cells = data.get("cells", [])
        for idx, cell in enumerate(cells):
            cell_type = cell.get("cell_type")
            source = cell.get("source", "")
            if isinstance(source, list):
                source = "".join(source)

            if cell_type == "markdown":
                content.append(f"### Cell {idx} (Markdown):\n{source.strip()}\n")
            elif cell_type == "code":
                content.append(
                    f"### Cell {idx} (Code):\n```python\n{source.strip()}\n```\n"
                )
        return "\n".join(content)
    except Exception as e:
        print(f"Error parsing notebook {filepath}: {e}", file=sys.stderr)
        return ""


def get_all_files():
    """
    Get a list of all files in the repository.
    """
    # 1. Try git ls-files
    try:
        res = subprocess.run(
            ["git", "ls-files"],
            capture_output=True,
            text=True,
            check=True
        )
        files = res.stdout.splitlines()
        return [f.strip() for f in files if f.strip()]
    except Exception:
        pass

    # 2. Fallback to recursive directory walk
    files = []
    exclude_dirs = {".git", ".github", "__pycache__", "venv", ".venv", "node_modules"}
    for root, dirs, filenames in os.walk("."):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for filename in filenames:
            rel_path = os.path.relpath(os.path.join(root, filename), ".")
            files.append(rel_path)
    return files


def read_file_content(filepath):
    """
    Safely reads any file content. If it is a notebook, parses cells.
    If it is a generic file, checks size constraints and decodes safely.
    """
    if filepath.endswith(".ipynb"):
        return parse_ipynb(filepath)

    try:
        # Avoid reading large files (limit to 1MB)
        if os.path.getsize(filepath) > 1024 * 1024:
            return "[Large File: Content omitted from prompt]"
            
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            # Check for null bytes which usually indicate a binary file
            if '\x00' in content:
                return "[Binary/Non-text File]"
            return content
    except Exception as e:
        print(f"Error reading file {filepath}: {e}", file=sys.stderr)
        return f"[Unreadable File: {e}]"


def main():
    # Retrieve API key
    api_key = os.environ.get("AI_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print(
            "Error: Neither AI_API_KEY nor GEMINI_API_KEY environment variable is set.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Check if we should do a full scan of all repository files
    force_all = "--all" in sys.argv
    readme_path = "README.md"
    readme_exists = os.path.exists(readme_path)

    if force_all or not readme_exists:
        if force_all:
            print("Force flag '--all' detected. Scanning all files in the repository...")
        else:
            print("README.md does not exist. Performing initial scan of all files in the repository...")
        all_files = get_all_files()
    else:
        print("Scanning for changed files in the last commit...")
        all_files = get_changed_files()

    # Document all files, excluding workflows, hidden files/dirs, and the generator script
    exclude_prefixes = ('.git', '.github', 'script/', 'README.md', 'instructions.md')
    target_files = [
        f for f in all_files 
        if not any(f.startswith(p) for p in exclude_prefixes)
    ]

    if not target_files:
        print("No documentable files modified or added in this commit.")
        sys.exit(0)

    print(f"Found target files to document: {target_files}")

    # Read existing README.md
    existing_readme = ""
    readme_path = "README.md"
    if os.path.exists(readme_path):
        try:
            with open(readme_path, "r", encoding="utf-8") as f:
                existing_readme = f.read()
            print("Existing README.md loaded.")
        except Exception as e:
            print(f"Warning: Could not read existing README.md: {e}", file=sys.stderr)
    else:
        print("No existing README.md found. A new one will be created.")

    # Extract contents from the target files
    files_content_summary = []
    for filepath in target_files:
        if not os.path.exists(filepath):
            print(f"File {filepath} no longer exists. Skipping.")
            continue

        print(f"Extracting content from {filepath}...")
        content = read_file_content(filepath)

        if content.strip():
            files_content_summary.append(f"### File: {filepath}\n\n```\n{content}\n```")

    if not files_content_summary:
        print(
            "All target files are empty or could not be parsed. Exiting without updating README."
        )
        sys.exit(0)

    # Build files content representation
    files_content_str = "\n\n---\n\n".join(files_content_summary)

    # Initialize Gemini Client
    if genai is None:
        print(
            "Error: 'google-genai' SDK is not installed. Please run 'pip install google-genai'.",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        print(f"Error initializing Gemini client: {e}", file=sys.stderr)
        sys.exit(1)

    # Construct the AI prompt
    prompt = f"""You are an automated README generator bot. Your task is to update the repository's README.md by documenting the newly added or modified files.

Here is the existing README.md content (it might be empty or missing):
--- EXISTING README.MD START ---
{existing_readme}
--- EXISTING README.MD END ---

Here are the details and contents of the new/modified files in this commit:
{files_content_str}

Strict instructions:
1. Analyze the new code files.
2. Do not rewrite, alter, or delete any existing content of the README.md.
3. Append a new, contextually relevant section explaining the new/modified files at the bottom of the README.md.
4. Mirror the exact same markdown style, headers, and linguistic tone as the existing document.
5. If there is no existing README.md (or if it is empty), write a comprehensive README.md from scratch, including a clear title, description, and sections documenting the files.
6. Return ONLY the final, complete README.md content. Do not include markdown code block backticks (like ```markdown ... ```) around the entire output; output raw markdown text ready to be written to a file.
"""

    import time
    max_retries = 3
    delay = 2
    backoff_factor = 2
    response = None

    for attempt in range(max_retries):
        try:
            print(f"Calling Gemini API to generate README update (Attempt {attempt + 1}/{max_retries})...")
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            new_readme_content = response.text
            if not new_readme_content or not new_readme_content.strip():
                raise ValueError("Empty response returned from the Gemini API.")
            break
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"Error calling Gemini API after {max_retries} attempts: {e}", file=sys.stderr)
                sys.exit(1)
            print(f"API call failed: {e}. Retrying in {delay} seconds...", file=sys.stderr)
            time.sleep(delay)
            delay *= backoff_factor


    # Overwrite/write the README.md file
    try:
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(new_readme_content.strip() + "\n")
        print("README.md has been successfully updated.")
    except Exception as e:
        print(f"Error writing README.md: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
