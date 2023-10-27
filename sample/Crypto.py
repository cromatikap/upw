import base64
import json
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import yaml, hashlib
from . import cfg

with open('config.yml', 'r') as file:
    cfg = yaml.safe_load(file)
    
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

def derive_key_from(key1, key2):
    hash = cfg.get('hash')
    pk = hashlib.pbkdf2_hmac(hash['name'], key1.encode() + key2.encode(), hash['salt'].encode(), cfg['hash']['dklen'])
    return pk.hex()

def hash(input):
    sha = hashlib.sha256()
    sha.update(input.encode())
    return sha.hexdigest()

def emojish(input):
    emojish1 = cfg.get('emojish_list')[int(input[0], 16)]
    emojish2 = cfg.get('emojish_list')[int(input[-1], 16)]
    return emojish1 + ' ' + emojish2