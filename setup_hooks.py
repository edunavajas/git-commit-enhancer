#!/usr/bin/env python3

import os
import shutil
import subprocess
import stat
import sys
import platform

# Function to make a file executable
def make_executable(path):
    """Make a file executable."""
    st = os.stat(path)
    os.chmod(path, st.st_mode | stat.S_IEXEC)

# Function to create the commit-msg hook
def create_commit_msg_hook(hook_dest_path, main_py_path):
    """Create the commit-msg hook file with the appropriate content."""
    # Get the current Python interpreter path
    python_bin = sys.executable

    if platform.system() == 'Windows':
        # Windows commit-msg hook (batch script)
        hook_content = f'''@echo off
rem Commit-msg hook script that modifies the commit message using a Python script

rem Path to your Python script
set SCRIPT_PATH="{main_py_path}"

rem Get the commit message file (Git passes it as an argument)
set COMMIT_MSG_FILE=%1

rem Run the Python script to modify the commit message using the specific Python interpreter
"{python_bin}" "%SCRIPT_PATH%" "%COMMIT_MSG_FILE%"
'''
    else:
        # Unix commit-msg hook (bash script)
        hook_content = f'''#!/bin/bash
# Commit-msg hook script that modifies the commit message using a Python script

# Path to your Python script
SCRIPT_PATH="{main_py_path}"

# Path to the Python interpreter
PYTHON_BIN="{python_bin}"

# Get the commit message file (Git passes it as an argument)
COMMIT_MSG_FILE="$1"

# Run the Python script to modify the commit message using the specific Python interpreter
"$PYTHON_BIN" "$SCRIPT_PATH" "$COMMIT_MSG_FILE"
'''
    # Write the content to the commit-msg file
    with open(hook_dest_path, 'w') as hook_file:
        hook_file.write(hook_content)
        
    # Make the hook file executable (on Unix)
    if platform.system() != 'Windows':
        make_executable(hook_dest_path)
    
    print(f"commit-msg hook created at {hook_dest_path}")

# Function to set up the global hook
def setup_global_hook(main_py_path):
    """Setup the global Git template for hooks and create commit-msg."""
    # Create the ~/.git-templates/hooks directory
    global_hooks_dir = os.path.expanduser("~/.git-templates/hooks")
    os.makedirs(global_hooks_dir, exist_ok=True)

    # Configure Git to use the template directory
    subprocess.run(["git", "config", "--global", "init.templateDir", "~/.git-templates"], check=True)
    print(f"Global Git template directory set to {global_hooks_dir}")

    # Create the commit-msg hook in the global hooks directory
    if platform.system() == 'Windows':
        global_commit_msg_path = os.path.join(global_hooks_dir, "commit-msg.cmd")
    else:
        global_commit_msg_path = os.path.join(global_hooks_dir, "commit-msg")
    create_commit_msg_hook(global_commit_msg_path, main_py_path)
    return global_commit_msg_path

# Function to set up the hook in a repository
def setup_hook_in_repo(repo_path, global_commit_msg_path):
    """Copy the global commit-msg hook to a given repository."""
    git_hooks_path = os.path.join(repo_path, ".git", "hooks")

    # Check if the .git/hooks folder exists
    if not os.path.exists(git_hooks_path):
        print(f"Warning: No .git folder found in {repo_path}. Skipping this repository.")
        return

    if platform.system() == 'Windows':
        hook_dest_path = os.path.join(git_hooks_path, "commit-msg.cmd")
    else:
        hook_dest_path = os.path.join(git_hooks_path, "commit-msg")

    # Copy the global commit-msg file to the repository
    shutil.copy(global_commit_msg_path, hook_dest_path)

    # Make the hook file executable (on Unix)
    if platform.system() != 'Windows':
        make_executable(hook_dest_path)

    print(f"commit-msg hook applied to {repo_path}")

# Function to find all Git repositories in a directory
def find_git_repos(root_dir):
    """Find all git repositories within a given directory."""
    git_repos = []
    for dirpath, dirnames, _ in os.walk(root_dir):
        if '.git' in dirnames:
            git_repos.append(dirpath)
            # Do not traverse into subdirectories once a git repo is found
            dirnames[:] = []
    return git_repos

# Main function
def main():
    # Get the path to Main.py in the current working directory
    current_dir = os.getcwd()
    main_py_path = os.path.join(current_dir, "Main.py")

    if not os.path.exists(main_py_path):
        print(f"Error: Main.py not found at {main_py_path}")
        sys.exit(1)

    # Setup the global commit-msg hook
    global_commit_msg_path = setup_global_hook(main_py_path)

    # Ask the user for the path where the repositories are located
    root_dir = input("Enter the path where the repositories are located: ")

    if not os.path.exists(root_dir):
        print(f"Error: The provided path does not exist: {root_dir}")
        sys.exit(1)

    # Find all git repositories in the provided path
    git_repos = find_git_repos(root_dir)

    if not git_repos:
        print(f"No git repositories found in {root_dir}")
        sys.exit(1)

    # Apply the global commit-msg hook to each repository found
    for repo in git_repos:
        setup_hook_in_repo(repo, global_commit_msg_path)

    print("Process completed.")

if __name__ == "__main__":
    main()