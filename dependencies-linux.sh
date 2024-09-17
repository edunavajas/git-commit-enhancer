#!/bin/bash

set -e

echo "Updating package list..."
sudo apt update

# Install dependencies for pyenv and building Python
echo "Installing dependencies..."
sudo apt install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

# For Fedora:
# sudo dnf install -y make gcc zlib-devel bzip2 bzip2-devel readline-devel \
# sqlite sqlite-devel openssl-devel tk-devel libffi-devel xz-devel

# For CentOS/RHEL:
# sudo yum install -y make gcc zlib-devel bzip2 bzip2-devel readline-devel \
# sqlite sqlite-devel openssl-devel tk-devel libffi-devel xz-devel

# For Arch Linux:
# sudo pacman -Sy --noconfirm base-devel openssl zlib xz tk libffi


# Install pyenv if not installed
if ! command -v pyenv &> /dev/null; then
    echo "Installing pyenv..."
    curl https://pyenv.run | bash
else
    echo "pyenv is already installed."
fi

# Add pyenv to PATH and initialize it
if ! grep -q 'export PYENV_ROOT="$HOME/.pyenv"' ~/.bashrc; then
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    echo -e 'eval "$(pyenv init --path)"' >> ~/.bashrc
    source ~/.bashrc
fi

echo "Installing Python 3.12.5..."
pyenv install 3.12.5

pyenv global 3.12.5

echo "Creating a virtual environment named 'myenv'..."
pyenv virtualenv 3.12.5 myenv

echo "Activating the virtual environment 'myenv'..."
pyenv activate myenv

echo "Installing google-generativeai package..."
pip install google-generativeai

echo "Script completed. The 'google-generativeai' package is installed in the virtual environment 'myenv'."
