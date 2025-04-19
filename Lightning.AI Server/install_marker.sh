#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Define the repository URL and the target directory
REPO_URL="https://github.com/VikParuchuri/marker.git"
CLONE_DIR="/teamspace/studios/this_studio/marker" 

# Ensure the parent directory exists
PARENT_DIR=$(dirname "$CLONE_DIR")
if [ ! -d "$PARENT_DIR" ]; then
    echo "Creating parent directory: $PARENT_DIR"
    mkdir -p "$PARENT_DIR"
fi

# Clone the repository if it doesn't already exist
if [ ! -d "$CLONE_DIR" ]; then
    echo "Cloning repository into $CLONE_DIR..."
    git clone "$REPO_URL" "$CLONE_DIR"
else
    echo "Repository already cloned. Pulling latest changes..."
    pushd "$CLONE_DIR"
    git pull
    popd
fi

# Navigate to the cloned repository
pushd "$CLONE_DIR"

# Install the library
echo "Installing the library..."
pip install .

# Return to the original directory
popd

echo "Library installed successfully!"
