import os
import stat
import jsonschema
from typing import Dict, Any, Optional
from sample import cfg
from sample.Crypto import Crypto

# JSON schema for profile structure validation
PROFILE_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "domains": {
            "type": "array",
            "items": {
                "type": "string"
            }
        }
    },
    "required": ["domains"],
    "additionalProperties": False
}


class ProfileRepository:
    """Handles all file I/O operations for user profiles.
    
    This class is responsible for:
    - Reading/writing profile files
    - Managing directory structure
    - Encrypting/decrypting profile data
    - Validating profile structure
    - Setting file permissions
    """
    
    def __init__(self, crypto: Crypto, profile_hash: str) -> None:
        """Initialize repository with encryption and profile identifier.
        
        Args:
            crypto: Crypto instance for encryption/decryption
            profile_hash: Unique identifier for the profile file
        """
        self.crypto = crypto
        self.profile_hash = profile_hash
        self._profile_dir = cfg.get('UPW_DIR')
    
    def _ensure_profile_dir(self) -> None:
        """Ensure the profile directory exists with secure permissions."""
        if not os.path.exists(self._profile_dir):
            os.makedirs(self._profile_dir, mode=0o700)  # rwx------
    
    def _get_profile_path(self) -> str:
        """Get the full path to the profile file."""
        return os.path.join(self._profile_dir, self.profile_hash)
    
    def _validate_profile(self, profile_data: Dict[str, Any]) -> None:
        """Validate profile data against JSON schema.
        
        Args:
            profile_data: The profile dictionary to validate
            
        Raises:
            jsonschema.ValidationError: If profile structure is invalid
        """
        jsonschema.validate(instance=profile_data, schema=PROFILE_SCHEMA)
    
    def save(self, profile: Dict[str, Any]) -> None:
        """Save encrypted profile to disk.
        
        Args:
            profile: Profile dictionary to save
            
        Raises:
            RuntimeError: If file operations fail
        """
        self._ensure_profile_dir()
        profile_path = self._get_profile_path()
        
        try:
            with open(profile_path, "wb") as f:
                f.write(self.crypto.encrypt(profile))
            # Set secure file permissions (rw-------)
            os.chmod(profile_path, stat.S_IRUSR | stat.S_IWUSR)
        except (OSError, IOError) as e:
            raise RuntimeError(f"Failed to save profile: {e}") from e
    
    def load(self) -> Optional[Dict[str, Any]]:
        """Load and decrypt profile from disk.
        
        Returns:
            Profile dictionary if found and valid, None otherwise
        """
        profile_path = self._get_profile_path()
        
        try:
            with open(profile_path, "rb") as f:
                encrypted_content = f.read()
            decrypted_profile = self.crypto.decrypt(encrypted_content)
            # Validate structure
            self._validate_profile(decrypted_profile)
            return decrypted_profile
        except FileNotFoundError:
            return None
        except (OSError, IOError):
            return None
        except jsonschema.ValidationError:
            # Profile structure is invalid (corrupted or tampered)
            return None
        except Exception:
            # Decryption failed (wrong password, corrupted file, etc.)
            return None
    
    def exists(self) -> bool:
        """Check if profile file exists.
        
        Returns:
            True if profile file exists, False otherwise
        """
        return os.path.exists(self._get_profile_path())

