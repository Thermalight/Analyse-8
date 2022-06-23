_valid_chars = "0123456789"

def merge(f_arr) -> bool:
    def try_all(x):
        for f in f_arr:
            if not f(x):
                return False
        return True
    
    return try_all

has_valid_len = lambda ID: len(ID) == 10
has_valid_chars = lambda ID: False not in [char in _valid_chars for char in ID]
first_not_zero = lambda ID: ID[0] != "0"

def sum_all_digits(ID) -> int:
    # strip checksum off the id
    clean_id = ID[0:-1]
    # sum all the numbers
    total = 0
    for char in clean_id:
        total += int(char)
    return total

valid_checksum = lambda ID: sum_all_digits(ID) % 10 == int(ID[-1])
check_id = merge([has_valid_len, has_valid_chars, first_not_zero, valid_checksum])


if __name__ == '__main__':
    ids = [
        "0123456789",
        "1123456789",
        "2123456789",
        "3123456789",
        "4123456789",
        "5123456789",
        "6123456789",
        "7123456789",
        "8123456789",
        "9123456789",
        "a123456789",
        "112345678",
        "",
        "#$%^&*#%$",
        "5223287425",

    ]

    for i in ids:
        print(f"{i} - {check_id(i)}")
