import os
from sample import prompt
from sample.user import User

os.environ["XDG_SESSION_TYPE"] = "" # Prevent warning related to clipboard and Wayland on Gnome

def main() -> None:
    print('upw-0.1.0')
    print()

    user: User | None = None
    try:
        user = prompt.identify()
        os.system('clear')
        prompt.authenticate(user)
        input("Press Enter to continue...")
        prompt.select_domain(user)

    except KeyboardInterrupt:
        os.system('clear')
        if user is not None:
            user.update_profile()
        print('\n* Bye.')

if __name__ == "__main__":
    main()
