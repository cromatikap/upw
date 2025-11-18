from . import crypto, cfg
import math

def generate(masterkey: str, domain: str) -> str:
    pk = crypto.derive_key_from(masterkey, domain)
    pk_resized = pk[0:cfg.get('passwords_length')]

    counters = dict(digit=0, letter=0)
    password = ''
    for char in pk_resized:
        if char.isdigit():
            password += process_digit(char, counters["digit"])
            counters["digit"] += 1
        else:
            password += process_letter(char, counters["letter"])
            counters["letter"] += 1

    return password

def process_letter(letter: str, n: int) -> str:
    # Uppercase each 2 letters
    if n % 2 == 1:
        return letter.upper()
    else:
        return letter

def process_digit(digit: str, n: int) -> str:
    # replace each 2 digits by the next special character from the config.yml list
    if n % 2 == 1:
        special_char_list = cfg.get("spec_char_list")
        return special_char_list[math.ceil(n / 2) - 1]
    else:
        return digit
