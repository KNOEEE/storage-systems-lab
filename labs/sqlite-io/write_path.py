#!/usr/bin/env python3
"""Create and verify one small SQLite transaction for syscall tracing.

Requires only the Python standard library. Existing output directories are never
reused, so re-running the lab cannot overwrite a previous database or report.
"""

import argparse
import datetime
import json
from pathlib import Path
import platform
import sqlite3
import time


ROWS = 128
PAYLOAD_BYTES = 256
PAYLOAD = "x" * PAYLOAD_BYTES


def run(output_dir):
    # Creating the leaf directory exclusively also rejects an existing symlink.
    output_dir.mkdir(parents=True, exist_ok=False)
    database = output_dir / "database.sqlite3"
    connection = sqlite3.connect(str(database), isolation_level=None)
    try:
        journal_mode = connection.execute("PRAGMA journal_mode=DELETE").fetchone()[0]
        connection.execute("PRAGMA synchronous=FULL")
        synchronous = connection.execute("PRAGMA synchronous").fetchone()[0]
        if journal_mode.lower() != "delete" or synchronous != 2:
            raise RuntimeError("SQLite did not apply journal_mode=DELETE / synchronous=FULL")

        started = time.perf_counter()
        connection.execute("BEGIN IMMEDIATE")
        connection.execute("CREATE TABLE records (id INTEGER PRIMARY KEY, payload TEXT NOT NULL)")
        connection.executemany(
            "INSERT INTO records (id, payload) VALUES (?, ?)",
            ((row_id, PAYLOAD) for row_id in range(1, ROWS + 1)),
        )
        connection.execute("COMMIT")
        transaction_seconds = time.perf_counter() - started
        page_size = connection.execute("PRAGMA page_size").fetchone()[0]
        page_count = connection.execute("PRAGMA page_count").fetchone()[0]
    finally:
        connection.close()

    # Normal close/reopen checks are not crash-recovery or power-loss tests.
    reopened = sqlite3.connect(str(database))
    try:
        records = reopened.execute("SELECT id, payload FROM records ORDER BY id").fetchall()
        integrity = [row[0] for row in reopened.execute("PRAGMA integrity_check")]
    finally:
        reopened.close()

    content_matches = records == [(row_id, PAYLOAD) for row_id in range(1, ROWS + 1)]
    passed = content_matches and integrity == ["ok"]
    report = {
        "schema_version": 1,
        "recorded_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "environment": {
            "python_version": platform.python_version(),
            "sqlite_version": sqlite3.sqlite_version,
            "sqlite_source_id": sqlite_source_id(),
            "system": platform.system(),
            "kernel_release": platform.release(),
            "machine": platform.machine(),
        },
        "workload": {
            "name": "sqlite-single-transaction-write-path",
            "transactions": 1,
            "rows": ROWS,
            "payload_bytes_per_row": PAYLOAD_BYTES,
            "journal_mode": journal_mode,
            "synchronous": "FULL",
            "synchronous_value": synchronous,
        },
        "observations": {
            "database_path": str(database.resolve()),
            "database_size_bytes": database.stat().st_size,
            "page_size_bytes": page_size,
            "page_count": page_count,
            "transaction_seconds": transaction_seconds,
            "rows_after_reopen": len(records),
            "content_matches": content_matches,
            "integrity_check": integrity,
        },
        "verification": {
            "normal_reopen_passed": passed,
            "syscall_trace": "not_assessed_by_this_script",
            "crash_recovery": "not_tested",
            "power_loss_durability": "not_tested",
        },
    }
    with (output_dir / "result.json").open("x", encoding="utf-8") as report_file:
        json.dump(report, report_file, ensure_ascii=False, indent=2)
        report_file.write("\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if not passed:
        raise RuntimeError("Data verification failed; inspect result.json")


def sqlite_source_id():
    connection = sqlite3.connect(":memory:")
    try:
        return connection.execute("SELECT sqlite_source_id()").fetchone()[0]
    finally:
        connection.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir", type=Path, required=True,
        help="A new directory for database.sqlite3 and result.json; must not exist",
    )
    arguments = parser.parse_args()
    try:
        run(arguments.output_dir)
    except FileExistsError:
        parser.exit(2, "Output path already exists; choose a new --output-dir. Nothing was overwritten.\n")
    except (OSError, sqlite3.Error, RuntimeError) as error:
        parser.exit(1, "Lab failed: {}. Keep the output directory for diagnosis.\n".format(error))


if __name__ == "__main__":
    main()
