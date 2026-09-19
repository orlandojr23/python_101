"""
setup.py - Initializes the SECURE_STORAGE_LAB directory and data files.

Run this once (or it's called automatically by main.py on first launch).
Creates:
  SECURE_STORAGE_LAB/
    public.txt   - plain text, readable by all
    internal.txt - plain text, readable by Employee+
    sensitive.txt- AES-encrypted at rest, readable by Owner only
"""

import os
from crypto import encrypt_data

# Canonical storage folder name (as specified by the activity)
STORAGE_DIR = os.path.join(os.path.dirname(__file__), "SECURE_STORAGE_LAB")

# The Owner's encryption passphrase (hardcoded for the lab demo)
# In production, this would NEVER be hardcoded - it would come from a KMS.
OWNER_PASSPHRASE = "IAS1-SecureOwner-2026"

# ─────────────────────────────────────────────
#  File content definitions
# ─────────────────────────────────────────────
PUBLIC_CONTENT = """\
=== PUBLIC NOTICE - SECURE_STORAGE_LAB ===

Welcome to the PHINMA IAS1 Secure Storage Lab.
This file is publicly accessible to all users: Guest, Employee, and Owner.

CIA Triad Focus: AVAILABILITY
  - This file is intentionally unencrypted and world-readable.
  - Availability is the priority: any user must be able to access it instantly.
  - No sensitive data is stored here.

Last Updated: September 22, 2026
"""

INTERNAL_CONTENT = """\
=== INTERNAL MEMO - SECURE_STORAGE_LAB ===
[CLASSIFICATION: INTERNAL - FOR AUTHORIZED EMPLOYEES ONLY]

This document contains internal operational guidelines for Group 1.
Access is restricted to Employees and Owners only.

CIA Triad Focus: INTEGRITY + CONTROLLED AVAILABILITY
  - Role-based access control prevents Guest-level tampering.
  - Only verified Employees may read or contribute to this file.
  - Integrity is maintained: unauthorized parties cannot alter records.

Internal Notes:
  - Encryption key rotation schedule: every 90 days.
  - All access attempts are logged via audit_log.txt.
  - Report any unauthorized access to the system Owner immediately.

Last Updated: September 22, 2026
"""

SENSITIVE_CONTENT = """\
=== SENSITIVE RECORD - SECURE_STORAGE_LAB ===
[CLASSIFICATION: TOP SECRET - OWNER ACCESS ONLY]
[STATUS: DECRYPTED - DO NOT DISTRIBUTE]

This file contains confidential credentials and private system data.
It is encrypted at rest using AES (Fernet) with a key derived via SHA-256.

CIA Triad Focus: CONFIDENTIALITY
  - Encrypted at rest: stored as AES ciphertext on disk at all times.
  - Only the Owner role may decrypt and read this file.
  - Guests and Employees see only an "Access Denied" message.
  - RBAC + Encryption together enforce confidentiality at two layers.

Confidential Data:
  Owner Username : admin_oj
  System Token   : 8f4a2c1e-9b3d-4f7e-a1c6-2d5b8e0f3a9c
  DB Passphrase  : [REDACTED - visible only after successful decryption]

Last Updated: September 22, 2026
"""


def setup_lab() -> bool:
    """
    Creates the SECURE_STORAGE_LAB directory and writes all three files.
    Returns True if setup was performed, False if already exists.
    """
    if os.path.isdir(STORAGE_DIR):
        return False  # Already set up

    os.makedirs(STORAGE_DIR, exist_ok=True)

    # Write public.txt - plain text
    _write_file("public.txt", PUBLIC_CONTENT.encode("utf-8"))

    # Write internal.txt - plain text (access controlled by RBAC only)
    _write_file("internal.txt", INTERNAL_CONTENT.encode("utf-8"))

    # Write sensitive.txt - AES encrypted at rest
    ciphertext = encrypt_data(SENSITIVE_CONTENT, OWNER_PASSPHRASE)
    _write_file("sensitive.txt", ciphertext)

    return True


def _write_file(filename: str, data: bytes) -> None:
    path = os.path.join(STORAGE_DIR, filename)
    with open(path, "wb") as f:
        f.write(data)


def get_storage_dir() -> str:
    return STORAGE_DIR


def get_owner_passphrase() -> str:
    return OWNER_PASSPHRASE
