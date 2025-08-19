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


_ENV_VAR_PATTERN = re.compile(r'\$\{([^}]+)\}|\$([a-zA-Z0-9_]+)')


def _resolve_env_var(match: re.Match) -> str:
    """Internal helper: return environment value or empty string."""
    var_name = match.group(1) or match.group(2)
    return os.environ.get(var_name, '')


def replace_env_vars(content: str) -> str:
    """Backward compatible wrapper returning only processed content (deprecated for counting)."""
    return _ENV_VAR_PATTERN.sub(_resolve_env_var, content)


def replace_env_vars_with_count(content: str):
    """Replace environment variables and return (processed_content, replacements_count).

    Counts every occurrence of patterns `${VAR}` or `$VAR` regardless of whether
    the variable is set. Unset variables still count as a replacement (value becomes empty).
    """
    processed, count = _ENV_VAR_PATTERN.subn(_resolve_env_var, content)
    return processed, count


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
            with open(file_path, 'r') as f:
                content = f.read()
            processed_content, count = replace_env_vars_with_count(content)
            with open(file_path, 'w') as f:
                f.write(processed_content)
            print(f" -> Processed: {file_path} (replacements: {count})")
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        patterns = sys.argv[1:]
    else:
        patterns = ["deploy/**/*.yaml"]

    print("Processing file patterns:")
    for p in patterns:
        print(f"  - {p}")

    print("With the following environment variables (APP_*):")
    for key, value in os.environ.items():
        if key.startswith("APP_"):
            print(f"  {key}={value}")

    # Collect all files from all patterns (deduplicated)
    all_files = []
    for pattern in patterns:
        matched = glob.glob(pattern, recursive=True)
        for f in matched:
            if f not in all_files:
                all_files.append(f)

    if not all_files:
        print("No files found to process")
        sys.exit(0)

    print(f"Total unique files to process: {len(all_files)}")
    total_replacements = 0
    for file_path in all_files:
        try:
            print(f"Processing: {file_path}")
            with open(file_path, 'r') as f:
                content = f.read()
            processed_content, count = replace_env_vars_with_count(content)
            with open(file_path, 'w') as f:
                f.write(processed_content)
            total_replacements += count
            print(f" -> Processed: {file_path} (replacements: {count})")
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")

    print(f"Total replacements across all files: {total_replacements}")
