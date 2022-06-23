import datetime
from turtle import back
import validator
import database
import zipfile
import os
import log

db = database.Database()
l = log.Logger()

BACKUP_FOLDER = "./backups"

class Advisor():
    def __init__(self, username):
        self.name = username
        self.registration_date = int(datetime.datetime.now().timestamp())
    
    def welcome(self):
        print(f"Welcome {type(self).__name__}")
    
    def register_member(self):
        firstname = input("Please enter a firstname for the member: ")
        lastname = input("Please enter a lastname for the member: ")
        street = input("Enter street name: ")
        options = """
[0] - city_a
[1] - city_b
[2] - city_c
[3] - city_d
[4] - city_e
[5] - city_f
[6] - city_g
[7] - city_h
[8] - city_i
[9] - city_j
              """
        print(options)
        
        city = ""
        while city not in "0123456789" or len(city) != 1:
            city = input("Enter the number in the brackets to select your city: ")
            
        city = f"city_{chr(ord('a') + int(city))}"
        
        housenumber = input("Enter housenumber: ")
        
        zipcode = ""
        while not validator.validate_zip(zipcode):
            zipcode = input("Enter zipcode: ")
        
        phone = ""
        while not validator.validate_phone(phone):
            phone = input("Enter the last 8 digits of your phone number: +31 6 ")
            
        email = ""
        while not validator.validate_email(email):
            email = input("Enter an e-mail address: ")
            
        db.add_member(firstname, lastname, street, housenumber, zipcode, city, email, f"+31 6 {phone}")
        print(f"Member {firstname} {lastname} added to the database")
    
    def modify_member(self):
        member_id = input("Please enter the ID of the member you wish to modify: ")
        if not validator.validate_id(member_id) or not db.member_exists(member_id):
            print("That member doesn't exist")
            return
        firstname = input("Please enter a firstname for the member: ")
        lastname = input("Please enter a lastname for the member: ")
        street = input("Enter street name: ")
        options = """
[0] - city_a
[1] - city_b
[2] - city_c
[3] - city_d
[4] - city_e
[5] - city_f
[6] - city_g
[7] - city_h
[8] - city_i
[9] - city_j
              """
        print(options)
        
        city = ""
        while city not in "0123456789" or len(city) != 1:
            city = input("Enter the number in the brackets to select your city: ")
            if city == "":
                break
        
        if city != "":
            city = f"city_{chr(ord('a') + int(city))}"
        
        housenumber = input("Enter housenumber: ")
        
        zipcode = ""
        while not validator.validate_zip(zipcode):
            zipcode = input("Enter zipcode: ")
            if zipcode == "":
                break
        
        phone = ""
        while not validator.validate_phone(phone):
            phone = input("Enter the last 8 digits of your phone number: +31 6 ")
            if phone == "":
                break
        if phone != "":
            phone = "+31 6 " + phone
            
        email = ""
        while not validator.validate_email(email):
            email = input("Enter an e-mail address: ")
            if email == "":
                break
        
        db.update_member(int(member_id), firstname,lastname,street,housenumber,zipcode,city,email,phone)
        print("Member has been updated")

    def search_member(self):
        query = input("Enter filter (none to see all): ").lower()
        print(f"-------------------")
        for mem in db.get_members():
            found = False
            if query != "":
                for item in mem:
                    if query in str(item):
                        found = True
            else:
                found = True
                
            if found:
                print(f"Id: {mem[0]}")
                print(f"Firstname: {mem[1]}")
                print(f"Lastname: {mem[2]}")
                print(f"Street: {mem[3]}")
                print(f"Housenumber: {mem[4]}")
                print(f"Zipcode: {mem[5]}")
                print(f"City: {mem[6]}")
                print(f"Email: {mem[7]}")
                print(f"Phone: {mem[8]}")
                print(f"Registration: {mem[9]}")
                print(f"-------------------")
        print("End of list")
        
    def update_password(self):
        while not validator.validate_password(new_pass := input("Enter your new password: ")):
            pass
        
        db.update_password(self.name, new_pass)
        print("Password has been updated")
        

    def print_options(self):
        print("[1] - register member")
        print("[2] - modify member")
        print("[3] - search member")
        print("[4] - update password")
        
    def handle_input(self, option):
        match option:
            case "1":
                self.register_member()
            case "2":
                self.modify_member()
            case "3":
                self.search_member()
            case "4":
                self.update_password()

    

