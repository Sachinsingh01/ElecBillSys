from os import pardir
from numpy.lib.function_base import select
from pymysql import cursors
from pymysql.cursors import Cursor
from .consumer import Consumer
from .connection import Connection
from datetime import timedelta
from datetime import date
from datetime import datetime
import pymysql
import numpy as np
# from .fileToDB import MeterReading
class Bill():

    def __init__(self,conn,meterNo,prevDate,prevReading,readDate,reading):

        self.conn = conn
        self.cursor = conn.cursor(pymysql.cursors.DictCursor)
        self.meterNo = meterNo
        self.cursor.execute("SELECT Co_Type_ID from connection where Meter_No = %s",(self.meterNo))
        self.connType = self.cursor.fetchone()['Co_Type_ID']
        self.prevDate = self.getDate(prevDate)
        self.currDate = self.getDate(readDate)
        self.prevReading = prevReading
        self.currReading = reading
        self.dueDate = self.generateDueDate() #due date can be generated using todays date
        print(f"prev: {self.prevDate}, curr:{self.currDate},due:{self.dueDate}")
        # self.amount = self.getAmount()

    
    def getAmount(self):
        self.consumption = self.currReading - self.prevReading
        print(f"self.consumption: {self.consumption}")
        self.cursor.execute("SELECT Units_To from slab_charges WHERE From_Date = (SELECT MAX(From_Date) from slab_charges) and S_Charge_Type = %s and Con_Type_ID = %s",("EC",self.connType)) 
        temp = self.cursor.fetchall()
        slabs=[]
        for t in temp:
            slabs.append(t['Units_To'])
        print(slabs)
        slabs = np.array(slabs)
        #find the days passed between prev and current date
        billingPeriod = int((self.currDate - self.prevDate).days)
        print(billingPeriod)
        print(str(self.prevDate))
        self.cursor.execute("SELECT DISTINCT From_Date FROM slab_charges WHERE (From_Date >%s and From_Date <%s) or From_Date =(SELECT MAX(From_Date) from slab_charges where From_Date <=%s) ORDER BY From_Date Desc ",(str(self.prevDate),str(self.currDate),str(self.prevDate)))
        Temp = self.cursor.fetchall()
        dates = []
        for t in Temp:
            print(t)
            dates.append(t['From_Date'])

        i = len(dates) - 2
        frm = self.prevDate
        to = self.currDate
        days = []
        sum = 0
        while(i>=0):
            to = dates[i]
            d = (to - frm).days
            sum += int(d)
            frm = dates[i]
            days.append(d)
            i -=1
        days.append(billingPeriod-sum)
        print(days)

        dates.reverse()
        print(f"Reversed dates = {dates}")

        #calculate fixed charge
        #calculate Subsidy charge
        fixedCharges = []
        subsidy = []
        for d in dates:
            self.cursor.execute("SELECT NS_Charges from no_slab_charges WHERE From_Date= %s and NS_Charge_Type = %s and Con_Type_ID = %s ",(str(d),"Fixed",self.connType))
            fixedCharges.append(self.cursor.fetchone()['NS_Charges'])
            self.cursor.execute("SELECT NS_Charges from no_slab_charges WHERE From_Date= %s and NS_Charge_Type = %s and Con_Type_ID = %s ",(str(d),"Subsidy",self.connType))
            subsidy.append(self.cursor.fetchone()['NS_Charges'])
        
        print(f"fixedCharges = {fixedCharges}")
        print(f"subsidy = {subsidy}")

        #calculate EC values
        ECs = []
        for d in dates:
            self.cursor.execute("SELECT S_Charges, Units_To from slab_charges WHERE From_Date= %s and S_Charge_Type = %s and Con_Type_ID = %s ORDER BY Units_To",(str(d),"EC",self.connType))
            records = self.cursor.fetchall()
            ls = []
            for record in records:
                ls.append(float(record['S_Charges']))
            ECs.append(ls)
        print(f"ECs: {ECs}")

        #calculate FPPCA values
        FPPCAs = []
        for d in dates:
            self.cursor.execute("SELECT S_Charges, Units_To from slab_charges WHERE From_Date= %s and S_Charge_Type = %s and Con_Type_ID = %s ORDER BY Units_To",(str(d),"FPPCA",self.connType))
            records = self.cursor.fetchall()
            ls = []
            for record in records:
                ls.append(float(record['S_Charges']))
            FPPCAs.append(ls)
        print(f"FPPCAs: {FPPCAs}")
        #weighted fixedCharge and Subsidy
        t1 = 0
        t2 = 0
        for d,f,s in zip(days,fixedCharges,subsidy):
            t1 += int(d)*int(f)
            t2 += int(d)*int(s)
    
        fixChargeRate = t1/billingPeriod
        subsidyRate = t2/billingPeriod
        print(f"fcr:{fixChargeRate}, sr:{subsidyRate}")


        #weighted EC and FPPCA
        tt1 = [0,0,0,0,0]
        tt2 = [0,0,0,0,0]
        ECs = np.array(ECs)
        FPPCAs = np.array(FPPCAs)
        for d,ec,fppca in zip(days,ECs,FPPCAs):
            tt1 += ec*d
            tt2 += fppca*d
        
        ECRates = tt1/billingPeriod
        FPPCARates = tt2/billingPeriod

        print(f"ECs: {ECRates}")
        print(f"FPPCAs: {FPPCARates}")

        #calculating new slabs
        c = billingPeriod /30.0
        newSlabs = slabs * c
        print(f"New Slabs: {newSlabs}")

        #calculate the slabs used by connection
        i = 0
        c = self.consumption
        for slab in newSlabs:
            if slab > c:
                index = i
                break
            i += 1
        newSlabs[i] = self.consumption
        prev = 0
        j = 0
        while(j<5):
            newSlabs[j] -= prev
            prev += newSlabs[j]
            j +=1

        i += 1
        while(i<5):
            newSlabs[i] = 0
            i += 1
        print("newSlabs")
        print(f"{newSlabs} * {ECRates} = {np.sum(newSlabs * ECRates)}")
        self.amount = fixChargeRate + subsidyRate + np.sum(newSlabs * ECRates) + np.sum(newSlabs * FPPCARates)
        print(f"amount = {fixChargeRate} + {subsidyRate} + {np.sum(newSlabs * ECRates)} + {np.sum(newSlabs * FPPCARates)}")
        print(self.amount)
    
        #fill the required tables  or return amount 
        self.BDID = self.generateBDID()
        print(self.BDID)
        self.cursor.execute("INSERT INTO bill_master VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.BDID,self.meterNo,self.currDate,self.currReading,self.prevDate,self.prevReading,self.consumption,"OK",str(date.today()),str(date.today()),self.amount))
        # insert fixedCharge and subsidy 
        temp = self.generateBDDID()
        print(temp)
        self.cursor.execute("INSERT INTO bill_detail VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",(temp,self.BDID,"Fixed",1,(fixChargeRate*30)/billingPeriod,0,str(date.today()),str(date.today()),fixChargeRate))
        temp = self.generateBDDID()
        print(temp)
        self.cursor.execute("INSERT INTO bill_detail VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",(temp,self.BDID,"Subsidy",1,(subsidyRate*30)/billingPeriod,0,str(date.today()),str(date.today()),subsidyRate))
        
        #insert EC
        #insert FPPCA
        i=0
        while(i <= index):
            temp = self.generateBDDID()
            print(temp)
            self.cursor.execute("INSERT INTO bill_detail VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",(temp,self.BDID,"EC",newSlabs[i],ECRates[i],slabs[i],str(date.today()),str(date.today()),newSlabs[i] * ECRates[i]))
            temp = self.generateBDDID()
            print(temp)
            self.cursor.execute("INSERT INTO bill_detail VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",(temp,self.BDID,"FPPCA",newSlabs[i],FPPCARates[i],slabs[i],str(date.today()),str(date.today()),newSlabs[i] * FPPCARates[i]))
            i += 1
        
        self.conn.commit()
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
        return self.currDate + timedelta(days = 15)

    
    def generateBDID(self):
        self.cursor.execute("SELECT max(BD_ID) as BD_ID from bill_master")
        record = self.cursor.fetchone()
        print(record)
        if record["BD_ID"] == None:
            return 60000000000001
        else:
            return int(record['BD_ID']) + 1
    
    def generateBDDID(self):
        self.cursor.execute("SELECT max(BDD_ID) as BDD_ID from bill_detail")
        record = self.cursor.fetchone()
        if record['BDD_ID'] == None:
            return 4000000000000001
        else:
            return int(record['BDD_ID']) + 1

    def getDate(self,date):
        temp = date.split("/")
        dat = f"{temp[2]}-{temp[0]}-{temp[1]}"
        return datetime.strptime(dat,'%Y-%m-%d').date()

    def getBill(self,bid):
        pass
    
    """ i =0
        c = self.consumption
        prev = 0
        while (c > 0):
            c = c - (newSlabs[i] - prev)
            prev = newSlabs[i]
            i += 1
        i -= 1
        newSlabs[i] += c - newSlabs[i-1] if i > 0 else prev
        i +=1
        while(i<5):
            newSlabs[i] = 0
            i += 1
        print(newSlabs) """
