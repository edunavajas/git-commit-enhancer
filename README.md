<div align="center">
  <br />
      <img src="https://raw.githubusercontent.com/edunavajas/git-commit-enhancer/main/img/header.png" alt="Project Header">
  <br />
 </div>

 # 📋 <a name="table">Table of Contents</a>

1. 🤖 [Introduction](#introduction)
2. ⚙️ [Dependencies installation for Mac Os](#dependencies)
3  ⚙️ [Dependencies installation for Linux](#dependencies-linux)
3  ⚙️ [Dependencies installation for Windows](#dependencies-windows)
3. 🦾 [Project setup](#setup)


# <a name="introduction">🤖 Automated Git Commit Hook with Gemini Integration</a>

> ⚠️ **Warning**: This project is primarily configured for macOS. However, configurations have been adapted for Linux and Windows. If you encounter any issues or errors, feel free to report them in the issues section or submit a pull request.

This project provides an automated Git hook that improves every commit message using Gemini AI. It automatically updates your commit messages before they are applied to the repository. The script requires a Gemini API key, which you need to store in a `.env` file as an environment variable named `GEMINI_API_KEY`.

# <a name="dependencies">⚙️ Dependencies MacOs</a>

## Atomatic installation for MacOs


To automatically set up pyhton env and dependencies run this script:

```bash
chmod +x dependencies-macos.sh
./dependencies-macos.sh
```
Now you can go 👉 (🦾 [Project setup](#setup))

## Manual installation for MacOs

This guide walks you through the manual steps required to set up a Python environment on macOS using `pyenv`, install Python version 3.12.5, create a virtual environment, and install the `google-generativeai` package.

### Prerequisites 

Make sure you have the following installed:
- **Homebrew** (If not, follow the instructions in Step 1)
- **pyenv**

### Steps

1. Install Homebrew (if not installed)

Homebrew is required to install pyenv. To check if Homebrew is installed, open a terminal and run:

```bash
brew --version
```

If Homebrew is not installed, you can install it by running the following command in your terminal:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. Install pyenv

Check if pyenv is installed by running:

```bash
pyenv --version
```

If pyenv is not installed, install it using Homebrew:

```bash
brew update
brew install pyenv
```

3. Configure pyenv

To ensure pyenv works properly, you need to add it to your shell’s environment variables. Add the following lines to your ~/.bash_profile (or ~/.zshrc if you’re using Zsh):

```bash
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
```

After adding these lines, apply the changes by running:

```bash
source ~/.bash_profile  # or ~/.zshrc for Zsh users
```

4. Install Python 3.12.5 (current newer version)

Now that pyenv is set up, you can install the specific version of Python (3.12.5 in this case) by running:
```bash
pyenv install 3.12.5
```

5. Set Python 3.12.5 as the Global Version
```bash
pyenv global 3.12.5
```

6. Create a Virtual Environment

With Python 3.12.5 installed, create a virtual environment (in this example, we’ll call it myenv):
```bash
pyenv virtualenv 3.12.5 myenv
```

7. Activate the Virtual Environment
```bash
pyenv activate myenv
```

8. Install the google-generativeai Package
```bash
pip install google-generativeai
```

You now have a Python 3.12.5 virtual environment with the google-generativeai package installed. To deactivate the environment at any point, run:

```bash
pyenv deactivate
```
For future use, you can reactivate the environment by running:

```bash
pyenv activate myenv
```

# <a name="dependencies-linux">⚙️ Dependencies Linux</a>

## Atomatic installation for Linux

To automatically set up pyhton env and dependencies run this script:

```bash
chmod +x dependencies-linux.sh
./dependencies-linux.sh
```
In the dependency script, if there is an installation error, replace the commented installation commands with those corresponding to the correct Linux distribution you are using.

Now you can go 👉 (🦾 [Project setup](#setup))

# <a name="dependencies-windows">⚙️ Dependencies Windows</a>

## Installation for Windows

## 1. Install Python 3.12.5 on Windows

### Step 1: Download Python 3.12.5
1. Visit the official Python website: [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Find and download **Python 3.12.5** for Windows.
3. Run the installer and make sure to check the box **"Add Python 3.12 to PATH"** before proceeding with the installation.

### Step 2: Verify Installation
Once Python is installed, open a **Command Prompt (CMD)** window and run the following command to verify the installation:

```bash
python --version
```
You should see output similar to:
```
Python 3.12.5
```
## 2. Create a Virtual Environment
### Step 1: Create the Virtual Environment
In the Command Prompt (CMD) window, navigate to the directory where you want to create your virtual environment.
Run the following command to create a virtual environment named env:
```bash
python -m venv env
```

### Step 2: Activate the Virtual Environment
Once the virtual environment is created, activate it with this command:

```bash
.\env\Scripts\activate
```

## 3. Install google-generativeai Using pip
Step 1: Install google-generativeai
With the virtual environment activated, run the following command to install the required package:

```bash
pip install google-generativeai
```
This will install the necessary library in your virtual environment.

Now you can go 👉 (🦾 [Project setup](#setup))

# <a name="setup">🦾  Project setup</a>

To use this hook, follow the steps below.

## Prerequisites

1. You need to have Python installed on your system. (See ⚙️ [Dependencies installation](#dependenciesk))
2. You must have an API key for Gemini AI. Store this key in a `.env` file located in the root directory of the project:
    ```
    GEMINI_API_KEY=your_gemini_api_key_here
    ```

## Automatic Setup

To automatically set up the hook for your Git repositories, clone the project and run the following commands:

```bash
chmod +x setup_hooks.py
./setup_hooks.py
```

The script will ask you where your Git projects are located. It will then configure the Git hooks for all the projects in that directory. Any new repositories you clone will have the hook applied automatically.

## Manual Setup

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

more info here