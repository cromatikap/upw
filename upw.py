import sys, os
from sample import prompt

os.environ["XDG_SESSION_TYPE"] = "" # Prevent warning related to clipboard and Wayland on Gnome

print('upw-0.1.0')
print()

try:
    user = prompt.identify()
    os.system('clear')
    prompt.authenticate(user)
    input("Press Enter to continue...")
    prompt.select_domain(user)

except KeyboardInterrupt:
    os.system('clear')
    print('\n* Bye.')
