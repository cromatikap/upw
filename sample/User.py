import os, stat
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

    def _ensure_profile_dir(self):
        """Ensure the profile directory exists."""
        profile_dir = cfg.get('UPW_DIR')
        if not os.path.exists(profile_dir):
            os.makedirs(profile_dir, mode=0o700)  # rwx------ permissions

    def _get_profile_path(self):
        """Get the full path to the profile file."""
        return os.path.join(cfg.get('UPW_DIR'), self.hash)

    def save_profile(self):
        """Save the encrypted profile to disk."""
        self._ensure_profile_dir()
        profile_path = self._get_profile_path()
        
        try:
            with open(profile_path, "wb") as f:
                f.write(self.Crypto.encrypt(self.profile))
            # Set file permissions to 600 (rw-------) for security
            os.chmod(profile_path, stat.S_IRUSR | stat.S_IWUSR)
            self.authenticated = True
        except (OSError, IOError) as e:
            raise RuntimeError(f"Failed to save profile: {e}") from e

    def import_profile(self):
        """Import and decrypt the profile from disk."""
        profile_path = self._get_profile_path()
        
        try:
            with open(profile_path, "rb") as f:  # Binary mode for encrypted data
                encrypted_content = f.read()
            self.profile = self.Crypto.decrypt(encrypted_content)
            self.authenticated = True
            return True
        except FileNotFoundError:
            return False
        except (OSError, IOError):
            return False
        except Exception:
            # Decryption failed (wrong password, corrupted file, etc.)
            return False
    
    def update_profile(self):
        if self.authenticated:
            self.save_profile()

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
