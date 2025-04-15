#!/bin/bash

# ============================================
# Locator3.sh
# ============================================
# Description:
# This script searches for a given folder name starting from the root of the C: drive
# (useful in Git Bash on Windows), changes into that directory, and then runs an 
# Ionic app using npm.

# Usage:
# In Git Bash, run:
#     source Locator3.sh <folder_name>
# Example:
#     source Locator3.sh imagegallery
#
# Notes:
# - 'source' is used so that the directory change persists in the current shell.
# - Requires Git Bash, npm, and Ionic CLI installed and properly configured.

# --------------------------------------------
# Check if a folder name argument is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <folder_name>"
    exit 1
fi

FOLDER_NAME=$1

# --------------------------------------------
# Define the search root path (C drive in Git Bash)
SEARCH_PATH="/c/"
echo "Searching for '$FOLDER_NAME' in $SEARCH_PATH..."

# --------------------------------------------
# Search for the folder and grab the first match
FOLDER_PATH=$(find "$SEARCH_PATH" -type d -name "$FOLDER_NAME" 2>/dev/null | head -n 1)

# --------------------------------------------
# Handle case when folder is not found
if [ -z "$FOLDER_PATH" ]; then
    echo "Folder '$FOLDER_NAME' not found."
    exit 1
fi

echo "Folder found at: $FOLDER_PATH"

# --------------------------------------------
# Attempt to change to the found folder
cd "$FOLDER_PATH" || {
    echo "Failed to change directory to $FOLDER_PATH"
    exit 1
}

echo "Successfully changed directory to $FOLDER_PATH"

# --------------------------------------------
# Run the Ionic application
# '--host=0.0.0.0' allows access from other devices on the network (optional)
# '--port=8100' specifies the development server port
# '--project=app' specifies which project to run (if multiple projects exist)
npm.cmd run ionic:serve -- --host=0.0.0.0 --port=8100 --project=app
