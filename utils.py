import random
import string
from hashlib import sha256

PASSWORD_LENGTH = 32

def random_printable(length):
    return ''.join(random.choice(string.printable) for _ in range(length))

def random_english_digits(length):
    return ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(length))

def do_sha256(text):
    return sha256(text.encode()).hexdigest()

def password_generator():
    passwords = [
        random_english_digits(PASSWORD_LENGTH),
        random_english_digits(4),
        random_english_digits(PASSWORD_LENGTH),
        random_english_digits(PASSWORD_LENGTH),
        random_english_digits(PASSWORD_LENGTH)
    ]

    print("{")
    for i, pwd in enumerate(passwords):
        print(f'    "level{i+2}": "{pwd}",')
    print("}")

def print_hashes(passwords):
    print("{")
    for level in passwords:
        print(f'    "{level}": "{do_sha256(passwords[level])}",')
    print("}")


# password_generator()

PASSWORDS = {
    "level2": "YiR6pcj2GTQKhZjsdITUaD9UD187UUnr",
    "level3": "yxAl",
    "level4": "5b2zOzIiNFeh2Cv5GKkxZggZO1EazxLz",
    "level5": "uX0ffyrHStMzUDkEoLu6PcfcDlZCAQc1",
    "level6": "aaa0djvGgwmdyDwM2YR432xEIJgvT61F",
}



def check_password(level, password):
    if level not in PASSWORDS:
        return False
    
    if type(password) != str:
        return False
    
    return PASSWORDS[level] == password