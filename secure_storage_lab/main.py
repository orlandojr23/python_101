"""
main.py - Entry Point for the SECURE_STORAGE_LAB Console Application
Course: Information Assurance and Security 1 (IAS1) - Module 9
Group:  Group 1 | Language: Python
Date:   September 22, 2026

Run with:  python main.py

No external servers required. All data stored locally in SECURE_STORAGE_LAB/.
"""

import os
import sys
import time

# ── Make sure sibling modules resolve correctly ──────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))

from setup import setup_lab, get_storage_dir, get_owner_passphrase
from rbac import can_access, is_encrypted, FILE_ACCESS_POLICY, ROLES
from crypto import decrypt_data
from audit_log import log_access, print_log

# ─────────────────────────────────────────────────────────────────────────────
#  Console color codes (ANSI - works on modern Windows terminals & Linux/Mac)
# ─────────────────────────────────────────────────────────────────────────────
class C:
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    DIM    = "\033[2m"
    RED    = "\033[91m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    CYAN   = "\033[96m"
    WHITE  = "\033[97m"
    BLUE   = "\033[94m"
    MAGENTA= "\033[95m"
    BG_RED = "\033[41m"
    BG_GRN = "\033[42m"
    BG_BLU = "\033[44m"


def enable_ansi_windows() -> None:
    """Enable ANSI escape codes on Windows 10+ terminals."""
    if sys.platform == "win32":
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except Exception:
            pass


def banner() -> None:
    print(f"""
{C.CYAN}{C.BOLD}
╔══════════════════════════════════════════════════════════════════╗
║          SECURE STORAGE LAB  -  IAS1 Module 9 Demo              ║
║          Role-Based Access Control + Encryption at Rest          ║
║          Group 1 | PHINMA Education | Python                     ║
╚══════════════════════════════════════════════════════════════════╝{C.RESET}
""")


def section(title: str) -> None:
    width = 66
    print(f"\n{C.BLUE}{C.BOLD}{'─' * width}")
    print(f"  {title}")
    print(f"{'─' * width}{C.RESET}")


def success(msg: str) -> None:
    print(f"  {C.GREEN}✔  {msg}{C.RESET}")


def denied(msg: str) -> None:
    print(f"  {C.RED}✘  {msg}{C.RESET}")


def warn(msg: str) -> None:
    print(f"  {C.YELLOW}⚠  {msg}{C.RESET}")


def info(msg: str) -> None:
    print(f"  {C.DIM}{msg}{C.RESET}")


# ─────────────────────────────────────────────────────────────────────────────
#  Role Selection
# ─────────────────────────────────────────────────────────────────────────────
def select_role() -> str:
    section("STEP 1 - SELECT YOUR ROLE (Login Simulation)")
    print(f"""
  {C.WHITE}Available Roles:{C.RESET}

    {C.CYAN}[1]{C.RESET}  GUEST     - Public access only
    {C.YELLOW}[2]{C.RESET}  EMPLOYEE  - Internal access (group-level)
    {C.GREEN}[3]{C.RESET}  OWNER     - Full access + encrypted file access
    {C.MAGENTA}[4]{C.RESET}  View Audit Log
    {C.MAGENTA}[5]{C.RESET}  View Presentation Notes (CIA Triad + Checklist)
    {C.RED}[0]{C.RESET}  Exit
""")
    while True:
        choice = input(f"  {C.BOLD}Enter your choice: {C.RESET}").strip()
        if choice == "1":
            return "GUEST"
        elif choice == "2":
            return "EMPLOYEE"
        elif choice == "3":
            return "OWNER"
        elif choice == "4":
            return "__LOG__"
        elif choice == "5":
            return "__DOCS__"
        elif choice == "0":
            return "__EXIT__"
        else:
            warn("Invalid choice. Please enter 1, 2, 3, 4, 5, or 0.")


# ─────────────────────────────────────────────────────────────────────────────
#  File Browser
# ─────────────────────────────────────────────────────────────────────────────
def file_menu(role: str) -> None:
    section(f"STEP 2 - FILE ACCESS BROWSER  [Active Role: {role}]")

    files = list(FILE_ACCESS_POLICY.keys())
    role_color = {"GUEST": C.CYAN, "EMPLOYEE": C.YELLOW, "OWNER": C.GREEN}.get(role, C.WHITE)

    print(f"\n  {C.BOLD}Logged in as: {role_color}{role}{C.RESET}\n")
    print(f"  {C.WHITE}Available files in SECURE_STORAGE_LAB:{C.RESET}\n")

    for i, fname in enumerate(files, 1):
        accessible = can_access(role, fname)
        enc_tag = f"{C.MAGENTA}[AES-ENCRYPTED]{C.RESET}" if is_encrypted(fname) else ""
        status_tag = f"{C.GREEN}✔ Accessible{C.RESET}" if accessible else f"{C.RED}✘ Restricted{C.RESET}"
        print(f"    {C.BOLD}[{i}]{C.RESET}  {fname:<17} {status_tag}  {enc_tag}")

    print(f"\n    {C.RED}[0]{C.RESET}  Back to main menu\n")

    while True:
        choice = input(f"  {C.BOLD}Select a file to read (or 0 to go back): {C.RESET}").strip()
        if choice == "0":
            return
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(files):
                read_file(role, files[idx])
                input(f"\n  {C.DIM}Press Enter to continue...{C.RESET}")
                return
            else:
                warn("Invalid file number.")
        except ValueError:
            warn("Please enter a number.")


def read_file(role: str, filename: str) -> None:
    section(f"FILE READ REQUEST - {filename}")
    info(f"Role     : {role}")
    info(f"File     : {filename}")
    info(f"Encrypted: {'Yes (AES-Fernet)' if is_encrypted(filename) else 'No (plain text)'}")
    print()

    storage_dir = get_storage_dir()
    filepath = os.path.join(storage_dir, filename)

    # ── Access Control Check ─────────────────────────────────────────────────
    if not can_access(role, filename):
        denied(f"ACCESS DENIED - Your role ({role}) does not have permission to read '{filename}'.")
        denied("Principle of Least Privilege enforced.")
        log_access(role, filename, success=False, note="Insufficient role privileges")
        return

    # ── File must exist ──────────────────────────────────────────────────────
    if not os.path.exists(filepath):
        warn(f"File '{filename}' not found on disk. Run setup first.")
        log_access(role, filename, success=False, note="File not found on disk")
        return

    # ── Encrypted file: prompt for decryption key ────────────────────────────
    if is_encrypted(filename):
        print(f"  {C.YELLOW}⚑  This file is encrypted at rest.{C.RESET}")
        print(f"  {C.YELLOW}   You must enter the decryption key to read its contents.{C.RESET}\n")

        attempts = 0
        max_attempts = 3

        while attempts < max_attempts:
            attempts += 1
            key_input = input(f"  {C.BOLD}Enter decryption key (Attempt {attempts}/{max_attempts}): {C.RESET}").strip()

            with open(filepath, "rb") as f:
                ciphertext = f.read()

            plaintext = decrypt_data(ciphertext, key_input)

            if plaintext is not None:
                success("Decryption successful! Displaying file contents:\n")
                print(f"{C.CYAN}{'═' * 66}{C.RESET}")
                print(plaintext)
                print(f"{C.CYAN}{'═' * 66}{C.RESET}")
                log_access(role, filename, success=True, note="Decryption OK")
                return
            else:
                denied(f"Wrong decryption key. {max_attempts - attempts} attempt(s) remaining.")
                log_access(role, filename, success=False, note=f"Wrong decryption key (attempt {attempts})")

        denied("Maximum decryption attempts exceeded. Access blocked.")
        log_access(role, filename, success=False, note="Max decryption attempts exceeded")
        return

    # ── Plain text file: read directly ──────────────────────────────────────
    with open(filepath, "r", encoding="utf-8") as f:
        contents = f.read()

    success(f"Access granted. Displaying '{filename}':\n")
    print(f"{C.CYAN}{'═' * 66}{C.RESET}")
    print(contents)
    print(f"{C.CYAN}{'═' * 66}{C.RESET}")
    log_access(role, filename, success=True, note="Plain text access")


# ─────────────────────────────────────────────────────────────────────────────
#  Presentation Notes - CIA Triad + Audit Checklist + Risk Analysis
# ─────────────────────────────────────────────────────────────────────────────
PRESENTATION_NOTES = f"""
{C.CYAN}{C.BOLD}
╔══════════════════════════════════════════════════════════════════╗
║         PRESENTATION NOTES - GROUP 1 | IAS1 MODULE 9            ║
╚══════════════════════════════════════════════════════════════════╝{C.RESET}

{C.BOLD}{C.YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 1. CIA TRIAD JUSTIFICATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{C.RESET}

{C.GREEN}▶ public.txt - AVAILABILITY is prioritized{C.RESET}
  public.txt is readable by all roles (Guest, Employee, Owner) without
  any authentication or decryption, because its contents are non-sensitive
  public notices. Prioritizing Availability ensures that any user or visitor
  can always retrieve the information, preventing unnecessary friction and
  service disruption for non-confidential data.

{C.YELLOW}▶ internal.txt - INTEGRITY + CONTROLLED AVAILABILITY{C.RESET}
  Access to internal.txt is restricted to Employee and Owner roles through
  RBAC (Role-Based Access Control), enforcing the Principle of Least Privilege.
  This preserves Integrity by ensuring only authorized personnel can view or
  reference internal documents - reducing the risk of unauthorized modification
  or leaking of operational information to Guest-level users.

{C.RED}▶ sensitive.txt - CONFIDENTIALITY is maintained{C.RESET}
  sensitive.txt is encrypted at rest using AES (Fernet) with a key derived
  from a passphrase via SHA-256. Even if the file is physically accessed on
  disk, the ciphertext is unreadable without the correct key. Combined with
  RBAC (Owner-only access) and a decryption key prompt, two independent
  security layers enforce Confidentiality: role authorization AND encryption.

{C.BOLD}{C.YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 2. STORAGE SECURITY AUDIT CHECKLIST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{C.RESET}

  {C.GREEN}[✔] Data Location{C.RESET}
       Storage location identified → Local File System (SECURE_STORAGE_LAB/)

  {C.GREEN}[✔] Access Roles{C.RESET}
       Roles clearly defined → Guest (0), Employee (1), Owner (2)

  {C.GREEN}[✔] Least Privilege{C.RESET}
       No "everyone" access for sensitive files.
       Each file has a minimum required role level enforced in rbac.py.

  {C.GREEN}[✔] Encryption-at-Rest{C.RESET}
       sensitive.txt is encrypted using AES-128 (Fernet/cryptography lib).
       Ciphertext is stored on disk; decryption only happens in-memory.

  {C.GREEN}[✔] Monitoring / Logging{C.RESET}
       All access attempts (success + denied) are logged to audit_log.txt
       with timestamp, role, filename, and status.

{C.BOLD}{C.YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 3. RISK ANALYSIS (Coaching Prompt)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{C.RESET}

  {C.RED}⚠  One Risk / Vulnerability Found:{C.RESET}
     The decryption passphrase ("IAS1-SecureOwner-2026") is hardcoded
     directly in setup.py. In this demo, anyone who reads the source code
     can discover the key and decrypt sensitive.txt without going through
     the RBAC prompt. This violates the principle that secrets should never
     live in source code or version control.

  {C.GREEN}✔  One Proposed Fix (Production Mitigation):{C.RESET}
     In a production system, the passphrase (or its derived key) would be
     stored in a Key Management Service (KMS) - such as AWS KMS, Azure Key
     Vault, or HashiCorp Vault - and never embedded in code. The application
     would request the key from the KMS at runtime only after the user
     authenticates, ensuring the key is never in plaintext in the codebase
     or in version control repositories.
"""


def show_docs() -> None:
    print(PRESENTATION_NOTES)
    input(f"\n  {C.DIM}Press Enter to return to the main menu...{C.RESET}")


# ─────────────────────────────────────────────────────────────────────────────
#  Main Loop
# ─────────────────────────────────────────────────────────────────────────────
def main() -> None:
    enable_ansi_windows()

    # Initialize storage on first run
    banner()
    info("Initializing SECURE_STORAGE_LAB...")
    was_setup = setup_lab()
    if was_setup:
        success("SECURE_STORAGE_LAB created and files initialized successfully!")
        info(f"  Storage path: {get_storage_dir()}")
        info("  Files created: public.txt | internal.txt | sensitive.txt (AES-encrypted)")
    else:
        success("SECURE_STORAGE_LAB already initialized. Ready.")
    
    time.sleep(0.8)

    # Main application loop
    while True:
        banner()
        action = select_role()

        if action == "__EXIT__":
            print(f"\n  {C.CYAN}Goodbye! All access events have been logged to audit_log.txt{C.RESET}\n")
            break
        elif action == "__LOG__":
            section("AUDIT LOG - All Access Attempts")
            print()
            print_log()
            print()
            input(f"  {C.DIM}Press Enter to return to the main menu...{C.RESET}")
        elif action == "__DOCS__":
            show_docs()
        else:
            # User selected a role - go to file browser
            file_menu(action)


if __name__ == "__main__":
    main()
