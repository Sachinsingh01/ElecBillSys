import pandas as pd
from datetime import datetime
from datetime import date
import pymysql
from pymysql.cursors import Cursor
from .Billing import Bill
from application import Billing

class MeterReading():
    columns = ['MeterReadingId', 'MeterNo', 'Fname', 'Lname','Address','Taluka','District','Pin', 'Contact', 'prev_date', 'prev_reading', 'Meter_Reading', 'Read_Date']
    #update the lis
    Talukas = {"PO":"Ponda", "TI":"Tiswadi"}
    def __init__(self, conn, id):
        # self.filename = 
        self.path = "C:\\Users\\adamle\\Documents\\ElecBillSys\\application\\static\\file"
        #take filename from {decide later}
        self.id = id
        self.fileName = f'{self.id[:2]}-{date.today()}.csv'
        self.conn = conn
        self.cursor = conn.cursor(pymysql.cursors.DictCursor)

    def readFile(self):
        # filename = f"C:\\Users\\adamle\\Documents\\ElecBillSys\\application\\static\\file\\{self.filename}"
        df = pd.read_csv(f'{self.path}\\{self.fileName}')
        print(df.columns == MeterReading.columns)
        cursor = self.conn.cursor()
        # try:
        #     for _, row in df.iterrows():
        #         try:
        #             print(f'row: {_}')
        #             print(row["MeterNo"],row["prev_date"],row["prev_reading"],row["Read_Date"],row["Meter_Reading"])
        #             bill = Bill(self.conn,row["MeterNo"],row["prev_date"],row["prev_reading"],row["Read_Date"],row["Meter_Reading"])
        #             bill.jadoo()
        #             # s = f"inserting row: {_}"
        #             # print(s)
        #             #check if row[2] contains date else change it
        #             # date = datetime.strptime(row[], '%m/%d/%Y').strftime('%Y-%m-%d')
        #             #change the query according to table and staging table? how to use
        #             # cursor.execute("INSERT INTO cwmr_month VALUES(%s,%s,%s,%s)",(row[0],row[1],date,row[3]))
        #         except:

        #             return False
        # finally:
        #     self.conn.commit()
        for _, row in df.iterrows():
            print(f'row: {_}')
            print(row["MeterNo"],row["prev_date"],row["prev_reading"],row["Read_Date"],row["Meter_Reading"])
            bill = Bill(self.conn,row["MeterNo"],row["prev_date"],row["prev_reading"],row["Read_Date"],row["Meter_Reading"])
            bill.getAmount()
        return True

    def createMeterReadingFile(self): 
        #get meter guy login id
        taluka = self.Talukas[self.id[:2]]
        self.cursor.execute("SELECT * FROM connection where Co_Taluka = %s ",(taluka))
        connections = self.cursor.fetchall()
        ls = []
        self.cursor.execute('SELECT MAX(Meter_reading_id) as md FROM meter_reading')
        record = self.cursor.fetchone()
        id = int(record['md'])
        print(id)
        for row in connections:
            print(row)
            #generate a meter reading ID
            id = id + 1
            # ['MeterReadingId', 'MeterNo', 'Fname', 'Lname','Address','Taluka','District','Pin', 'Contact', 'prev_date', 'prev_reading', 'Meter_Reading', 'Read_Date']
             #create database connection with pymysql dictionary
            self.cursor.execute("select Meter_Reading,Read_Date,Meter_Status from meter_reading where Co_ID = %s and Read_Date = (SELECT max(Read_Date) from Meter_Reading WHERE Co_ID = %s);",(row['Co_ID'],row['Co_ID']))
            reading = self.cursor.fetchone()
            print(f'Reading: {reading["Meter_Reading"]}')

            self.cursor.execute("SELECT Con_First_Name,Con_Last_Name,Con_Contact FROM consumer where Con_ID = %s ",(row['Con_ID']))
            consumer = self.cursor.fetchone()
            temp = [id,row['Meter_No'], consumer['Con_First_Name'],consumer['Con_Last_Name'],row['Co_Address'],row['Co_Taluka'],row['Co_District'],row['Co_Pin'],consumer['Con_Contact'],str(reading['Read_Date']),reading['Meter_Reading'],"",""]
            print(temp)
            ls.append(temp)
        df = pd.DataFrame(data=ls,columns=self.columns)
        path_file = f'{self.path}\\{self.fileName}'
        df.to_csv(path_file,index=False)
       
        
        #create the file name according to month and region
        #get the connection ID, meter number address, connection type, ... 
        #just leave the "Meter_Reading", "Read_Date", "Meter_Status" empty for the guy to fill in