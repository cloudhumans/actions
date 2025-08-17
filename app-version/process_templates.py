#!/usr/bin/env python3
"""
Script to process text files by replacing environment variables.
This is a Python replacement for the shell envsubst command.
"""

import os
import sys
import glob
import re
from pathlib import Path


def replace_env_vars(content):
    """
    Replace environment variables in content with their values.
    Supports both ${VAR} and $VAR formats.
    """
    # Pattern to match environment variables like ${VAR} or $VAR
    pattern = re.compile(r'\$\{([^}]+)\}|\$([a-zA-Z0-9_]+)')
    
    def replace_var(match):
        # Get the variable name, either from group 1 ${VAR} or group 2 $VAR
        var_name = match.group(1) or match.group(2)
        # Return the environment variable value or empty string if not found
        return os.environ.get(var_name, '')
    
    # Replace all occurrences of env vars
    return pattern.sub(replace_var, content)


def process_files(file_pattern):
    """
    Find all files matching the given file pattern and replace
    environment variables in them.
    """
    # Find all files using the provided pattern directly
    files = glob.glob(file_pattern, recursive=True)
    
    if not files:
        print("No files found to process")
        return
    
    print(f"Found {len(files)} files to process")
    
    for file_path in files:
        try:
            print(f"Processing: {file_path}")
            
            # Read file content
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Replace environment variables
            processed_content = replace_env_vars(content)
            
            # Write back to file
            with open(file_path, 'w') as f:
                f.write(processed_content)
                
            print(f" -> Processed: {file_path}")
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_pattern = sys.argv[1]
    else:
        file_pattern = "deploy/**/*.yaml"
    
    # Print environment variables for debugging
    print(f"Processing files matching pattern: {file_pattern}")
    print("With the following environment variables:")
    for key, value in os.environ.items():
        if key.startswith("APP_"):
            print(f"  {key}={value}")
    
    process_files(file_pattern)
