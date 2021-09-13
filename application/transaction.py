from random import randint
import pymysql 
from datetime import date

class Transaction():
    def __init__(self,conn,request = ""):

        self.conn = conn
        self.cursor = conn.cursor(pymysql.cursors.DictCursor)
        if request != "":
            self.trId = self.getTrId()
            self.bid = request.form['bid']
            self.date = str(date.today())
            self.status = "Success" if randint(1,10000) % 2 else "Failure"
            self.amount = request.form['amount']

    def insertTransaction(self):
        try:
            print("Executing Insert Query")
            today = str(date.today())
            self.cursor.execute("INSERT INTO transaction VALUES(%s,%s,%s,%s,%s,%s,%s)",(self.trId,self.bid,self.amount,self.status,self.date,today,today))
            return True
        except Exception as e:
            print(e)
            return False

    def getTransactionByBid(self,bid):
        try:
            self.cursor.execute('SELECT * FROM transactions WHERE BD_ID = %s', (bid))
            acc = self.cursor.fetchone()
            self.trId  = acc["Tr_ID"]
            self.bid = acc['BD_ID']
            self.date = acc['Tr_Date']
            self.status = acc['Tr_Status']
            self.amount = acc['Amount']
            return True
        except Exception as e:
            print(e)
            print("Unable to get transaction")
            return False


    def getTrId(self):
        try:
            self.cursor.execute('SELECT MAX(Tr_ID) as Tr_ID FROM transactions')
            record = self.cursor.fetchone()
            if record:
                TrId = record['Tr_ID'] + 1
                print(TrId)
            else:
                # if the table is empty
                TrId = 100000000001
            return (TrId)
        except Exception as e:
            print(e)
            print("Unable to generate InstallID")