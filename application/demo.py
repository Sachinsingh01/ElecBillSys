import werkzeug
import string
import hashlib
import os
import random
from werkzeug.security import generate_password_hash, check_password_hash

def generatePassword():

        DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']  
        LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q','r', 's', 't', 'u', 'v', 'w', 'x', 'y','z']
        
        UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'M', 'N', 'O', 'p', 'Q','R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y','Z']
        
        SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>', '*', '(', ')', '<']
        
        COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + LOCASE_CHARACTERS + SYMBOLS

        length = 8
        r_str = ''.join(random.choice(COMBINED_LIST) for i in range(length))
        print(r_str)
        # h_password is the hashed value
        # h_password = hashlib.pbkdf2_hmac('sha256',r_str.encode('utf-8'), salt, 100000, dklen=32)
        #h_password = bcrypt.hashpw(r_str, salt)

        h_password = generate_password_hash(r_str)
        return h_password 

print(generatePassword())
