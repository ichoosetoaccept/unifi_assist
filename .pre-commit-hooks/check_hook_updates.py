#!/usr/bin/env python3
"""Check if any pre-commit hooks have updates available."""

from subprocess import run
import sys
from datetime import datetime, timedelta
import os
import json


def get_last_check_time():
    """Get the last time we checked for updates."""
    cache_file = os.path.expanduser("~/.cache/pre-commit-update-check")
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r") as f:
                data = json.load(f)
                return datetime.fromisoformat(data["last_check"])
        except (json.JSONDecodeError, KeyError, ValueError):
            pass
    return None


def update_last_check_time():
    """Update the last check time."""
    cache_file = os.path.expanduser("~/.cache/pre-commit-update-check")
    os.makedirs(os.path.dirname(cache_file), exist_ok=True)
    with open(cache_file, "w") as f:
        json.dump({"last_check": datetime.now().isoformat()}, f)


def main():
    """
    Check for available pre-commit hook updates and manage update check frequency.
    
    This function performs a daily check for pre-commit hook updates. It prevents redundant checks by tracking the last update check time and only proceeds if more than a day has passed since the previous check.
    
    The function runs `pre-commit autoupdate` in dry-run mode to identify potential hook updates without making changes. If updates are detected, it prints warning messages to stderr and returns a non-zero status code.
    
    Returns:
        int: 0 if no updates are available or check is skipped, 1 if updates are found
    
    Raises:
        subprocess.CalledProcessError: If the pre-commit command fails to execute
    """
    # Only check once per day
    last_check = get_last_check_time()
    if last_check:
        time_since_check = datetime.now() - last_check
        if time_since_check < timedelta(days=1):
            return 0

    # Run pre-commit autoupdate in dry-run mode
    result = run(
        ["pre-commit", "autoupdate", "--dry-run"],
        capture_output=True,
        text=True,
    )

    # Look for lines indicating updates are available
    updates_available = False
    for line in result.stdout.splitlines():
        if "updating" in line and "->" in line:
            updates_available = True
            print(f"⚠️  {line}", file=sys.stderr)

    if updates_available:
        print(
            "⚠️  Updates available for pre-commit hooks. Run 'pre-commit autoupdate' to update.",
            file=sys.stderr,
        )
        return 1

    update_last_check_time()
    return 0


if __name__ == "__main__":
    sys.exit(main())
