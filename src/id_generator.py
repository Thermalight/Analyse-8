import checksum
import random

class function_error(Exception):
    pass

def generate_id():
    random_num = random.randint(100000000,999999999)
    check = sum([int(i) for i in str(random_num)]) % 10
    ID = str(random_num) + str(check)


    if not checksum.check_id(ID):
        raise function_error("Invalid ID was generated")
    return ID



if __name__ == '__main__':
    # keep generating until an invalid ID is created
    count = 0
    while 1:
        generate_id()
        count += 1
        if count % 100000 == 0:
            print(count)