#!/bin/bash

# Exit if any command fails
set -e

# Install Homebrew if not installed
if ! command -v brew &> /dev/null; then
    echo "Homebrew is not installed. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "Homebrew is already installed."
fi

# Install pyenv if not installed
if ! command -v pyenv &> /dev/null; then
    echo "Installing pyenv..."
    brew update
    brew install pyenv
else
    echo "pyenv is already installed."
fi

# Add pyenv to PATH
if ! grep -q 'export PYENV_ROOT="$HOME/.pyenv"' ~/.bash_profile; then
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
    echo 'eval "$(pyenv init --path)"' >> ~/.bash_profile
    source ~/.bash_profile
fi

# Install Python 3.12.5
echo "Installing Python 3.12.5..."
pyenv install 3.12.5

# Set the global Python version to 3.12.5
pyenv global 3.12.5

brew install pyenv-virtualenv

# Create a virtual environment with Python 3.12.5
echo "Creating a virtual environment named 'myenv'..."
pyenv virtualenv 3.12.5 myenv

# Activate the virtual environment
echo "Activating the virtual environment 'myenv'..."
pyenv activate myenv

# Install the google-generativeai package
echo "Installing google-generativeai package..."
pip install google-generativeai
pip install python-dotenv

echo "Script completed. The 'google-generativeai' package is installed in the virtual environment 'myenv'."