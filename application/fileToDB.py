class MeterReading():

    attr = ["ReadID", "ConID", "ReadDate", "Reading"]
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
        # row['date'] = datetime.strptime(row['date'], '%m/%d/%Y').strftime('%Y-%m-%d')
                    date = datetime.strptime(row[2], '%m/%d/%Y').strftime('%Y-%m-%d')
                    cursor.execute("INSERT INTO cwmr_month VALUES(%s,%s,%s,%s)",(row[0],row[1],date,row[3]))
                except:
                    return False
        finally:
            self.conn.commit()
        return True