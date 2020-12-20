import os.path, json
from sample import upw, cfg

def create_user(user):
    f = open(cfg.get('UPW_DIR') + user['hash'], "a")

def is_user_exists(user):
    return os.path.isfile(cfg.get('UPW_DIR') + user['hash'])

def add_domain(domain, user):
    print('\nADD ' + domain + ' TO ' + user['login'] + '\'S PROFILE\n')
    f = open(cfg.get('UPW_DIR') + user['hash'], "a")
