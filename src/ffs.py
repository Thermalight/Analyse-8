from multiprocessing import Event
import os
from checksum import check_id
from id_generator import generate_id
from users import Advisor, System_Admin, Super_Admin
from getpass import getpass
from validator import validate_username, validate_password
from database import Database
import log


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def user_info():
    print("Your username:")
    print("""
    ○ must be unique and have a length of at least 6 characters
    ○ must be no longer than 10 characters
    ○ must be started with a letter
    ○ can contain letters (a-z), numbers (0-9), underscores (_), apostrophes ('), and periods (.)
    ○ no distinguish between lowercase or uppercase letters
""")
    
def pass_info():
    print("Your password:")
    print("""    
    ○ must have a length of at least 8 characters
    ○ must be no longer than 30 characters
    ○ can contain letters (a-z), (A-Z), numbers (0-9), 
      Special characters such as ~!@#$%&_-+=`|\()\{\}[]:;'<>,.?/
""")

running = True
logged_in = False
change_password = False
state = -1
db = Database()


## SET THIS TO TRUE TO SKIP LOGIN ##
DEBUG = False
if DEBUG:
    user = Super_Admin("superadmin")
    logged_in = True
## END OF DEBUG SECTION ##


# main loop
while running:
    count = 3
    while not logged_in:
        clear()
        # set login variables
        if state == -1:
            valid_username = False
            valid_password = False
            state = 0
        
        if state == 0:
            clear()
            user_info()
            username = input("Please enter your username: ")
            if validate_username(username) and db.user_exists(username):
                valid_username = True
                state = 1
        
        if state == 1:
            clear()
            pass_info()
            print("Your password will be invisible in the terminal")
            print("Enter an empty password to go back")
            print(f"You have {count} tries remaining")
            if count <= 0:
                log.Logger().add_log(log.Event(f"Failed login", "-", f"Someone failed thrice to login to account {username}, their last password was {password}", "true"))
                input("You have run out of attempts press [Enter] to quit")
                exit()
            count -= 1
            password = getpass("Please enter your password: ")

            if password == "":
                state = 0
                valid_password = False
                valid_username = False
                continue

            if validate_password(password) and db.login(username, password):
                valid_password = True
                state = 2
                
        if state == 2:
            if valid_password and valid_username: # check if 
                logged_in = True
                change_password = password == "TempPass123!"
                    
                password = None

                role = db.get_role(username)
                if role == "advisor":
                    user = Advisor(username)
                elif role == "systemadmin":
                    user = System_Admin(username)
                elif role == "superadmin":
                    user = Super_Admin(username)
                else: # if user does not have an existing role
                    logged_in = False
                    running = False
                    print("Role error")
                    break

                username = None
                

    while logged_in:
        # if the user has a temp password
        clear()
        if change_password:
            print("Your password has been set to a temp password, type your new password below")
            user.update_password()
            change_password = False
        # main loop
        clear()
        print(f"You are now logged in as {user.name.lower()}")
        user.welcome()
        print("Enter the character(s) in the brackets to select that option")
        print("-----------")
        print("[Q] - quit")
        print("[L] - log out")

        user.print_options()
        print("-----------")

        user_input = input("Select your option: ")

        if user_input.lower() == "q":
            logged_in = False
            running = False
            state = -1

        if user_input.lower() == "l":
            logged_in = False
            state = -1
            
        else:
            user.handle_input(user_input.lower())
            input("Press [ENTER] to continue")