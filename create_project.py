#!/usr/bin/env python3
"""
Automated Project Creator from GitHub Template with Token Auth
"""

import os
import subprocess
import shutil
from dotenv import load_dotenv

def load_github_token(env_path: str) -> str:
    """Load GitHub token from a .env file."""
    load_dotenv(dotenv_path=env_path)
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN not found in .env file.")
    return token

def clone_template_repo(github_url: str, temp_dir: str, token: str):
    """Clone the template repository using token authentication."""
    # Transform https://github.com/youruser/repo.git into https://<token>@github.com/youruser/repo.git
    secure_url = github_url.replace("https://", f"https://{token}@")
    print(f"Cloning template from {github_url}...")
    subprocess.run(["git", "clone", secure_url, temp_dir], check=True)

def rename_project(temp_dir: str, new_project_name: str):
    """Rename project inside the cloned template."""
    # Rename the directory
    if not os.path.exists(new_project_name):
        shutil.move(temp_dir, new_project_name)
    else:
        raise FileExistsError(f"Directory {new_project_name} already exists!")

    # Update placeholders
    files_to_update = [
        os.path.join(new_project_name, "README.md"),
        os.path.join(new_project_name, "pyproject.toml"),
        os.path.join(new_project_name, "src", "main.py"),
        os.path.join(new_project_name, "tests", "test_main.py")
    ]

    for file_path in files_to_update:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            content = content.replace("your_project_name", new_project_name)
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)

    print(f"Project renamed successfully to {new_project_name}.")

def main():
    """Main function."""
    env_file_path = os.path.expanduser("~/GitHub/.env")
    github_template_url = input("Enter your GitHub template repository URL: ").strip()
    new_project_name = input("Enter your new project name: ").strip()
    temp_dir = "temp_project_template"

    try:
        token = load_github_token(env_file_path)
        clone_template_repo(github_template_url, temp_dir, token)
        rename_project(temp_dir, new_project_name)
        print(f"✅ Project '{new_project_name}' created successfully.")
        print(f"➡️ Next steps:")
        print(f"   cd {new_project_name}")
        print(f"   python -m venv venv")
        print(f"   source venv/bin/activate")
        print(f"   pip install .")
    except Exception as e:
        print(f"❌ Error: {e}")
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

if __name__ == "__main__":
    main()
