"""
crypto.py - Encryption-at-Rest helpers for SECURE_STORAGE_LAB
Uses the `cryptography` library (Fernet = AES-128-CBC + HMAC-SHA256).
The encryption key is derived from the user's passphrase via SHA-256.
"""

import base64
import hashlib
from cryptography.fernet import Fernet, InvalidToken


def derive_key(passphrase: str) -> bytes:
    """
    Derives a 32-byte Fernet-compatible key from a plaintext passphrase.
    Steps:
      1. Encode passphrase to bytes (UTF-8).
      2. Hash with SHA-256 to get exactly 32 bytes.
      3. Base64url-encode - Fernet requires a URL-safe base64 key of 32 bytes.
    """
    raw = hashlib.sha256(passphrase.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(raw)


def encrypt_data(plaintext: str, passphrase: str) -> bytes:
    """
    Encrypts a plaintext string with AES (Fernet) using the derived key.
    Returns the ciphertext as bytes (safe to write to a file).
    """
    key = derive_key(passphrase)
    f = Fernet(key)
    return f.encrypt(plaintext.encode("utf-8"))


def decrypt_data(ciphertext: bytes, passphrase: str) -> str | None:
    """
    Decrypts Fernet ciphertext using the derived key.
    Returns the plaintext string on success, or None if the key is wrong.
    """
    key = derive_key(passphrase)
    f = Fernet(key)
    try:
        return f.decrypt(ciphertext).decode("utf-8")
    except InvalidToken:
        return None
