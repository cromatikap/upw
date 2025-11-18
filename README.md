# MicroPassword: `upw`

## Simple, discreet and secure passwords manager

- off-line
- no third-party involved
- passwords recoverable from any device with upw installed on
- confidential CLI

Inspired from MasterPassword (`mpw`). Written in python.

# Derive website compliant passwords from your master password and the domain name

upw provides a keys derivation tree from a login (confidential key) and a master password (secret key)

## domain passwords format

- 16 first characters sliced from the derived hash (masterkey + domain name)
- Letter chars alternate from lowercase to uppercase
- 1 digit on 2 is replaced by a special char from `spec_char_list` in `config.yml` following the array order reading

Example:
- dC7b#5D%0b$8^Ac8
- d3E#1%3aB$9^aDa6
- 2fD#4f%E7cD$3^7b

## Derivation tree:

```
Login + Master Password (Example: user + pwd)
  |- filename (hash function)
  |- masterkey (7e12c57de7836db62089f04ae02ea7de057ae49face85e657fabdfd0f2b12547)
  `- masterkey + domain (7e12c57de7836db62089f04ae02ea7de057ae49face85e657fabdfd0f2b12547 + facebook.com)
    `- domain password: 5#4d%0$3^2@Ec3F?
```

## Algorithms used for critical computations

- Keys derivation: `hashlib.pbkdf2_hmac`
- User profile file encryption: `cryptography.fernet`

See more in `config.yaml`

## Security Model

### Deterministic Password Generation

**upw** is a deterministic password manager, meaning it generates the same password for the same domain and master password combination every time. This design allows you to:

- ✅ Recover passwords on any device without syncing files
- ✅ Regenerate passwords even if you lose your profile file
- ✅ Use passwords across multiple devices without cloud sync

### How Security Works

**Security relies entirely on your master password strength.** This is the only secret you need to protect.

1. **Master Key Derivation**: Your master key is derived from your login and master password using PBKDF2 with a fixed salt. The fixed salt ensures deterministic key generation across devices.

2. **Password Generation**: Domain-specific passwords are generated using:
   ```
   PBKDF2(masterkey + domain, salt='upw', iterations=100000)
   ```
   The fixed salt `'upw'` ensures the same domain always produces the same password.

3. **Profile File**: The `.upw/{hash}` profile file is an encrypted convenience cache that stores your domain list. It is **not required** to generate passwords - you can regenerate all passwords with just your login and master password.

### Important Security Considerations

⚠️ **Master Password Requirements**:
- Use a **strong, unique master password** - this is your only security factor
- Consider using a passphrase (multiple words) for better security
- Never reuse your master password for other accounts
- The security of all your generated passwords depends on this single secret

⚠️ **Fixed Salts (By Design)**:
- The hardcoded salts in the code are **intentional** and **correct** for deterministic password generation
- They enable password recovery without the profile file
- This is the same security model used by MasterPassword (`mpw`) and similar deterministic password managers
- Trade-off: Determinism vs. per-user salt security (acceptable for this use case)

✅ **What Makes This Secure**:
- Uses industry-standard PBKDF2 for key derivation (100,000 iterations)
- Uses Fernet (symmetric encryption) for profile file encryption
- No network dependencies - completely offline
- No third-party services - you control all data
- Profile files are encrypted (though not required for password generation)

### Password Recovery

If you lose your profile file or switch devices:
1. Install `upw` on the new device
2. Enter the same login and master password
3. All passwords will be regenerated identically

**You only need to remember**:
- Your login (confidential key)
- Your master password (secret key)

The profile file is optional and only speeds up domain autocompletion.

# Run instructions

```
$ source env/bin/activate
$ pip3 install -r requirements.txt
$ python3 upw.py
```

# Unit test

```
$ python3 -m unittest
```
