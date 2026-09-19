"""
rbac.py - Role-Based Access Control (RBAC) definitions for SECURE_STORAGE_LAB

Roles and their permissions (Principle of Least Privilege):
  - GUEST    : can only read public.txt
  - EMPLOYEE : can read public.txt + internal.txt
  - OWNER    : can read all files (public, internal, sensitive)

Files:
  - public.txt   → readable by ALL roles
  - internal.txt → readable by EMPLOYEE and OWNER only
  - sensitive.txt→ readable by OWNER only (AND requires decryption key)
"""

# Define the role hierarchy
ROLES = {
    "GUEST": 0,
    "EMPLOYEE": 1,
    "OWNER": 2,
}

# Define per-file minimum role level required for access
FILE_ACCESS_POLICY = {
    "public.txt": ROLES["GUEST"],       # Everyone can read
    "internal.txt": ROLES["EMPLOYEE"],  # Employee and above
    "sensitive.txt": ROLES["OWNER"],    # Owner only
}

# Which file is encrypted at rest
ENCRYPTED_FILES = {"sensitive.txt"}


def get_role_level(role: str) -> int:
    """Returns the numeric privilege level for a given role string."""
    return ROLES.get(role.upper(), -1)


def can_access(role: str, filename: str) -> bool:
    """
    Returns True if the given role is permitted to access the file.
    Enforces Least Privilege - checks role level against file policy.
    """
    role_level = get_role_level(role)
    required_level = FILE_ACCESS_POLICY.get(filename, 999)  # unknown files = deny
    return role_level >= required_level


def is_encrypted(filename: str) -> bool:
    """Returns True if the file is stored encrypted at rest."""
    return filename in ENCRYPTED_FILES


def list_accessible_files(role: str) -> list[str]:
    """Returns the list of filenames this role can access."""
    return [f for f in FILE_ACCESS_POLICY if can_access(role, f)]
