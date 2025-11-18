# Code Analysis: upw (MicroPassword)

## Executive Summary

**upw** is a deterministic password manager that generates site-specific passwords from a master password and domain name. The project is functional but has several security concerns, code quality issues, and areas for improvement.

**Overall Assessment**: ⚠️ **Needs Improvement**
- ✅ Core functionality works
- ✅ Deterministic design (hardcoded salts are intentional for recovery)
- ⚠️ Security model relies on master password strength (needs documentation)
- ⚠️ Code quality issues (error handling, resource management)
- ⚠️ Limited test coverage
- ✅ Good use of cryptography library

---

## 1. Architecture Overview

### Project Structure
```
upw/
├── upw.py              # Main entry point
├── sample/             # Core modules
│   ├── prompt.py       # CLI interface
│   ├── User.py         # User profile management
│   ├── password.py     # Password generation
│   ├── Crypto.py       # Encryption/decryption
│   ├── cfg.py          # Configuration loader
│   └── DomainCompleter.py  # Autocomplete
├── tests/              # Unit tests
├── config.yml          # Configuration
└── requirements.txt    # Dependencies
```

### Data Flow
1. **User Input** → Login + Master Password
2. **Key Derivation** → PBKDF2 (login + master password) → masterkey
3. **Profile Hash** → SHA256(login + masterkey) → user profile identifier
4. **Domain Password** → PBKDF2(masterkey + domain) → formatted password
5. **Profile Storage** → Encrypted JSON (Fernet) → `.upw/{hash}`

---

## 2. Security Analysis

### 🔴 Critical Issues

#### 2.1 Hardcoded Salts (By Design)

**Password Generation Salt** (config.yml line 9):
```yaml
salt: 'upw'
```
Used in `derive_key_from()` for password generation - **MUST be fixed** for determinism.

**Encryption Salt** (Crypto.py line 18):
```python
salt=b'J\xfd7\xa8\x91#bL\xcbY\x9d<\xdd}\xa4f',
```
Used for Fernet encryption key derivation - **Also fixed by design**.

**Analysis**: 
- ✅ **This is correct** for a deterministic password manager (like MasterPassword/mpw)
- ✅ Allows password recovery on any device without the profile file
- ✅ Security model relies entirely on master password strength
- ⚠️ Trade-off: Determinism vs. per-user salt security
- ⚠️ **Requires strong master passwords** - this is the only security factor

**Security Model**:
- Passwords are generated deterministically: `PBKDF2(masterkey + domain, salt='upw')`
- Profile file encryption is deterministic: `Fernet(PBKDF2(masterkey, fixed_salt))`
- Profile file is a convenience cache (domain list), not security-critical
- Actual passwords don't require the profile file to be generated

**Recommendation**: 
- ✅ Keep fixed salts for determinism (current design is correct)
- ⚠️ Document that security relies on master password strength
- ⚠️ Consider adding password strength validation/guidance
- ⚠️ Consider adding iteration count recommendations for master passwords

#### 2.2 File Handling Issues

**User.py - import_profile()** (Line 24):
```python
f = open(cfg.get('UPW_DIR') + self.hash, "r", encoding="utf-8")
content = f.read()
self.profile = self.Crypto.decrypt(content)
f.close()
```
**Issues**:
- File opened in text mode but contains binary data (encrypted bytes)
- No exception handling for decryption failures
- File not closed if exception occurs (though `f.close()` is present)

**User.py - save_profile()** (Line 17):
```python
f = open(cfg.get('UPW_DIR') + self.hash, "wb")
f.write(self.Crypto.encrypt(self.profile))
f.close()
```
**Issues**:
- No exception handling
- File not closed if exception occurs
- No directory creation if `.upw/` doesn't exist

**Recommendation**: Use context managers (`with` statements) and proper error handling.

#### 2.3 Configuration File Loading

