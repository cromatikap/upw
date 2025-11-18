import getpass
import os
import sys
import pyperclip
import secrets
from sample import cfg, password, crypto
from .domain_completer import DomainCompleter
from .user import User
from prompt_toolkit import prompt


def _secure_wipe(data: bytearray) -> None:
    """Securely clear sensitive bytearray data from memory.
    
    This function overwrites the bytearray's memory contents with random data
    and then zeros. Since bytearray is mutable, this actually modifies the
    memory containing the sensitive data.
    
    Args:
        data: The mutable bytearray to clear
    """
    if data:
        # Overwrite with random bytes multiple times
        for _ in range(100000):
            data[:] = secrets.token_bytes(len(data))

def identify() -> User:

    print('- 1. Identification -\n')
    print('Make sure to cover your keyboard from any camera,')
    print('window and any potential eavesdropper.\n')

    login = input("* Login: ")
    
    master_password_bytes = bytearray(getpass.getpass(prompt='* Master Password: ', stream=None).encode('utf-8'))
    masterkey = crypto.derive_key_from(login.encode('utf-8'), master_password_bytes)
    _secure_wipe(master_password_bytes)
    del master_password_bytes
    
    user = User(login, masterkey)

    print('\nEmojish: *** [ ' + user.emojish + ' ] ***')
    return user

def create(user: User) -> None:
    master_password_confirmation_bytes = bytearray(getpass.getpass(prompt='', stream=None).encode('utf-8'))
    masterkey_confirmation = crypto.derive_key_from(
        user.login.encode('utf-8'), 
        master_password_confirmation_bytes
    )
    
    _secure_wipe(master_password_confirmation_bytes)
    del master_password_confirmation_bytes
    
    if masterkey_confirmation == user.masterkey:
        user.save_profile()
        print('\n*** High five ' + user.login + '! ***\n')
        print('* Your encrypted profile has been created:')
        print('\n ' + cfg.get('UPW_DIR') + user.hash + '\n')
    else:
        print('\n* The password doesn\'t match with the first\n  typed in.\n')
        sys.exit(1)

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