class System_Admin(Advisor):
    def __init__(self, username):
        super().__init__(username)
        
    def welcome(self):
        super().welcome()
        print(f"You have {self.unread_log_count()} unread sussy log files to read")

    def unread_log_count(self) -> int:
        return 0
        pass
    
    def add_advisor(self):
        firstname = input("Please enter a firstname for the advisor: ")
        lastname = input("Please enter a lastname for the advisor: ")
            
        username = ""
        while not validator.validate_username(username) and not db.user_exists(username):
            username = input("Please enter a username for the advisor: ")
            
        password = ""
        while not validator.validate_password(password):
            password = input(f"Please enter a password for {firstname} {lastname}: ")
            
        db.add_user(username, password, firstname, lastname, "advisor")
        print(f"Advisor {firstname} {lastname} added to the database")

    def modify_advisor(self):
        name = input("Enter the username of the adviser to modify: ")
        if validator.validate_username(name) and db.user_exists(name) and db.get_role(name) == "advisor":
            print("Enter new information, leave empty to keep current value")
            new_username = input("Enter new username: ")
            while new_username != "" and (not validator.validate_username(new_username) or db.user_exists(new_username)):
                new_username = input("Enter new username: ")
            new_firstname = input("Enter new firstname: ")
            new_lastname = input("Enter new firstname: ")
            
            db.update_user(name ,new_username, new_firstname, new_lastname)
            
            
        else:
            print("Adviser with that username does not exist")
        pass

    def delete_advisor(self):
        username = input("Enter the username of the advisor: ")
        
        if validator.validate_username(username) and db.get_role(username) == "advisor":
            if db.user_exists(username):
                db.delete_user(username)
                print("Advisor deleted")
            else:
                print("User not found")
        else:
            print(f"Advisor {username} doesn't exist")
        
    def delete_member(self):
        Id = input("Enter the ID of the member: ")
        for i in Id:
            if i not in "0123456789":
                print("only enter digits")
                return
        Id = int(Id)
        
        if validator.validate_id(Id):
            if db.member_exists(Id):
                db.delete_member(Id)
                print("Member deleted")
            else:
                print("Member not found")
        else:
            print(f"Member with ID {Id} doesn't exist")
            
    def reset_advisor_password(self):
        name = input("Enter the username of the advisor to reset their password: ")
        if not validator.validate_username(name) or not db.user_exists(name) or not db.get_role(name) == "advisor":
            print("This user does not exist")
            return
        
        db.update_password(name, "TempPass123!") 
        print("Their password has been reset to TempPass123!")
        print("They will be prompted to change their password on login")
        
    def create_backup(self):
        log.Logger().add_log(log.Event(f"Backup created", f"{self.name}", f"{self.name} created a backup", "false"))
        if not os.path.exists(BACKUP_FOLDER):
            os.mkdir(BACKUP_FOLDER)
        
        with zipfile.ZipFile(BACKUP_FOLDER + "/" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".zip", mode="w") as archive:
            archive.write("Users.db")
            archive.write("log.txt")
            
    def load_backup(self):
        files = os.listdir(BACKUP_FOLDER)
        for idx,file in enumerate(files):
            print(f"[{idx}] - {file}")
        
        option = input("Which one you want?: ")
        if False in [char in "1234567890" for char in option] or option == "" or int(option) >= len(files):
            print("Invalid option")
            return
        
        log.Logger().add_log(log.Event(f"Backup restored", f"{self.name}", f"{self.name} restored a backup", "false"))
        with zipfile.ZipFile(BACKUP_FOLDER + "/" + files[int(option)], 'r') as archive:
            archive.extractall()
        log.Logger().add_log(log.Event(f"Backup restored", f"{self.name}", f"{self.name} restored a backup", "false"))

    def check_users(self):
        query = input("Enter filter (none to see all): ").lower()
        print(f"-------------------")
            
        for user in db.get_users():
            found = False
            if query != "":
                for item in user:
                    if query in str(item):
                        found = True
            else:
                found = True
                
            if found:
                print(f"Username: {user[0]}")
                print(f"Firstname: {user[2]}")
                print(f"Lastname: {user[3]}")
                print(f"Role: {user[4]}")
                print(f"Registration: {user[5]}")
                print(f"-------------------")
                
        log.Logger().add_log(log.Event(f"Users requested", f"{self.name}", f"{self.name} looked up users with keyword='{query}'", "false"))
        
    # TODO: check_logs
    def check_logs(self):
        log.Logger().add_log(log.Event(f"Users requested the logs", f"{self.name}", f"{self.name} looked up the logs", "false"))
        l.show_log()
        
    def print_options(self):
        super().print_options()
        print("[5] - add advisor")
        print("[6] - modify advisor")
        print("[7] - delete advisor")
        print("[8] - delete member")
        print("[9] - reset advisor password")
        print("[10] - create backup")
        print("[11] - load backup")
        print("[12] - check logs")
        print("[13] - check users")
        
    def handle_input(self, option):
        super().handle_input(option)
        match option:
            case "5":
                self.add_advisor()
            case "6":
                self.modify_advisor()
            case "7":
                self.delete_advisor()
            case "8":
                self.delete_member()
            case "9":
                self.reset_advisor_password()
            case "10":
                self.create_backup()
            case "11":
                self.load_backup()
            case "12":
                self.check_logs()
            case "13":
                self.check_users()

