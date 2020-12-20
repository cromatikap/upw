import getpass, yaml, hashlib
from hashlib import blake2s
from . import cfg

with open('config.yml', 'r') as file:
    cfg = yaml.safe_load(file)

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
