# src/utils/helpers.py
from cryptography.fernet import Fernet
from src.config.settings import settings

_fernet = Fernet(settings.ENCRYPTION_KEY.encode() if settings.ENCRYPTION_KEY else Fernet.generate_key())

def encrypt_key(private_key: str) -> str:
    return _fernet.encrypt(private_key.encode()).decode()

def decrypt_key(encrypted_key: str) -> str:
    return _fernet.decrypt(encrypted_key.encode()).decode()
