from typing import Dict
from sample import Crypto
from sample.profile_repository import ProfileRepository

class User:
    """Represents a user and manages their profile data.
    
    This class is responsible for:
    - User identity (login, masterkey, hash, emojish)
    - Domain management (add/remove/get domains)
    - Authentication state
    - Coordinating with ProfileRepository for persistence
    """
    authenticated: bool = False
    profile: Dict[str, list[str]] = {"domains": []}
    
    def __init__(self, login: str, master_password: str) -> None:
        """Initialize user from login and master password."""
        self.login: str = login
        self.masterkey: str = Crypto.derive_key_from(login, master_password)
        self.crypto: Crypto.Crypto = Crypto.Crypto(self.masterkey)
        self.hash: str = Crypto.hash(login + self.masterkey)[0:40]
        self.emojish: str = Crypto.emojish(self.hash)
        
        # Initialize repository for file operations
        self._repository: ProfileRepository = ProfileRepository(
            self.crypto, 
            self.hash
        )

    def save_profile(self) -> None:
        """Save the current profile to disk."""
        self._repository.save(self.profile)
        self.authenticated = True

    def import_profile(self) -> bool:
        """Import profile from disk if it exists.
        
        Returns:
            True if profile was loaded successfully, False otherwise
        """
        loaded_profile = self._repository.load()
        if loaded_profile is not None:
            self.profile = loaded_profile
            self.authenticated = True
            return True
        return False
    
    def update_profile(self) -> None:
        if self.authenticated:
            self.save_profile()

    def add_domain(self, domain: str) -> bool:
        try:
            self.profile["domains"].index(domain)
            return False
        except ValueError:
            self.profile["domains"].append(domain)
            return True
    
    def del_domain(self, domain: str) -> bool:
        try:
            self.profile["domains"].remove(domain)
            return True
        except ValueError:
            return False

    def get_domains(self) -> list[str]:
        return self.profile["domains"]
