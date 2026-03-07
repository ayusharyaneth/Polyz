from cryptography.fernet import Fernet
from config.settings import ENCRYPTION_KEY

_fernet = Fernet(ENCRYPTION_KEY) if ENCRYPTION_KEY else None

def encrypt_key(private_key: str) -> str:
    if not _fernet: raise ValueError("Encryption key not set")
    return _fernet.encrypt(private_key.encode()).decode()

def decrypt_key(encrypted_key: str) -> str:
    if not _fernet: raise ValueError("Encryption key not set")
    return _fernet.decrypt(encrypted_key.encode()).decode()
