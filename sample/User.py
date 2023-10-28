from sample import cfg, Crypto

class User:
    """Define a user gerated from the couple login/master_password
       and manage its local configuration file."""
    authenticated = False
    profile = {"domains": []}
    
    def __init__(self, login, master_password):
        self.login = login
        self.masterkey = Crypto.derive_key_from(login, master_password)
        self.Crypto = Crypto.Crypto(self.masterkey)
        self.hash = Crypto.hash(login + self.masterkey)[0:40]
        self.emojish = Crypto.emojish(self.hash)

    def save_profile(self):
        f = open(cfg.get('UPW_DIR') + self.hash, "wb")
        f.write(self.Crypto.encrypt(self.profile))
        f.close()
        self.authenticated = True

    def import_profile(self):
        try:
            f = open(cfg.get('UPW_DIR') + self.hash, "r", encoding="utf-8")
            content = f.read()
            self.profile = self.Crypto.decrypt(content)
            f.close()
            self.authenticated = True
            return True
        except OSError:
            return False
    
    def update_profile(self):
        if self.authenticated:
            self.create_profile()

    def add_domain(self, domain):
        try:
            self.profile["domains"].index(domain)
            return False
        except ValueError:
            self.profile["domains"].append(domain)
            return True
    
    def del_domain(self, domain):
        try:
            self.profile["domains"].remove(domain)
            return True
        except ValueError:
            return False

    def get_domains(self):
        return self.profile["domains"]