**Crypto.py** (Line 9) and **cfg.py** (Line 3):
```python
with open('config.yml', 'r') as file:
    cfg = yaml.safe_load(file)
```
**Issues**:
- Hardcoded path (not relative to script location)
- Loaded at module import time (executed twice)
- No error handling if file missing

**Recommendation**: Use `__file__` for relative paths, load once, add error handling.

#### 2.4 Password in Memory

**prompt.py** (Line 16):
```python
MasterPassword = None  # Make sure Master Password typed by the user is no longer in memory
```
**Issue**: Setting variable to `None` doesn't guarantee memory is cleared. Python strings are immutable and may remain in memory.

**Recommendation**: Use `secrets` module or clear sensitive data more thoroughly.

### ⚠️ Medium Priority Issues

#### 2.5 Weak Error Handling
- No validation of user input
- No handling of decryption failures (wrong password)
- Silent failures in some cases

#### 2.6 Profile File Permissions
- No explicit file permission setting (should be 600 on Unix)
- Profile files readable by other users on system

---

## 3. Code Quality Issues

### 3.1 Resource Management

**Problem**: Files opened without context managers
```python
# Bad
f = open(path, "wb")
f.write(data)
f.close()

# Good
with open(path, "wb") as f:
    f.write(data)
```

**Affected Files**:
- `sample/User.py` (lines 17, 24)

### 3.2 Error Handling

**Issues**:
- Generic `OSError` catch (line 30 in User.py) - should be `FileNotFoundError`
- No validation of decrypted data structure
- No handling of corrupted profile files
- `sys.exit(0)` on password mismatch (line 33) - should use non-zero exit code

### 3.3 Code Organization

**Issues**:
- Configuration loaded multiple times (Crypto.py and cfg.py)
- Mixed responsibilities (User class handles file I/O and business logic)
- No separation of concerns

### 3.4 Type Hints

**Missing**: No type hints except in `DomainCompleter.py`
- Makes code harder to maintain
- No IDE autocomplete support
- No static type checking

### 3.5 Naming Conventions

**Issues**:
- Inconsistent: `Login`, `MasterPassword` (PascalCase) vs `login`, `masterkey` (camelCase)
- Should follow PEP 8 (snake_case for variables)

### 3.6 Magic Numbers and Strings

**Issues**:
- Hardcoded values: `[0:40]` (line 13 User.py), `[0:cfg.get('passwords_length')]` (line 6 password.py)
- String literals: `"domains"` (line 7 User.py)
- Should use constants or config

---

## 4. Algorithm Analysis

### 4.1 Password Generation

**Process**:
1. Derive key: `PBKDF2(masterkey + domain)`
2. Take first 16 hex characters
3. Transform:
   - Letters: Alternate case (every 2nd uppercase)
   - Digits: Replace every 2nd with special char from list

**Issues**:
- **Limited character set**: Only uses hex characters (0-9, a-f)
- **Predictable pattern**: Alternating case/char replacement is deterministic
- **Short passwords**: 16 characters may not meet all requirements
- **No variation**: Same domain always produces same password

**Strengths**:
- Deterministic (good for password manager)
- Uses PBKDF2 (good key derivation)
- Includes special characters

### 4.2 Key Derivation

**PBKDF2 Configuration** (config.yml):
```yaml
hash:
  name: 'sha256'
  salt: 'upw'
  dklen: 100000
```

**Issues**:
- `dklen: 100000` - This is the iteration count, not key length
- Salt is just string 'upw' (should be bytes, more random)
- Key length not specified (uses default)

**Crypto.py** (Line 34):
```python
pk = hashlib.pbkdf2_hmac(hash['name'], key1.encode() + key2.encode(), hash['salt'].encode(), cfg['hash']['dklen'])
```
- `dklen` used as iteration count (confusing naming)
- No explicit key length parameter

---

## 5. Testing Analysis

### Current Test Coverage

**Test Files**:
- `test_Crypto.py` - Basic encryption/decryption, key derivation
- `test_password.py` - Password generation logic
- `test_User.py` - User class functionality

