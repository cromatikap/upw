import base64
import json
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Crypto:

    def __init__(self, password):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'J\xfd7\xa8\x91#bL\xcbY\x9d<\xdd}\xa4f',
            iterations=390000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(bytes(password, 'utf-8')))
        self.fernet = Fernet(key)

    def encrypt(self, json_profile):
        s = json.dumps(json_profile)
        return self.fernet.encrypt(bytes(s, 'utf-8'))

    def decrypt(self, json_profile):
        s = self.fernet.decrypt(json_profile).decode('utf-8')
        return json.loads(s)
