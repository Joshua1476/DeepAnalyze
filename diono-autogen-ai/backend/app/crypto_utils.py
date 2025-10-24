"""
Encryption and security utilities
"""
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
from typing import Optional


class CryptoUtils:
    """Encryption utilities for sensitive data"""
    
    def __init__(self, master_key: Optional[str] = None):
        """Initialize with master key"""
        if master_key:
            self.master_key = master_key.encode()
        else:
            self.master_key = os.environ.get("MASTER_KEY", "default-key-change-me").encode()
    
    def _derive_key(self, salt: bytes) -> bytes:
        """Derive encryption key from master key"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000
        )
        return base64.urlsafe_b64encode(kdf.derive(self.master_key))
    
    def encrypt(self, data: str) -> str:
        """Encrypt string data"""
        salt = os.urandom(16)
        key = self._derive_key(salt)
        f = Fernet(key)
        encrypted = f.encrypt(data.encode())
        # Combine salt and encrypted data
        return base64.urlsafe_b64encode(salt + encrypted).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt string data"""
        try:
            combined = base64.urlsafe_b64decode(encrypted_data.encode())
            salt = combined[:16]
            encrypted = combined[16:]
            key = self._derive_key(salt)
            f = Fernet(key)
            decrypted = f.decrypt(encrypted)
            return decrypted.decode()
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")
    
    def hash_password(self, password: str) -> str:
        """Hash password for storage"""
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(plain_password, hashed_password)


# Global crypto instance
crypto = CryptoUtils()
