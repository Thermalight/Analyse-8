import string
import re as regex

def merge(f_arr) -> bool:
    def try_all(x):
        for f in f_arr:
            if not f(x):
                return False
        return True
    
    return try_all

def validate_username(username) -> bool:
    for letter in username:
        if letter not in string.digits + string.ascii_letters + "_.'":
            return False
    
    has_valid_len = lambda username: len(username) >= 6 and len(username) <= 10
    starts_with_letter = lambda username: username[0] in string.ascii_letters
    
    return merge([has_valid_len, starts_with_letter])(username)

def validate_password(password) -> bool:
    has_valid_len = lambda password: len(password) >= 8 and len(password) <= 30
    has_digit = lambda password: len([i for i in password if i in string.digits]) > 0
    has_lower = lambda password: len([i for i in password if i in string.ascii_lowercase]) > 0
    has_upper = lambda password: len([i for i in password if i in string.ascii_uppercase]) > 0
    has_special = lambda password: len([i for i in password if i in string.punctuation]) > 0
    
    return merge([has_valid_len, has_digit, has_lower, has_upper, has_special])(password)
    

def sum_all_digits(ID) -> int:
    # strip checksum off the id
    clean_id = ID[0:-1]
    # sum all the numbers
    total = 0
    for char in clean_id:
        total += int(char)
    return total
    


def validate_id(ID) -> bool:
    valid_chars = "0123456789" 
    has_valid_len = lambda ID: len(ID) == 10
    has_valid_chars = lambda ID: False not in [char in valid_chars for char in ID]
    first_not_zero = lambda ID: ID[0] != "0"
    valid_checksum = lambda ID: sum_all_digits(ID) % 10 == int(ID[-1])
    
    return lambda ID: merge([has_valid_len, has_valid_chars, first_not_zero, valid_checksum])(ID)

def validate_phone(number) -> bool:
    for c in number:
        if c not in "0123456789":
            return False
    return len(number) == 8

def validate_zip(zipcode):
    if len(zipcode) != 6:
        return False
    return regex.search('[0-9]{4}[a-zA-Z]{2}', zipcode)

def validate_email(email: str) -> bool:
    return regex.search('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email)


if __name__ == "__main__":
    passwords = [
        "",
        "123456789",
        "over30                            ",
        "invalid_char: *",
        "Validpass1_",
    ]
    
    for password in passwords:
        print(f"{password}: {validate_password(password)}")