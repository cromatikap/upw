import os.path
from sample import upw, cfg

def createUser(user):
    f = open(cfg.get('UPW_DIR') + user['hash'], "a")

def isUserExists(user):
    return os.path.isfile(cfg.get('UPW_DIR') + user['hash'])

def addDomain(domain, user):
    print('\nADD ' + domain + ' TO ' + user['login'] + '\'S PROFILE\n')
