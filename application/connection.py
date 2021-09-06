import pymysql
from datetime import date

class Connection:

    # initialise the connection whenever created 
    def __init__(self, conn, request):
        self.conn = conn
        self.cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            self.connID = self.generateConnID()
            self.connAddress = request.form['inputConnAddress']
            self.connTaluka = request.form['inputConnTaluka']
            self.connDistrict = request.form['inputConnDistrict']
            self.connPin = request.form['inputConnPin']
            self.meterNo = request.form['inputMeterNo']
            self.conType = request.form['inputConnType']
            self.conNo = request.form['inputConNo']
            self.installationID = self.generateInstallID()
            self.installationDate = request.form['inputInstallationDate']
            self.connStatus = request.form['inputConnStatus']
            self.created = ""
            self.updated = ""
        except:
            print("Could not instantiate connection")

        


    def generateInstallID(self):
        try:
            self.cursor.execute('SELECT MAX(Installation_ID) as Installation_ID FROM connection')
            record = self.cursor.fetchone()
            if record:
                installID = record['Installation_ID'] + 1
                print(installID)
            else:
                # if the table is empty
                installID = 1000000001
        except Exception as e:
            print(e)
            print("Unable to generate InstallID")

        return installID
    
    # created using auto-increment (max of co_id + 1)
    def generateConnID(self):
        try:
            self.cursor.execute('SELECT MAX(Co_ID) as Co_ID FROM connection')
            record = self.cursor.fetchone()
            if record:
                connectID = record['Co_ID'] + 1
                print(connectID)
            else:
                # if the table is empty
                connectID = 100000000001
        except:
            print("Unable to generate connectID")

        return connectID
    

    # when provided with id initialize the variables
    def getConnection(self, connId):
        try:
            self.cursor.execute("SELECT * FROM connection WHERE Co_ID = %s",(connId))
            record = self.cursor.fetchone()
            self.connID = connId
            self.connAddress = record['Co_Address']
            self.connTaluka = record['Co_Taluka']
            self.connDistrict = record['Co_District']
            self.connPin = record['Co_Pin']
            self.meterNo = record['Meter_No']
            self.conType = record['Co_Type_ID']
            self.conNo = record['Con_ID']
            self.installationID = record['Installation_ID']
            self.installationDate = record['Installation_Date']
            self.connStatus = record['Co_Status']
            self.created = record['Created']
            self.updated = record['Updated']
            return True
        except:
            print("Unable to get connection")
            return False

    def insertConnection(self):
        today = str(date.today())
        self.created = today
        self.updated = today
        print(self.connID)
        print(self.connAddress)
        print(self.installationID)
        try:
            print("Executing Insert Query")
            self.cursor.execute("INSERT INTO connection VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.connID,self.connAddress,self.connTaluka,self.connDistrict, self.connPin, self.meterNo, self.conType, self.conNo, self.installationID, self.installationDate, self.connStatus, self.created, self.updated))
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            print("Unable to insert into connection")
            return False
    
    def deleteConnection(self, connId):
        try:
            print("Executing Delete Query")
            self.cursor.execute("DELETE FROM connection WHERE Co_ID = %s",(connId))
            record = self.cursor.fetchone()
            self.conn.commit()
            return True
        except:
            print("Unable to delete connection")
            return False

    