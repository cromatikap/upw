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
        self.profile = {"domains": []}

    def create(self):
        f = open(cfg.get('UPW_DIR') + self.hash, "a", encoding="utf-8")
        json.dump(self.profile, f, ensure_ascii=False)
        f.close()

    def import_profile(self):
        try:
            f = open(cfg.get('UPW_DIR') + self.hash, "r", encoding="utf-8")
            self.profile = json.load(f)
            f.close()
            return True
        except OSError:
            return False

    def add_domain(self, domain):
        try:
            self.profile["domains"].index(domain)
            return False
        except ValueError:
            self.profile["domains"].append(domain)
            f = open(cfg.get('UPW_DIR') + self.hash, "w", encoding="utf-8")
            json.dump(self.profile, f, ensure_ascii=False)
            f.close()
            return True

    def get_domains(self):
        f = open(cfg.get('UPW_DIR') + self.hash, "r", encoding="utf-8")
        data = json.load(f)
        f.close()
        return data['domains']
