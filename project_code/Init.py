#!/usr/bin/env python3

import os
import subprocess
import sys
import argparse
import google.generativeai as genai
from dotenv import load_dotenv
import logging

load_dotenv()

# Initial Gemini configuration
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
DEFAULT_MODEL = 'gemini-1.5-flash'
logging.basicConfig(filename='/tmp/commit-msg-hook.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

model = genai.GenerativeModel(DEFAULT_MODEL) 

# Prompt template (easily modifiable)
PROMPT_TEMPLATE = """Improve the following commit message while preserving its original intent. If the message is in Spanish, translate it to English. Follow the Conventional Commits rules:
    - Use feat: for new features and fix: for bug fixes.
    - Use BREAKING CHANGE: in the footer or a ! after the type/scope for breaking changes.
    - Additional types like build:, chore:, ci:, docs:, style:, refactor:, perf:, and test: are allowed.
    - Optionally, include a scope within parentheses after the type to provide additional context (e.g., feat(parser):).
    - The commit message should be clear, concise, and follow these conventions strictly.
    - Correct any spelling or grammar mistakes, and add verbs or any necessary elements to enhance clarity and professionalism.
    - **Do not add any kind of quotes, backticks (`), or characters around the message, respond only with the string of the message itself.**

    Commit message: {commit_message}
"""

def get_commit_message_from_args(args):
    """Gets the commit message from the arguments provided."""
    if "-m" in args:
        index = args.index("-m") + 1
        if index < len(args):
            return args[index]
    return None

def get_git_diff():
    """Gets code changes using git diff."""
    try:
        diff_output = subprocess.check_output(['git', 'diff', '--staged'], text=True)
        return diff_output.strip()
    except subprocess.CalledProcessError as e:
        logging.error(f"Error getting git diff: {e}")
        return ""

def build_prompt(commit_message, include_diff=False):
    """Generates the prompt to send to Gemini."""
    prompt = PROMPT_TEMPLATE.format(commit_message=commit_message)
    
    if include_diff:
        logging.info(f"Include diff true")
        git_diff = get_git_diff()
        if git_diff:
            prompt += f"\n\nGit Diff (context of the changes):\n{git_diff}"

    logging.info(f"Prompt generated: {prompt}")
    return prompt

def modify_commit_message(commit_message, use_diff=False):
    """Sends the commit message to the Gemini API for modification."""
    logging.info("Sending commit message to Gemini for modification...")
    original_message = commit_message
    try:
        prompt = build_prompt(commit_message, use_diff)
        response = model.generate_content(prompt)
        modified_message = response.text.strip() if response and response.text else commit_message
        logging.info(f"Modified message: {modified_message}")
        return modified_message
    except Exception as e:
        logging.error(f"Error using the Gemini model: {e}")
        return original_message

def init():
    # Argument parser for the flag and commit message file
    parser = argparse.ArgumentParser(description='Pre-commit hook script.')
    parser.add_argument('commit_file', help='Path to the commit message file.') 
    parser.add_argument('--use-diff', action='store_true', help='Include git diff in the prompt sent to Gemini.')
    args = parser.parse_args()

    try:
        with open(args.commit_file, 'r') as f:
            commit_message = f.read().strip()
    except FileNotFoundError:
        logging.error(f"Could not find the file: {args.commit_file}")
        sys.exit(1)

    use_git_diff = os.getenv("USE_GIT_DIFF", "false").lower() == "true"
    
    if args.use_diff:
        use_git_diff = True

    modified_message = modify_commit_message(commit_message, use_diff=use_git_diff)

    with open(args.commit_file, 'w') as f:
        f.write(modified_message)

def handle_interrupt(signal, frame):
    """Handles Ctrl+C interrupt."""
    print("\nCtrl+C pressed! Exiting...")
    clear_screen()
    sys.exit(0)  

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    init()