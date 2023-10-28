import getpass, os, sys, clipboard
from sample import cfg, password
from .DomainCompleter import DomainCompleter
from .User import User
from prompt_toolkit import prompt

def identify():

    print('- 1. Identification -\n')
    print('Make sure to cover your keyboard from any camera,')
    print('window and any potential eavesdropper.\n')

    Login = input("* Login: ")
    MasterPassword = getpass.getpass(prompt='* Master Password: ', stream = None)
    user = User(Login, MasterPassword)
    MasterPassword = None # Make sure Master Password typed by the user is no longer in memory

    print('\nEmojish: *** [ ' + user.emojish + ' ] ***')
    return user
    # DEBUG:
    # return User('user name', 'masterpassword')

def create(user):
    MasterPasswordConfirmation = getpass.getpass(prompt='', stream = None)
    # if(upw.authenticate(user['login'], MasterPasswordConfirmation)['hash'] == user['hash']):
    if(User(user.login, MasterPasswordConfirmation).hash == user.hash):
        user.save_profile()
        print('\n*** High five ' + user.login + '! ***\n')
        print('* Your encrypted profile has been created:')
        print('\n ' + cfg.get('UPW_DIR') + user.hash + '\n')
    else:
        print('\n* The password doesn\'t match with the first\n  typed in.\n')
        sys.exit(0)

def authenticate(user):

    print('\n- 2. Authentication -\n')
    print('\nEmojish: *** [ ' + user.emojish + ' ] ***\n\n')

    # Is this user has a file in .upw/ ?
    print('* Checking for a matching profile\n  at ' + cfg.get('UPW_DIR') + user.hash + '...')
    if(user.import_profile()):
        print('-> Profile found.')
        print('\n- Welcome back ' + user.login + '! -\n')

    else:
        print('-> Profile not found. Creating a new one...\n  Please confirm your master password:')
        create(user)

def options():
    os.system('clear')
    print('-------------- μPassword: options ---------------')
    print('***                                           ***')
    print('***             Work in progress              ***')
    print('***                     :)                    ***')
    print('***                                           ***')
    print('-------------------------------------------------')
    input('\n-> Press enter to continue...')

def select_domain(user):
    while 1:
        os.system('clear')
        print('-> Type `options` to access your profile options.\n')
        domain = prompt(
            '[ ' + user.emojish + ' ] <' + user.login + '> Domain: ',
            completer=DomainCompleter(user.get_domains())
        )
        if(domain == 'options'):
            options()
        elif(domain == cfg.get('options')['display_domains_list']):
            domains = user.get_domains()
            domains.sort()
            for domain in domains:
                print(domain)
            input('-> Press enter to continue...')
        else:
            clipboard.copy(password.generate(user.masterkey, domain))
            print('\n*** Copied to clipboard. ***\n')
            if(user.add_domain(domain)):
                print('This domain has been added to your profile!\n')
            print('-> Type `delete` to remove ' + domain + ' from your profile.')
            print('-> Press enter to continue.')
            keypress = input()
            if(keypress == 'delete'):
                user.del_domain(domain)
                print('profile deleted')
