import pandas as pd
from datetime import datetime
from datetime import date
import pymysql
from pymysql.cursors import Cursor


class MeterReading():
    column = ['MeterReadingId', 'MeterNo', 'Co_ID', 'Meter_Reading', 'Read_Date', 'Meter_Status', 'prev_date', 'prev_reading']
    #update the list
    Talukas = {"PO":"Ponda", "TI":"Tiswadi"}
    def __init__(self, conn, id):
        # self.filename = 
        self.path = "C:\\Users\\adamle\\Documents\\ElecBillSys\\application\\static\\file"
        self.id = id
        self.conn = conn
        self.cursor = conn.cursor(pymysql.cursors.DictCursor)

    def readFile(self):
        filename = f"C:\\Users\\adamle\\Documents\\ElecBillSys\\application\\static\\file\\{self.filename}"
        df = pd.read_csv(filename)
        print(df.columns == MeterReading.attr)
        cursor = self.conn.cursor()
        try:
            for _, row in df.iterrows():
                try:
                    print(row[0],row[1],row[2],row[3])
                    s = f"inserting row: {_}"
                    print(s)
                    #check if row[2] contains date else change it
                    date = datetime.strptime(row[2], '%m/%d/%Y').strftime('%Y-%m-%d')
                    #change the query according to table and staging table? how to use
                    cursor.execute("INSERT INTO cwmr_month VALUES(%s,%s,%s,%s)",(row[0],row[1],date,row[3]))
                except:
                    return False
        finally:
            self.conn.commit()
        return True

    def createMeterReadingFile(self): 
        #get meter guy login id
        self.fileName = f'{self.id[:2]}-{date.today()}.csv'
        taluka = self.Talukas[self.id[:2]]
        self.cursor.execute("SELECT * FROM connection where Co_Taluka = %s ",(taluka))
        rows = self.cursor.fetchall()
        ls = []
        self.cursor.execute('SELECT MAX(Meter_reading_id) as md FROM meter_reading')
        record = self.cursor.fetchone()
        id = int(record['md'])
        print(id)
        for row in rows:
            id = id + 1
            temp = []
            print(f"{id},{row}")
        #create database connection with pymysql dictionary
        #generate a meter reading ID
        #create the file name according to month and region
        #get the connection ID, meter number address, connection type, ... 
        #just leave the "Meter_Reading", "Read_Date", "Meter_Status" empty for the guy to fill in