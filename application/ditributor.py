from re import S
import pymysql 
from datetime import date

class Distributor:
    def __init__(self, conn, request):
        self.conn = conn
        self.cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            self.disId = request.form['inputDistID']
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
        

    def insertDistributor(self):
        try:
            print("Executing Insert Query")
            self.cursor.execute("INSERT INTO distributor VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.disId,self.disCompName,self.disAddress,self.disDistrict,self.disPincode,self.supplyPMonth,self.supplyRate,self.disContact,self.created, self.updated))
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def deleteDistributor(self, disId):
        try:
            print("deleting inside dis")
            self.cursor.execute('DELETE FROM distributor WHERE dis_id = %s', (disId))
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
            self.supplyRate = record['dis_contact']
            self.disContact = record['supply_rate']
            self.created = record['created']
            self.updated = record['updated']
            return True
        except Exception as e:
           print(e) 
           return False
