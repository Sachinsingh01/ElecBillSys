from datetime import date
import pymysql
import random
import string
import hashlib
import os
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, conn, cid):
        self.conn = conn
        self.cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            self.cursor.execute("SELECT * FROM consumer WHERE Con_ID = %s",(cid))
            record = self.cursor.fetchone()
        except Exception as e:
            print(e)
            print("Unable to fetch record ")
        self.userId = self.generateUserId()
        self.userType = 2
        self.userName = record['Con_No']
        self.password = self.generatePassword()
        self.created =  str(date.today())
        self.updated = str(date.today())

    def generatePassword(self):

        DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']  
        LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q','r', 's', 't', 'u', 'v', 'w', 'x', 'y','z']
        
        UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'M', 'N', 'O', 'p', 'Q','R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y','Z']
        
        SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>', '*', '(', ')', '<']
        
        COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + LOCASE_CHARACTERS + SYMBOLS

        length = 8
        r_str = ''.join(random.choice(COMBINED_LIST) for i in range(length))

        # h_password is the hashed value
        # h_password = hashlib.pbkdf2_hmac('sha256',r_str.encode('utf-8'), salt, 100000, dklen=32)
        #h_password = bcrypt.hashpw(r_str, salt)

        h_password = generate_password_hash(r_str)
        return h_password    
    

    def insertUser(self):
        try:
            self.cursor.execute("INSERT INTO login_info VALUES(%s,%s,%s,%s,%s,%s)",(self.userId, self.userType, self.userName, self.password, self.created, self.updated))
        except Exception as e:
            print(e)
            print("Unable to insert user")

    def generateUserId(self):
        try:
            self.cursor.execute('SELECT MAX(user_id) as user_id FROM login_info')
            record = self.cursor.fetchone()
            if record:
                user_id = record['user_id'] + 1
                print(user_id)
            else:
                # if the table is empty
                user_id = 1000000001
        except Exception as e:
            print(e)
            print("Unable to generate user_id")
