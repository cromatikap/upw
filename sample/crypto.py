import base64
import json
import hashlib
from typing import Dict, Any
from . import cfg
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class Crypto:

    def __init__(self, password: str) -> None:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'J\xfd7\xa8\x91#bL\xcbY\x9d<\xdd}\xa4f',
            iterations=390000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(bytes(password, 'utf-8')))
        self.fernet: Fernet = Fernet(key)

    def encrypt(self, json_profile: Dict[str, Any]) -> bytes:
        s = json.dumps(json_profile)
        return self.fernet.encrypt(bytes(s, 'utf-8'))

    def decrypt(self, json_profile: bytes) -> Dict[str, Any]:
        s = self.fernet.decrypt(json_profile).decode('utf-8')
        return json.loads(s)

def derive_key_from(key1: str | bytes | bytearray, key2: str | bytes | bytearray) -> str:
    """Derive a key from two input keys using PBKDF2.
    
    Args:
        key1: First key (can be str, bytes, or bytearray)
        key2: Second key (can be str, bytes, or bytearray)
        
    Returns:
        Hex-encoded derived key
    """
    hash_config = cfg.get('hash')
    
    # Convert to bytes if needed
    if isinstance(key1, str):
        key1_bytes = key1.encode('utf-8')
    elif isinstance(key1, bytearray):
        key1_bytes = bytes(key1)  # Create bytes copy from bytearray
    else:
        key1_bytes = key1  # Already bytes
    
    if isinstance(key2, str):
        key2_bytes = key2.encode('utf-8')
    elif isinstance(key2, bytearray):
        key2_bytes = bytes(key2)  # Create bytes copy from bytearray
    else:
        key2_bytes = key2  # Already bytes
    
    pk = hashlib.pbkdf2_hmac(
        hash_config['name'], 
        key1_bytes + key2_bytes, 
        hash_config['salt'].encode(), 
        hash_config['dklen']
    )
    return pk.hex()

def hash(input: str) -> str:
    sha = hashlib.sha256()
    sha.update(input.encode())
    return sha.hexdigest()

def emojish(input: str) -> str:
    emojish1 = cfg.get('emojish_list')[int(input[0], 16)]
    emojish2 = cfg.get('emojish_list')[int(input[-1], 16)]
    return emojish1 + ' ' + emojish2