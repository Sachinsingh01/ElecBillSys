from .consumer import Consumer
from .connection import Connection
from datetime import timedelta
from datetime import date
from datetime import datetime
# from .fileToDB import MeterReading
class Bill():

    def __init__(self,conn,meterNo,prevDate,prevReading,readDate,reading):
        # self.connection = Connection(conn,request)
        # self.connection.getConnection(connId)


        # self.consumer = Consumer(conn,request)
        # self.consumer.getConsumer(cid)


        # self.billId = self.generateID()
        self.prevDate = prevDate
        self.currDate = readDate
        self.prevReading = prevReading
        self.currReading = reading
        self.dueDate = self.generateDueDate()
        # self.amount = self.getAmount()

    
    def getAmount(self):
        slabs = [100,200,300,400] #get from the dataBase  
        #define this functions
        prevReading = self.meterReading.getPreviousReading()
        currentReading = self.meterReading.getCurrentReading()
        consumption = currentReading - prevReading
        prevDate = self.meterReading.getPrevDate()
        currDate = self.meterReading.getCurrDate()
        d1 = datetime.strftime(prevDate, '%Y-%m-%d')
        d2 = datetime.strftime(currDate, '%Y-%m-%d')
        #find the days passed between prev and current date
        delta = int((d2-d1).days)
        print(f"d1 = {d1} d2= {d2} delta = {delta}")
        #if prev reading date >= last change of slabs 
            #simple calculations 
        #else 
            #go uptill prev date >= last change and calculate for every change
        #fill the required tables  or return amount 
        #do not forget to update the billing calender

    def getCurrDate(self):
        try:
            print("Trying to Get Current Reading date")
            self.cursor.execute('SELECT Max(Read_Date) as currDate, Meter_Reading FROM Meter_Reading where Co_ID = %s',(self.connection.connID))
            acc = self.cursor.fetchone()
            currDate = acc['currDate']
            currReading = acc['Meter_Reading']
            return currDate
        except:
            print("unable to create cno")
            return 0

    def getPrevDate(self):
        #check for prev data in billing table
        #if no data then get the installation date asa prev date and make prev reading 0
        try:
            print("Trying to Get prev Reading date")
            self.cursor.execute('SELECT Installation_ID as prevDate FROM Connection where Co_ID = %s',(self.connection.connID))
            acc = self.cursor.fetchone()
            prevDate = acc['prevDate']
            return prevDate, 0
        except:
            print("unable to create cno")
            return 0

    def generateDueDate(self):
        return date.strftime(self.currDate,'%Y-%m-%d' + timedelta(days = 15))
    
    def jadoo(self):
        pass