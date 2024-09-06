<div align="center">
  <br />
      <img src="https://raw.githubusercontent.com/edunavajas/git-commit-enhancer/main/img/header.png" alt="Project Header">
  <br />
 </div>


# Automated Git Commit Hook with Gemini Integration

This project provides an automated Git hook that improves every commit message using Gemini AI. It automatically updates your commit messages before they are applied to the repository. The script requires a Gemini API key, which you need to store in a `.env` file as an environment variable named `GEMINI_API_KEY`.

## Setup

To use this hook, follow the steps below.

### Prerequisites

1. You need to have Python installed on your system.
2. You must have an API key for Gemini AI. Store this key in a `.env` file located in the root directory of the project:
    ```
    GEMINI_API_KEY=your_gemini_api_key_here
    ```

### Automatic Setup

To automatically set up the hook for your Git repositories, clone the project and run the following commands:

```bash
chmod +x setup_hooks.py
./setup_hooks.py
```

The script will ask you where your Git projects are located. It will then configure the Git hooks for all the projects in that directory. Any new repositories you clone will have the hook applied automatically.

### Manual Setup

If you prefer to set up the hook manually, follow these steps:

1.	Create a Global Hooks Directory:

```bash
    mkdir -p ~/.git-templates/hooks
```    

2. Configure Git to Use the Global Hooks Template:


```bash
git config --global init.templateDir '~/.git-templates'
```
3. Create the commit-msg Hook in the Global Hooks Directory:


```bash
nano ~/.git-templates/hooks/commit-msg
```

4. Add the Hook Script:

Copy the following script into the commit-msg file. This script will invoke a Python script that uses Gemini AI to enhance your commit messages.

```bash
#!/bin/bash
# commit-msg hook script

# Path to your Python script
SCRIPT_PATH="/path/to/Main.py"

# Temporary file that contains the commit message
COMMIT_MSG_FILE="$1"

# Read the message from the temporary file
COMMIT_MSG=$(<"$COMMIT_MSG_FILE")

# Call the Python script with the commit message
MODIFIED_MSG=$(python3 "$SCRIPT_PATH" --message "$COMMIT_MSG" --test)

# If the Python script returned a modified message, replace it in the temporary file
if [ "$COMMIT_MSG" != "$MODIFIED_MSG" ]; then
    echo "$MODIFIED_MSG" > "$COMMIT_MSG_FILE"
fi
```

5. Make the Hook Executable:

```bash
chmod +x ~/.git-templates/hooks/commit-msg
```

6. Apply the Hook to Existing Repositories:

To apply this hook to existing Git repositories, copy the commit-msg file to the .git/hooks/ directory of each repository:

```bash
cp ~/.git-templates/hooks/commit-msg /path/to/your/repository/.git/hooks/
```

### Usage
Once the hook is set up, it will automatically enhance your commit messages using Gemini AI every time you commit changes. Simply use Git as you normally would, and the commit messages will be updated before being applied to the repository.

```bash
git commit -m "your commit message"
```

Gemini will process the commit message, improve it, and apply the changes to the commit automatically.

### Notes
Make sure the .env file with your GEMINI_API_KEY is present in the root directory of the project before running the hook.
You can manually run the Python script Main.py if needed to test or debug any issues with commit messages.
