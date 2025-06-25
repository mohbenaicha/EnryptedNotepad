import os
import base64
import json
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

backend = default_backend()

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=backend,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt_data(key: bytes, data: bytes) -> bytes:
    f = Fernet(key)
    return f.encrypt(data)

def decrypt_data(key: bytes, token: bytes) -> bytes:
    f = Fernet(key)
    return f.decrypt(token)

def verify_password(password: str, salt: bytes, stored_hash: bytes) -> bool:
    try:
        key = derive_key(password, salt)
        return key == stored_hash
    except Exception:
        return False

def create_password_hash(password: str) -> dict:
    salt = os.urandom(16)
    key = derive_key(password, salt)
    return {
        'salt': base64.b64encode(salt).decode('utf-8'),
        'hash': base64.b64encode(key).decode('utf-8'),
    }

def load_config(path='config.json'):
    if not os.path.exists(path):
        return None
    try:
        with open(path, 'r') as f:
            data = f.read().strip()
            if not data:
                return None
            return json.loads(data)
    except (json.JSONDecodeError, IOError):
        return None


def save_config(data, path='config.json'):
    with open(path, 'w') as f:
        json.dump(data, f)
