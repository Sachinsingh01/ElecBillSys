
from re import S
import pymysql 
from datetime import date

class Consumer():
    # Dictionary of Talukas and Districts in Goa
    talukas = ["PONDA", "TISWADI", "BARDEZ", "BICHOLIM", "CANACONA", "SATTARI", "MORMUGAO", "PERNEM", "QUEPEM", "SALCETTE", "SANGUEM", "DHARBANDORA"]
    cidTalukas = ["PON", "TIS", "BAR", "BIC", "CAN", "SAT", "MOR", "PER", "QUE", "SAL", "SAN", "DHA"]
    districts = ["SOUTH GOA","NORTH GOA"]


    def __init__(self,conn,request):
        try:
            self.fname = request.form['inputConFName']
            self.lname = request.form['inputConLName']
            self.address = request.form['inputConAddress']
            print(request.form['inputConAddress'])
            print(self.address)
            self.taluka = request.form['inputConTaluka']
            self.district = request.form['inputConDistrict']
            self.pinCode = request.form['inputConPin']
            self.contact = request.form['inputConContact']
            self.email = request.form['inputConEmail']
            
        except:
            print("Unable to initialize consumer")
        self.conn = conn
        self.cursor = conn.cursor(pymysql.cursors.DictCursor)
        self.cno = self.createConsumerNo()

            
    def insertConsumer(self):
        today = str(date.today())
        print(today)
        print(self.cno)
        print(self.contact)
        cid = int(self.cno[3:])
        print(cid)
        # INSERT INTO consumer(Con_No,Con_First_Name,Con_Last_Name,Con_Address,Con_Taluka,Con_District,Con_Pin_Code,Con_Contact,Created,Updated) VALUES("PO1000000001","Sachin","Tendulkar", "HS NO 10 TOP COLA", "PONDA", "SOUTH GOA", "403401", "9876543210", "2021-09-05", "2021-09-05")
        try:
            print("Executing Insert Query")
            self.cursor.execute("INSERT INTO consumer(Con_No,Con_First_Name,Con_Last_Name,Con_Address,Con_Taluka,Con_District,Con_Pin_Code,Con_Contact,Created,Updated,Con_Email) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.cno,self.fname,self.lname,self.address,self.taluka,self.district,self.pinCode,self.contact,today,today,self.email))
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
    

    def deleteConsumer(self, cid):
        try:
            print("deleting inside cons")
            self.cursor.execute('DELETE FROM consumer WHERE Con_No = %s', (cid))
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False 


    def getConsumer(self, cid):
        try:
            #check is consumer number or consumer ID is to be used
            self.cursor.execute('SELECT * FROM consumer WHERE Con_No = %s', (cid))
            acc = self.cursor.fetchone()
            self.cid = cid
            self.fname = acc['Con_First_Name']
            self.lname = acc['Con_Last_Name']
            self.address = acc['Con_Address']
            print(acc['Con_Address'])
            self.taluka = acc['Con_Taluka']
            self.district = acc['Con_District']
            self.pinCode = acc['Con_Pin_Code']
            self.contact = acc['Con_Contact'] 
            self.email = acc["Con_Email"]
            return True
        except Exception as e:
            print(e)
            print("Unable to get consumer")
            return False

    def updateConsumer(self, cid, request):
        try:
            print("in consumer update")
            print(request.form['inputConPin'])
            self.fname = request.form['inputConFName']
            self.lname = request.form['inputConLName']
            self.address = request.form['inputConAddress']
            self.taluka = request.form['inputConTaluka']
            self.district = request.form['inputConDistrict']
            self.pinCode = request.form['inputConPin']
            self.contact = request.form['inputConContact']
            self.email = request.form['inputConEmail']
            today = str(date.today())
            print(cid)
            print("Done")
            self.cursor.execute("UPDATE consumer SET Con_First_Name = %s, Con_Last_Name = %s, Con_Address = %s, Con_Taluka = %s, Con_District = %s, Con_Pin_Code = %s,Con_Contact = %s, Con_Email= %s, Updated = %s WHERE Con_No = %s",(self.fname,self.lname,self.address,self.taluka,self.district,self.pinCode,self.contact,self.email,today,cid))
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            print("Exception")
            return False
    
    #create a consumer No for consumer 
    def createConsumerNo(self):
        try:
            print("Trying to Get ID")
            self.cursor.execute('SELECT * from consumer ORDER BY Con_ID DESC')
            acc = self.cursor.fetchone()
            print(acc)
            id = acc['Con_ID']
            cno = f'{self.taluka[:2].upper()}{id+1}'
            print(cno)
            return cno
        except:
            print("unable to create cno")
            return 0
    #create a password using provided calculations
    def createDefaultPassword(self):
        pass

    #take the created consumerID and password and store the hash of password in Login Table
    def insertLoginCredentials(self):
        pass
    
    '''def validateCId(self):
        self.cursor.execute('SELECT * FROM consumer WHERE ConID = %s', (self.cid))
        acc = self.cursor.fetchone()
        # print(acc)
        if len(self.cid) == 11 and self.cid[:3].upper() in self.cidTalukas and acc == None:
            return True
        else:
            return False


    def validateTaluka(self):
        if self.taluka.upper() in self.talukas:
            return True
        else:
            return False


    def validateDistrict(self):
        if self.district.upper() in self.districts:
            return True 
        else:
            return False


    def validateMeterID(self):
        self.cursor.execute('SELECT * FROM consumer WHERE MeterID = %s', (self.meterId))
        acc = self.cursor.fetchone()
        if len(self.meterId) == 14 and self.meterId[0].isdigit() and self.meterId[0] != '0' and self.meterId[1:4].upper() in self.cidTalukas and acc == None:
            return True
        else:
            return False


    def validateContact(self):
        if len(self.contact) == 10 and self.contact.isdigit():
            return True
        else:
            return False'''