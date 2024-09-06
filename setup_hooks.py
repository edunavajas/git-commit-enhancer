#!/usr/bin/env python3

import os
import shutil
import subprocess
import stat
import sys

# Define the content of the commit-msg hook
COMMIT_MSG_HOOK_CONTENT = '''#!/bin/bash
# Commit-msg hook script that modifies the commit message using a Python script

# Path to your Python script
SCRIPT_PATH="{main_py_path}"

# Path to the Python interpreter inside the virtual environment
PYTHON_BIN="/Users/eduardo.navajas/.pyenv/versions/3.12.5/envs/entorno/bin/python"

# Get the commit message file (Git passes it as an argument)
COMMIT_MSG_FILE="$1"

# Log the current step for debugging
echo "Running commit-msg hook" > /tmp/commit-msg-hook.log
echo "Commit message file: $COMMIT_MSG_FILE" >> /tmp/commit-msg-hook.log
echo "Using Python binary at: $PYTHON_BIN" >> /tmp/commit-msg-hook.log

# Log the Python path
$PYTHON_BIN --version >> /tmp/commit-msg-hook.log

# Run the Python script to modify the commit message using the specific Python interpreter
$PYTHON_BIN "$SCRIPT_PATH" "$COMMIT_MSG_FILE" 2>> /tmp/commit-msg-hook.log

# Log the result
echo "Commit message hook completed." >> /tmp/commit-msg-hook.log
'''


def make_executable(path):
    """Make a file executable."""
    st = os.stat(path)
    os.chmod(path, st.st_mode | stat.S_IEXEC)

def create_commit_msg_hook(hook_dest_path, main_py_path):
    """Create the commit-msg hook file with the appropriate content."""
    # Fill in the main.py path in the hook content
    hook_content = COMMIT_MSG_HOOK_CONTENT.format(main_py_path=main_py_path)

    # Write the content to the commit-msg file
    with open(hook_dest_path, 'w') as hook_file:
        hook_file.write(hook_content)
    
    # Make the hook file executable
    make_executable(hook_dest_path)

    print(f"commit-msg hook created at {hook_dest_path}")

def setup_global_hook(main_py_path):
    """Setup the global Git template for hooks and create commit-msg."""
    # Step 1: Create the ~/.git-templates/hooks directory
    global_hooks_dir = os.path.expanduser("~/.git-templates/hooks")
    os.makedirs(global_hooks_dir, exist_ok=True)

    # Step 2: Configure Git to use the template directory
    subprocess.run(["git", "config", "--global", "init.templateDir", "~/.git-templates"], check=True)
    print(f"Global Git template directory set to {global_hooks_dir}")

    # Step 3: Create the commit-msg hook in the global hooks directory
    global_commit_msg_path = os.path.join(global_hooks_dir, "commit-msg")
    create_commit_msg_hook(global_commit_msg_path, main_py_path)

def setup_hook_in_repo(repo_path, global_commit_msg_path):
    """Copy the global commit-msg hook to a given repository."""
    git_hooks_path = os.path.join(repo_path, ".git", "hooks")

    # Check if the .git/hooks folder exists
    if not os.path.exists(git_hooks_path):
        print(f"Warning: No .git folder found in {repo_path}. Skipping this repository.")
        return

    # Copy the global commit-msg file to the repository
    hook_dest_path = os.path.join(git_hooks_path, "commit-msg")
    shutil.copy(global_commit_msg_path, hook_dest_path)

    # Make the hook file executable
    make_executable(hook_dest_path)

    print(f"commit-msg hook applied to {repo_path}")

def find_git_repos(root_dir):
    """Find all git repositories within a given directory."""
    git_repos = []
    for dirpath, _, _ in os.walk(root_dir):
        if os.path.exists(os.path.join(dirpath, ".git")):
            git_repos.append(dirpath)
    return git_repos

def main():
    # Get the path to Main.py in the current working directory
    current_dir = os.getcwd()
    main_py_path = os.path.join(current_dir, "Main.py")

    if not os.path.exists(main_py_path):
        print(f"Error: Main.py not found at {main_py_path}")
        sys.exit(1)

    # Step 1: Setup the global commit-msg hook
    setup_global_hook(main_py_path)

    # Get the global commit-msg hook path
    global_commit_msg_path = os.path.expanduser("~/.git-templates/hooks/commit-msg")

    # Step 2: Ask the user for the path where the repositories are located
    root_dir = input("Enter the path where the repositories are located: ")

    if not os.path.exists(root_dir):
        print(f"Error: The provided path does not exist: {root_dir}")
        sys.exit(1)

    # Step 3: Find all git repositories in the provided path
    git_repos = find_git_repos(root_dir)

    if not git_repos:
        print(f"No git repositories found in {root_dir}")
        sys.exit(1)

    # Step 4: Apply the global commit-msg hook to each repository found
    for repo in git_repos:
        setup_hook_in_repo(repo, global_commit_msg_path)

    print("Process completed.")

if __name__ == "__main__":
    main()