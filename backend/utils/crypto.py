import hashlib
import secrets

# Generate a random salt
def generate_salt() -> str:
    # Return a random hexadecimal string with 16 bytes
    return secrets.token_hex(16)

# Hash a password with a given salt using SHA-256
def hash_password(password: str, salt: str) -> str:
    combined = password + salt
    return hashlib.sha256(combined.encode("utf-8")).hexdigest()

# Verify a password against the stored hash
def verify_password(password: str, salt: str, stored_hash: str) -> bool:
    return hash_password(password, salt) == stored_hash