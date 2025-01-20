#!/usr/bin/env python3
"""Check if any pre-commit hooks have updates available."""

import os
import json
import shutil
import sys
import shlex
from datetime import datetime, timedelta
from subprocess import CalledProcessError, run


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


def get_pre_commit_path():
    """Get the absolute path to pre-commit executable."""
    pre_commit_path = shutil.which("pre-commit")
    if not pre_commit_path:
        print("⚠️  pre-commit not found in PATH", file=sys.stderr)
        sys.exit(1)
    pre_commit_path = os.path.abspath(pre_commit_path)
    if not os.path.isfile(pre_commit_path) or not os.access(
        pre_commit_path,
        os.X_OK,
    ):
        print(f"⚠️  Invalid pre-commit path: {pre_commit_path}", file=sys.stderr)
        sys.exit(1)
    return pre_commit_path


def main():
    """Main function."""
    # Only check once per day
    last_check = get_last_check_time()
    if last_check:
        time_since_check = datetime.now() - last_check
        if time_since_check < timedelta(days=1):
            return 0

    # Run pre-commit autoupdate in dry-run mode with explicit arguments
    try:
        pre_commit_path = get_pre_commit_path()

        result = run(
            [shlex.quote(pre_commit_path), "autoupdate", "--dry-run"],
            capture_output=True,
            text=True,
            check=True,
        )
    except CalledProcessError as e:
        print(f"⚠️  Error running pre-commit: {e}", file=sys.stderr)
        return 1

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
