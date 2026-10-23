#!/usr/bin/env python3
"""Print actual lab environment metadata without reading credentials."""

import json
from pathlib import Path
import platform
import shutil
import sqlite3
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def output(command):
    try:
        result = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            universal_newlines=True, timeout=5, check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def main():
    connection = sqlite3.connect(":memory:")
    try:
        source_id = connection.execute("SELECT sqlite_source_id()").fetchone()[0]
    finally:
        connection.close()
    data = {
        "python_version": platform.python_version(),
        "python_executable": sys.executable,
        "sqlite_version": sqlite3.sqlite_version,
        "sqlite_source_id": source_id,
        "system": platform.system(),
        "kernel_release": platform.release(),
        "machine": platform.machine(),
        "git_commit": output(["git", "-C", str(ROOT), "rev-parse", "HEAD"]),
        "strace_version": output(["strace", "-V"]) if shutil.which("strace") else None,
        "filesystem": output(["df", "-T", str(ROOT)]) if shutil.which("df") else None,
    }
    print(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
