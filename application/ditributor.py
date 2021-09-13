from re import S
import pymysql 
from datetime import date

class Distributor:
    def __init__(self, conn, request):
        self.conn = conn
        self.cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            self.disId = ""
            self.disCompName = request.form['inputDistCompName']
            self.disAddress = request.form['inputDistAddress']
            self.disDistrict = request.form['inputDistDistrict']
            self.disPincode = request.form['inputDistPin']
            self.supplyPMonth = request.form['inputSupplyPMonth']
            self.supplyRate = request.form['inputSupplyRate']
            self.disContact = request.form['inputDistContact']
            self.created = str(date.today())
            self.updated = str(date.today())
        except Exception as e:
            print("Unable to initialize Distributor")
        

    def insertDistributor(self, conn):
        try:
            self.disId = self.generateDisID(conn)
            print("Executing Insert Query")
            self.cursor.execute("INSERT INTO distributor VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.disId,self.disCompName,self.disAddress,self.disDistrict,self.disPincode,self.supplyPMonth,self.disContact,self.supplyRate,self.created, self.updated))
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def deleteDistributor(self, disId):
        try:
            self.disId = disId
            print("deleting inside dis")
            self.cursor.execute('DELETE FROM distributor WHERE dis_id = %s', (self.disId))
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False 

    def updateDistributor(self, request, disId):
        try:
            self.disId = disId
            self.disCompName = request.form['inputDistCompName']
            self.disAddress = request.form['inputDistAddress']
            self.disDistrict = request.form['inputDistDistrict']
            self.disPincode = request.form['inputDistPin']
            self.supplyPMonth = request.form['inputSupplyPMonth']
            self.supplyRate = request.form['inputSupplyRate']
            self.disContact = request.form['inputDistContact']
            self.updated = str(date.today())
            self.cursor.execute("UPDATE distributor SET dis_compName = %s, dis_address = %s, dis_district = %s, dis_pincode = %s, supply_month = %s, dis_contact = %s, supply_rate = %s, updated  = %s WHERE dis_id = %s",(self.disCompName, self.disAddress, self.disDistrict, self.disPincode, self.supplyPMonth, self.supplyRate, self.disContact, self.updated, disId))
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            print("Unable to update Distributor")
            return False
    
    def getDistributor(self, disId):
        try:
            print("It is getting the dis")
            self.cursor.execute('SELECT * FROM distributor WHERE dis_id = %s', (disId))
            record = self.cursor.fetchone()
            self.disCompName = record['dis_compName']
            self.disAddress = record['dis_address']
            self.disDistrict = record['dis_district']
            self.disPincode = record['dis_pincode']
            self.supplyPMonth = record['supply_month']
            self.supplyRate = record['supply_rate']
            self.disContact = record['dis_contact']
            self.created = record['created']
            self.updated = record['updated']
            return True
        except Exception as e:
           print(e) 
           return False

    def generateDisID(self, conn):
        self.conn = conn
        self.cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            self.cursor.execute('SELECT MAX(dis_id) as dis_id FROM distributor')
            record = self.cursor.fetchone()
            if record:
                disId = record['dis_id'] + 1
                print(disId)
            else:
                # if the table is empty
                disId = 100000000001
        except:
            print("Unable to generate connectID")
        
        return disId
