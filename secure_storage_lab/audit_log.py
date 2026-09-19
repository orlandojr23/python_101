"""
audit_log.py - Access Attempt Logger for SECURE_STORAGE_LAB

Every read attempt (successful or denied) is appended to audit_log.txt
with a timestamp, the active role, the target file, and the outcome.
This satisfies the Monitoring/Logging requirement.
"""

import datetime
import os

# Audit log file is placed one level above the storage folder
LOG_FILE = os.path.join(os.path.dirname(__file__), "audit_log.txt")


def log_access(role: str, filename: str, success: bool, note: str = "") -> None:
    """
    Appends one audit log entry to audit_log.txt.

    Format:
        [2026-09-22 10:15:32] ROLE=OWNER  FILE=sensitive.txt  STATUS=SUCCESS  NOTE=Decryption OK
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "SUCCESS" if success else "DENIED"
    entry = (
        f"[{timestamp}]  ROLE={role:<10}  FILE={filename:<15}  "
        f"STATUS={status:<7}  NOTE={note}\n"
    )

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)


def print_log() -> None:
    """Reads and prints the current audit log to the console."""
    if not os.path.exists(LOG_FILE):
        print("  (No audit log entries yet.)")
        return
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        contents = f.read().strip()
    if not contents:
        print("  (Audit log is empty.)")
    else:
        print(contents)
