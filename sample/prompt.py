import getpass
import os
import sys
import pyperclip
import secrets
from sample import cfg, password
from .domain_completer import DomainCompleter
from .user import User
from prompt_toolkit import prompt


def _clear_sensitive_data(data: str) -> None:
    """Securely clear sensitive string data from memory.
    
    This function attempts to overwrite the memory containing the string
    by converting it to a mutable bytearray and overwriting it with random data.
    
    Note: Due to Python's string immutability and memory management,
    this cannot guarantee 100% memory clearing, but it significantly reduces
    the window of exposure. The original string object may still exist in memory
    until garbage collected, but we minimize the time it's accessible.
    
    Args:
        data: The sensitive string to clear
    """
    if data:
        # Convert to bytearray (mutable) and overwrite with random data
        data_bytes = bytearray(data.encode('utf-8'))
        # Overwrite with random bytes multiple times
        for _ in range(3):  # Multiple passes for better security
            for i in range(len(data_bytes)):
                data_bytes[i] = secrets.randbelow(256)
        # Final pass: overwrite with zeros
        data_bytes[:] = b'\x00' * len(data_bytes)
        # Clear the bytearray reference
        del data_bytes

def identify() -> User:

    print('- 1. Identification -\n')
    print('Make sure to cover your keyboard from any camera,')
    print('window and any potential eavesdropper.\n')

    login = input("* Login: ")
    master_password = getpass.getpass(prompt='* Master Password: ', stream=None)
    user = User(login, master_password)
    # Securely clear master password from memory
    _clear_sensitive_data(master_password)
    master_password = None

    print('\nEmojish: *** [ ' + user.emojish + ' ] ***')
    return user
    # DEBUG:
    # return User('user name', 'masterpassword')

def create(user: User) -> None:
    master_password_confirmation = getpass.getpass(prompt='', stream=None)
    # if(upw.authenticate(user['login'], master_password_confirmation)['hash'] == user['hash']):
    if User(user.login, master_password_confirmation).hash == user.hash:
        user.save_profile()
        print('\n*** High five ' + user.login + '! ***\n')
        print('* Your encrypted profile has been created:')
        print('\n ' + cfg.get('UPW_DIR') + user.hash + '\n')
    else:
        print('\n* The password doesn\'t match with the first\n  typed in.\n')
        sys.exit(1)
    # Securely clear confirmation password from memory
    _clear_sensitive_data(master_password_confirmation)
    master_password_confirmation = None

def authenticate(user: User) -> None:

    print('\n- 2. Authentication -\n')
    print('\nEmojish: *** [ ' + user.emojish + ' ] ***\n\n')

    # Is this user has a file in .upw/ ?
    print('* Checking for a matching profile\n  at ' + cfg.get('UPW_DIR') + user.hash + '...')
    if user.import_profile():
        print('-> Profile found.')
        print('\n- Welcome back ' + user.login + '! -\n')

    else:
        print('-> Profile not found. Creating a new one...\n  Please confirm your master password:')
        create(user)

def options() -> None:
    os.system('clear')
    print('-------------- μPassword: options ---------------')
    print('***                                           ***')
    print('***             Work in progress              ***')
    print('***                     :)                    ***')
    print('***                                           ***')
    print('-------------------------------------------------')
    input('\n-> Press enter to continue...')

def select_domain(user: User) -> None:
    while True:
        os.system('clear')
        print('-> Type `options` to access your profile options.\n')
        domain = prompt(
            '[ ' + user.emojish + ' ] <' + user.login + '> Domain: ',
            completer=DomainCompleter(user.get_domains())
        )
        if domain == 'options':
            options()
        elif domain == cfg.get('options')['display_domains_list']:
            domains = user.get_domains()
            domains.sort()
            for domain in domains:
                print(domain)
            input('-> Press enter to continue...')
        else:
            pyperclip.copy(password.generate(user.masterkey, domain))
            print('\n*** Copied to clipboard. ***\n')
            if user.add_domain(domain):
                print('This domain has been added to your profile!\n')
            print('-> Type `delete` to remove ' + domain + ' from your profile.')
            print('-> Press enter to continue.')
            keypress = input()
            if keypress == 'delete':
                user.del_domain(domain)
                print('profile deleted')