**Coverage Gaps**:
- ❌ No integration tests
- ❌ No tests for file I/O
- ❌ No tests for error cases (corrupted files, wrong passwords)
- ❌ No tests for edge cases (empty domains, special characters)
- ❌ No tests for `prompt.py` (CLI interaction)
- ❌ No tests for `DomainCompleter.py`

**Test Quality**:
- ✅ Tests use unittest framework
- ⚠️ Some tests check internal implementation details (Fernet keys)
- ⚠️ No test fixtures or setup/teardown for file operations
- ⚠️ Hardcoded test values (not parameterized)

---

## 6. Dependencies Analysis

### Current Dependencies
```
pyyaml          # Configuration parsing
pyperclip       # Clipboard operations
prompt_toolkit  # CLI interface
cryptography    # Encryption (Fernet, PBKDF2)
```

### Assessment
- ✅ All dependencies are well-maintained
- ✅ `cryptography` is industry-standard
- ✅ No security vulnerabilities in dependencies (check with `pip-audit`)
- ⚠️ `pyyaml` could be replaced with `ruamel.yaml` for better YAML support

---

## 7. Recommendations

### Priority 1: Security Fixes

1. **Fix file handling** - Use context managers
2. **Add file permissions** - Set 600 on profile files
3. **Improve error handling** - Handle decryption failures gracefully
4. **Fix config loading** - Use relative paths, load once
5. **Add password strength validation** - Guide users to choose strong master passwords
6. **Document security model** - Clarify that security relies on master password strength

### Priority 2: Code Quality

1. **Add type hints** - Improve maintainability
2. **Use context managers** - Proper resource management
3. **Follow PEP 8** - Consistent naming conventions
4. **Separate concerns** - Split file I/O from business logic
5. **Add input validation** - Validate user inputs

### Priority 3: Testing

1. **Increase coverage** - Add tests for file I/O, error cases
2. **Add integration tests** - Test full workflow
3. **Use pytest** - More modern than unittest
4. **Add fixtures** - For test data and cleanup

### Priority 4: Features

1. **Password strength options** - Configurable length/complexity
2. **Export/import** - Backup and restore functionality
3. **Password history** - Track password changes
4. **Better CLI** - Add commands, help text
5. **Logging** - Add proper logging instead of print statements

---

## 8. Code Metrics

### Lines of Code
- Total: ~400 lines
- Core logic: ~250 lines
- Tests: ~80 lines
- Config: ~30 lines

### Complexity
- **Low complexity** - Most functions are simple
- **Good separation** - Clear module boundaries
- **Some coupling** - User class tightly coupled to file system

### Maintainability
- **Moderate** - Code is readable but needs refactoring
- **Documentation** - Minimal docstrings
- **Comments** - Some helpful comments, could use more

---

## 9. Comparison with Best Practices

### ✅ Good Practices
- Uses established cryptography library
- Deterministic password generation
- Encrypted profile storage
- Offline operation (no network dependencies)

### ⚠️ Areas for Improvement
- Error handling
- Resource management
- Security hardening
- Test coverage
- Code organization

---

## 10. Conclusion

The **upw** project demonstrates a solid understanding of deterministic password management concepts (similar to MasterPassword/mpw) and uses appropriate cryptographic primitives. The hardcoded salts are **intentional design choices** for deterministic password recovery, which is correct for this use case.

However, it needs improvements in:

1. **Security**: Improve file handling, add proper error handling, document security model
2. **Code Quality**: Use modern Python practices, add type hints, improve organization
3. **Testing**: Expand test coverage, add integration tests
4. **Documentation**: Add docstrings, document security model and master password requirements

**Estimated Effort for Improvements**: 1-2 days for code quality fixes, 1 week for full refactoring.

**Risk Level**: Low-Medium - Functional and correctly implements deterministic password generation. Security relies on master password strength, which should be clearly documented to users.

