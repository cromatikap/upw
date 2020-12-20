import os.path, json
from sample import upw, cfg

class User:
    """Define a user gerated from the couple login/master_password
       and manage its local configuration file."""
    def __init__(self, login, master_password):
        self.login = login
        self.masterkey = upw.derive_key_from(login, master_password)
        self.hash = upw.hash(login + self.masterkey)[0:40]
        self.emojish = upw.emojish(self.hash)

    def create_config(self):
        f = open(cfg.get('UPW_DIR') + self.hash, "a", encoding="utf-8")

    def is_config_exists(self):
        return os.path.isfile(cfg.get('UPW_DIR') + self.hash)

    def add_domain(self, domain):
        print('\nADD ' + domain + ' TO ' + self.login + '\'S PROFILE\n')
        f = open(cfg.get('UPW_DIR') + self.hash, "w", encoding="utf-8")
        json.dump(get_domains(user), f, ensure_ascii=False)

    def get_domains(self):
        f = open(cfg.get('UPW_DIR') + self.hash, "r", encoding="utf-8")
        data = json.load(f)
        f.close()
        return data['domains']
