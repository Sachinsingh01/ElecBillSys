from datetime import date
import pymysql
import random
import string
import hashlib
import os

class User:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor(pymysql.cursors.DictCursor)
        self.cursor.execute("SELECT * FROM consumer WHERE Con_ID = %s",(cid))
        record = self.cursor.fetchone()
        self.userId = self.generateUserId()
        self.userType = "Consumer"
        self.userName = record['Con_No']
        self.password = self.generatePassword()
        self.created =  str(date.today())
        self.updated = str(date.today())

    def generatePassword():
        characters = string.printable
        # 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'()*+, -./:;<=>?@[\]^_`{|}~ 

        length = 10
        r_str = ''.join(random.choice(characters) for i in range(length))
        salt = os.urandom(32)

        # h_password is the hashed value
        h_password = hashlib.pbkdf2_hmac('sha256',r_str.encode('utf-8'), salt, 100000, dklen=128)
        return h_password
    

    def insertUser(self):
        try:
            self.cursor.execute("INSERT INTO User_Info VALUES(%s,%s,%s,%s,%s,%s)",(self.userId, self.userType, self.userName, self.password, self.created, self.updated))
        except Exception as e:
            print(e)

    def generateUserId(self):
        try:
            self.cursor.execute('SELECT MAX(user_id) as user_id FROM connection')
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
