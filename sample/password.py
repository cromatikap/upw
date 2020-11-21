from . import upw, cfg
import math

def generate(masterkey, domain):
    pk = upw.deriveKeyFrom(masterkey, domain)
    pkResized = pk[0:cfg.get('passwords_length')]

    c = Counters()
    password = ''
    for char in pkResized:
        if char.isdigit():
            password += processDigit(char, c.digit)
            c.digit += 1
        else:
            password += processLetter(char, c.letter)
            c.letter += 1

    return password

def processLetter(letter, c):
    # Uppercase each 2 letters
    if c % 2 == 1:
        return letter.upper()
    else:
        return letter

def processDigit(digit, c):
    # replace each 2 digits by the next special character from the config.yml list
    if c % 2 == 1:
        specialCharList = cfg.get("spec_char_list")
        return specialCharList[math.ceil(c / 2) - 1]
    else:
        return digit

class Counters:
    def __init__(self):
        self.digit = 0
        self.letter = 0