class Super_Admin(System_Admin):
    def __init__(self, username):
        super().__init__(username)
        
    def welcome(self):
        super().welcome()
        
    def create_system_admin(self):
        firstname = input("Please enter a firstname for the system admin: ")
        lastname = input("Please enter a lastname for the system admin: ")
            
        username = ""
        while not validator.validate_username(username) and not db.user_exists(username):
            username = input("Please enter a username for the system admin: ")
            
        password = ""
        while not validator.validate_password(password):
            password = input(f"Please enter a password for {firstname} {lastname}: ")
            
        db.add_user(username, password, firstname, lastname, "systemadmin")
        print(f"system admin {firstname} {lastname} added to the database")
    
    def modify_system_admin(self):
        name = input("Enter the username of the adviser to modify: ")
        
        if validator.validate_username(name) and db.user_exists(name) and db.get_role(name) == "systemadmin":
            print("Enter new information, leave empty to keep current value")
            new_username = input("Enter new username: ")
            while new_username != "" and (not validator.validate_username(new_username) or db.user_exists(new_username)):
                new_username = input("Enter new username: ")
            new_firstname = input("Enter new firstname: ")
            new_lastname = input("Enter new firstname: ")
            
            db.update_user(name ,new_username, new_firstname, new_lastname)
            
            
        else:
            print("System admin with that username does not exist")
        pass

    def delete_system_admin(self):
        username = input("Enter the username of the advisor: ")
        
        if validator.validate_username(username) and db.get_role(username) == "systemadmin":
            if db.user_exists(username):
                db.delete_user(username)
                print("System admin deleted")
            else:
                print("User not found")
        else:
            print(f"System admin {username} doesn't exist")

    def reset_system_admin_password(self):
        name = input("Enter the username of the system admin to reset their password: ")
        if not validator.validate_username(name) or not db.user_exists(name) or not db.get_role(name) == "systemadmin":
            print("This user does not exist")
            return
        
        db.update_password(name, "TempPass123!") 
        print("Their password has been reset to TempPass123!")
        print("They will be prompted to change their password on login")

    def print_options(self):
        super().print_options()
        print("[14] - create system admin")
        print("[15] - modify system admin")
        print("[16] - delete system admin")
        print("[17] - reset system admin password")
        
    def handle_input(self, option):
        super().handle_input(option)
        match option:
            case "14":
                self.create_system_admin()
            case "15":
                self.modify_system_admin()
            case "16":
                self.delete_system_admin()
            case "17":
                self.reset_system_admin_password()
    

class Member():
    def __init__(self, first_name, last_name, house_number, zipcode, city, email, phone_number):
        self.first_name = first_name
        self.last_name = last_name
        self.house_number = house_number
        self.zipcode = zipcode
        self.city = city
        self.email = email
        self.phone_number = phone_number