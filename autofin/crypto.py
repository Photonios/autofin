import hashlib

from autofin import settings


def hash_password(email: str, password: str) -> str:
    """Hashes the specified password with the configured
    hashing algorithm and returns the hex-encoded hash."""

    sha = hashlib.sha512()
    sha.update((email + password).encode())

    hex_hash = sha.hexdigest()
    return hex_hash
