class MeterReading():

    attr = ["Meter_Reading_id", "Meter_No", "Co_ID", "Meter_Reading", "Read_Date", "Meter_Status"]
    def __init__(self, conn):
        self.filename = "readings.csv"
        self.conn = conn

    def readFile(self):
        import pandas as pd
        from datetime import datetime
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

    def createMeterReadingFile(self, meterGuyID): #get meter guy login id
        
        #create database connection with pymysql dictionary
        #generate a meter reading ID
        #create the file name according to month and region
        #get the connection ID, meter number address, connection type, ... 
        #just leave the "Meter_Reading", "Read_Date", "Meter_Status" empty for the guy to fill in
        pass