from . import upw, cfg
import math

def generate(masterkey, domain):
    pk = upw.derive_key_from(masterkey, domain)
    pkResized = pk[0:cfg.get('passwords_length')]

    c = dict(digit=0, letter=0)
    password = ''
    for char in pkResized:
        if char.isdigit():
            password += process_digits(char, c["digit"])
            c["digit"] += 1
        else:
            password += process_letters(char, c["letter"])
            c["letter"] += 1

    return password

def process_letters(letter, c):
    # Uppercase each 2 letters
    if c % 2 == 1:
        return letter.upper()
    else:
        return letter

def process_digits(digit, c):
    # replace each 2 digits by the next special character from the config.yml list
    if c % 2 == 1:
        specialCharList = cfg.get("spec_char_list")
        return specialCharList[math.ceil(c / 2) - 1]
    else:
        return digit
