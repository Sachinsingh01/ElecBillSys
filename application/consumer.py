
import pymysql 


class Consumer():
    # Dictionary of Talukas and Districts in Goa
    talukas = ["PONDA", "TISWADI", "BARDEZ", "BICHOLIM", "CANACONA", "SATTARI", "MORMUGAO", "PERNEM", "QUEPEM", "SALCETTE", "SANGUEM", "DHARBANDORA"]
    cidTalukas = ["PON", "TIS", "BAR", "BIC", "CAN", "SAT", "MOR", "PER", "QUE", "SAL", "SAN", "DHA"]
    districts = ["SOUTH GOA","NORTH GOA"]


    def __init__(self,conn,request):
        try:
            self.cid = request.form['inputConID']
            self.fname = request.form['inputConFName']
            self.lname = request.form['inputConLName']
            self.address = request.form['inputConAddress']
            self.taluka = request.form['inputConTaluka']
            self.district = request.form['inputConDistrict']
            self.pinCode = request.form['inputConPin']
            self.meterId = request.form['inputMeterId']
            self.conType = request.form['inputConType']
            self.sanctionedLoad = request.form['inputSancLoad']
            self.contact = request.form['inputConContact']
        except:
            print("Unable to initialize consumer")

        self.conn = conn
        self.cursor = conn.cursor(pymysql.cursors.DictCursor)


    def validateCId(self):
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
            return False

            
    def insertConsumer(self):
        try:
            self.cursor.execute("INSERT INTO Consumer VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.cid,self.fname,self.lname,self.address,self.taluka,self.district,self.pinCode,self.meterId,self.conType,int(self.sanctionedLoad),self.contact))
            return True
        except:
            print("Exception")
            return False
    

    def deleteConsumer(self, cid):
        try:
            print("deleting inside cons")
            self.cursor.execute('DELETE FROM consumer WHERE ConID = %s', (cid))
            self.conn.commit()
            return True
        except:
            print("Exception")
            return False 


    def getConsumer(self, cid):
        try:
            self.cursor.execute('SELECT * FROM consumer WHERE ConID = %s', (cid))
            acc = self.cursor.fetchone()
            self.cid = cid
            self.fname = acc['ConFirstName']
            self.lname = acc['ConLastName']
            self.address = acc['ConAddress']
            self.taluka = acc['ConTaluka']
            self.district = acc['ConDistrict']
            self.pinCode = acc['ConPinCode']
            self.meterId = acc['MeterID']
            self.conType = acc['ConType']
            self.sanctionedLoad = acc['ConSanctionedLoad']
            self.contact = acc['ConContact'] 
            return True
        except:
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
            self.meterId = request.form['inputMeterId']
            self.conType = request.form['inputConType']
            self.sanctionedLoad = request.form['inputSancLoad']
            self.contact = request.form['inputConContact']
            print(cid)
            print("Done")
            self.cursor.execute("UPDATE consumer SET ConFirstName = %s, ConLastName = %s, ConAddress = %s, ConTaluka = %s, ConDistrict = %s, ConPinCode = %s,MeterID = %s,ConType = %s,ConSanctionedLoad = %s,ConContact = %s WHERE ConID = %s",(self.fname,self.lname,self.address,self.taluka,self.district,self.pinCode,self.meterId,self.conType,int(self.sanctionedLoad),self.contact,cid))
            self.conn.commit()
            return True
        except:
            print("Exception")
            return False
