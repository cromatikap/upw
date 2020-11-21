
import getpass, os, sys, clipboard
from sample import upw, cfg, password, data, lib
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter

def identify():

    print('- 1. Identification -\n')
    print('Make sure to cover your keyboard from any camera,')
    print('window and any potential eavesdropper.\n')

    Login = input("* Login: ")
    MasterPassword = getpass.getpass(prompt='* Master Password: ', stream = None)
    user = upw.authenticate(Login, MasterPassword)
    MasterPassword = None # Make sure Master Password typed by the user is no longer in memory

    print('\nEmojish: *** [ ' + user['emojish'] + ' ] ***')
    return user
    # DEBUG:
    # return upw.authenticate('user name', 'masterpassword')

def create(user):
    print('\n* Please confirm the master password you typed')
    print('  before.\n')
    print('* login: ' + user['login'])
    MasterPasswordConfirmation = getpass.getpass(prompt='* Master Password: ', stream = None)
    if(upw.authenticate(user['login'], MasterPasswordConfirmation)['hash'] == user['hash']):
        data.createUser(user)
        print('\n*** High five ' + user['login'] + '! ***\n')
        print('* Your encrypted profile has been created:')
        print('\n ' + cfg.get('UPW_DIR') + user['hash'] + '\n')
    else:
        print('\n* The password doesn\'t match with the first\n  typed in.\n')
        sys.exit(0)

def authenticate(user):

    print('\n- 2. Authentication -\n')
    print('\nEmojish: *** [ ' + user['emojish'] + ' ] ***\n\n')

    # Is this user has a file in .upw/ ?
    if(data.isUserExists(user)):
        print('* A matching profile has been found: ')
        print('\n ' + cfg.get('UPW_DIR') + user['hash'])
        print()

    else:
        print('-------------- Welcome to μPassword -------------')
        print('***                                           ***')
        print('***           You are about to create         ***')
        print('***      a new login/master password pair     ***')
        print('***                                           ***')
        print('-------------------------------------------------')
        print()
        print('* If this is what you want, type `confirm` below')
        print()
        print('* If you\'re trying to authenticate with a login')
        print('  you\'ve already made before on this device, you')
        print('  likely mistyped your master password.')
        print('  Just press [Enter] :)')
        print()
        if(input('> ') == 'confirm'):
            create(user)
        else:
            sys.exit(0)

def options(user):
    print('options menu')
    input('DEBUG Press enter to continue...')

def select_domain(user):
    html_completer = WordCompleter(
        ['options', 'facebook.com', 'twitter.com', 'linkedin.com', 'gmail.com', 'elektr.io']
    )

    while 1:
        os.system('clear')
        print('Type `options` to access your profile options.\n')
        domain = prompt('[ ' + user['emojish'] + ' ] <' + user['login'] + '> Domain: ',
            history=FileHistory(cfg.get('UPW_DIR') + 'history.txt'),
            auto_suggest=AutoSuggestFromHistory(),
            completer=html_completer
            )
        if(domain == 'options'):
            options(user)
        else:
            clipboard.copy(password.generate(user['masterkey'], domain))
            print('* Copied to clipboard.')
            print('Type `delete` to remove ' + domain + ' from your profile.')
            print('Press enter to continue...')
            keypress = input()
            if(keypress == 'delete'):
                print('profile deleted')
