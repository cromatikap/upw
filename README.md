# MicroPassword: `upw`

## The simplestm, fastest and most secure password manager in the world

- pure cryptography only
- offline
- trustless
- confidential UX

Inspired from MasterPassword (`mpw`). Written in python.

# Derive website compliant passwords from your master password and the domain name

upw provides a keys derivation tree from a login (confidential key) and a master password (secret key)

## domain passwords format

- 16 first characters sliced from the derived hash (masterkey + domain name)
- Letter chars alternate from lowercase to uppercase
- 1 digit on 2 is replaced by a special char from `spec_char_list` in `config.yml` following the array order reading

Example:
dC7b#5D%0b$8^Ac8
d3E#1%3aB$9^aDa6
2fD#4f%E7cD$3^7b

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

See more in `config.yaml`

# Run instructions

```
$ pip install -r requirements.txt
$ python main.py
```
