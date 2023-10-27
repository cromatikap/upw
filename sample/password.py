from . import Crypto, cfg
import math

def generate(masterkey, domain):
    pk = Crypto.derive_key_from(masterkey, domain)
    pkResized = pk[0:cfg.get('passwords_length')]

    counters = dict(digit=0, letter=0)
    password = ''
    for char in pkResized:
        if char.isdigit():
            password += process_digit(char, counters["digit"])
            counters["digit"] += 1
        else:
            password += process_letter(char, counters["letter"])
            counters["letter"] += 1

    return password

def process_letter(letter, n):
    # Uppercase each 2 letters
    if n % 2 == 1:
        return letter.upper()
    else:
        return letter

def process_digit(digit, n):
    # replace each 2 digits by the next special character from the config.yml list
    if n % 2 == 1:
        specialCharList = cfg.get("spec_char_list")
        return specialCharList[math.ceil(n / 2) - 1]
    else:
        return digit
