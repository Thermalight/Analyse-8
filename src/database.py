import sqlite3
import hasher
import log
import datetime
import id_generator

def add_logging(func):
    pogger = log.Logger()
    def wrapper(*args):
        e = log.Event(func.__name__, args[0].name, func.__doc__)
        pogger.add_log(e)
        func(*args)
    
    return wrapper

# Settings: 
_database_filename = "users.db" 

class Database:
    def __init__(self):
        self.db_name = _database_filename
        
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        
        db_ready = False
        
        cur.execute("CREATE TABLE IF NOT EXISTS Users (Username TEXT, Password TEXT, Firstname TEXT, Lastname TEXT, Role TEXT, Registration INTEGER)")
        cur.execute("CREATE TABLE IF NOT EXISTS Members (Id INTEGER, Firstname TEXT, Lastname TEXT, Street TEXT, Housenumber TEXT, Zipcode TEXT, City TEXT, Email TEXT, Phonenumber TEXT, Registration INTEGER)")
        
        for row in cur.execute("SELECT * FROM Users"):
            if hasher.encrypt("superadmin") in row:
                db_ready = True
        
        if (not db_ready):
            self.add_user('superadmin', 'Admin321!', 'Firstname', 'Lastname', 'Superadmin')

        cur.close()
        con.close()

    def add_user(self, username, password, firstname, lastname, role):
        log.Logger().add_log(log.Event(f"New user created", username, f"{role} {username} was added to the database", "false"))
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()

        registration = int(datetime.datetime.timestamp(datetime.datetime.now()))
        
        cur.execute("INSERT INTO Users VALUES (?, ?, ?, ?, ?, ?)", [hasher.encrypt(username.lower()), hasher.get_hash(password), hasher.encrypt(firstname.lower()), hasher.encrypt(lastname.lower()), hasher.encrypt(role.lower()), registration])
        con.commit()
        cur.close()
        con.close()
        
    def add_member(self, firstname, lastname, street, housenr, zipcode, city, email, phone):
        log.Logger().add_log(log.Event(f"New member created", f"{firstname} {lastname}", f"A new member was added to the database", "false"))
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()

        registration = int(datetime.datetime.timestamp(datetime.datetime.now()))
        generated_id = id_generator.generate_id()
        while self.member_exists(generated_id):
            generated_id = id_generator.generate_id()
        # (Id INTEGER, Firstname TEXT, Lastname TEXT, Street TEXT, Housenumber INTEGER, Zipcode TEXT, City TEXT, Email TEXT, Phonenumber INTEGER, Registration INTEGER)
        cur.execute("INSERT INTO Members VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [generated_id, hasher.encrypt(firstname.lower()), hasher.encrypt(lastname.lower()), hasher.encrypt(street.lower()), hasher.encrypt(housenr.lower()), hasher.encrypt(zipcode.lower()), hasher.encrypt(city.lower()), hasher.encrypt(email.lower()), hasher.encrypt(phone), registration])
        con.commit()
        cur.close()
        con.close()

    def user_exists(self, username) -> bool:
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        
        cur.execute("SELECT 'Person' from Users where Username = ?", [hasher.encrypt(username.lower())])
        rows = cur.fetchall()
        con.commit()
        cur.close()
        con.close()
        return len(rows)
    
    def member_exists(self, Id) -> bool:
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        
        cur.execute("SELECT 'Person' from Members where Id = ?", [Id])
        rows = cur.fetchall()
        con.commit()
        cur.close()
        con.close()
        return len(rows)
    
    def update_user(self, username, new_username="", new_password="", new_firstname="", new_lastname="", new_role=""):
        log.Logger().add_log(log.Event(f"User was updated", f"{username}", f"The information of {username} was updated", "false"))
        new_info = [new_username, new_password, new_firstname, new_lastname, new_role, username]
        information = self.get_user(username)
        
        new_info = [new_info[i] if new_info[i] != "" else information[i] for i in range(len(new_info))]

        con = sqlite3.connect(self.db_name)
        cur = con.cursor()

        cur.execute("UPDATE Users SET Username=?, Password=?, Firstname=?, Lastname=?, Role=? WHERE Username=?", [hasher.encrypt(item.lower()) if i != 1 else item for i,item in enumerate(new_info)])
        con.commit()
        cur.close()
        con.close()
        
    def update_member(self,member_id, firstname="", lastname="", street="", housenumber="", zipcode="", city="", email="", phone=""):
        log.Logger().add_log(log.Event(f"Member was updated", f"{firstname} {lastname}", f"The information of {firstname} was updated", "false"))
        new_info = [firstname, lastname, street, housenumber, zipcode, city, email, phone, member_id]
        information = self.get_member(member_id)
        
        new_info = [new_info[i] if new_info[i] != "" else information[i] for i in range(len(new_info))]

        con = sqlite3.connect(self.db_name)
        cur = con.cursor()

        cur.execute("UPDATE Members SET Firstname=?, Lastname=?, Street=?, Housenumber=?, Zipcode=?, City=?, Email=?, Phonenumber=? WHERE Id=?", [hasher.encrypt(item.lower()) if not isinstance(item, int) else item for i,item in enumerate(new_info)])
        rows = cur.fetchall()
        con.commit()
        cur.close()
        con.close()
        
    def update_password(self, user, password):
        log.Logger().add_log(log.Event(f"Password was changed", f"{user}", f"The password of {user} was updated", "false"))
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()

        cur.execute("UPDATE Users SET Password=? WHERE Username=?", [hasher.get_hash(password), hasher.encrypt(user.lower())])
        rows = cur.fetchall()
        con.commit()
        cur.close()
        con.close()
    
    def get_user(self, username):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        
        cur.execute("SELECT Username, Password, Firstname, Lastname, Role from Users where Username = ?", [hasher.encrypt(username.lower())])
        rows = cur.fetchall()
        con.commit()
        cur.close()
        con.close()
        return [hasher.decrypt(item) if i != 1 else item for i,item in enumerate(rows[0])]
    
    def get_member(self, member_id):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        
        cur.execute("SELECT Firstname, Lastname, Street, Housenumber, Zipcode, City, Email, Phonenumber from Members where Id = ?", [member_id])
        rows = cur.fetchall()
        con.commit()
        cur.close()
        con.close()
        return [hasher.decrypt(item) for i,item in enumerate(rows[0])]
    
    def get_users(self):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        
        cur.execute("SELECT * from Users")
        rows = cur.fetchall()
        con.commit()
        cur.close()
        con.close()
        return [[hasher.decrypt(item) if i != 1 and type(item) != type(1) else item for i,item in enumerate(user)] for user in rows]
    
    def get_members(self):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        
        cur.execute("SELECT * from Members")
        rows = cur.fetchall()
        con.commit()
        cur.close()
        con.close()
        return [[hasher.decrypt(item) if type(item) != type(1) else item for i,item in enumerate(user)] for user in rows]
        
    def delete_user(self, username):
        log.Logger().add_log(log.Event(f"User was deleted", f"{username}", f"User {username} was deleted from the database", "false"))
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        
        cur.execute("DELETE from Users where Username = ?", [hasher.encrypt(username.lower())])
        con.commit()
        cur.close()
        con.close()
        
    def delete_member(self, Id):
        log.Logger().add_log(log.Event(f"Member was deleted", f"{Id}", f"Member with ID {Id} was deleted from the database", "false"))
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        
        cur.execute("DELETE from Members where Id = ?", [Id])
        con.commit()
        cur.close()
        con.close()
    

    def login(self, username, password) -> bool:
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        
        cur.execute("SELECT 'Person' from Users where Username = ? AND Password = ?", [hasher.encrypt(username.lower()), hasher.get_hash(password)])
        rows = cur.fetchall()
        con.commit()
        cur.close()
        con.close()
        if len(rows) == 1:
            log.Logger().add_log(log.Event(f"Login attempt successful", f"{username}", f"{username} logged into their account", "false"))
            return 1
        log.Logger().add_log(log.Event(f"Login attempt failed", f"{username}", f"Someone failed to login to {username}'s account with password {password}", "false"))
        return False

    def get_role(self, username) -> str:
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        
        if not self.user_exists(username):
            return "None"
        
        cur.execute("SELECT Role from Users where LOWER(Username) = LOWER(?)", [hasher.encrypt(username.lower())])
        rows = cur.fetchall()
        con.commit()
        cur.close()
        con.close()
        return hasher.decrypt(rows[0][0])


if __name__ == "__main__":
    db = Database()
    # db.add_user("username", "password", "firstname", "lastname", 'fake_role', 1337)
    print(db.login("username", "Password123!"))
    print(db.user_exists("UseRNaMe"))
    print(db.get_role("UseRNaMe"))
