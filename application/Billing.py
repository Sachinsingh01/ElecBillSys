from .consumer import Consumer
import datetime
from .fileToDB import MeterReading
class Bill():

    def __init__(self,conn,request):
        self.consumer = Consumer(conn,request)
        self.meterReading = MeterReading(conn)
        cid = request.form['inputConFilID']
        self.consumer.getConsumer(cid)
        self.BillID = self.generateID()
        self.StartDate = self.getStartDate()
        self.EndDate = self.getEndDate()
        self.DueDate = self.generateDueDate()
        self.Amount = self.getAmount()
    
    def getAmount(self):

        from datetime import datetime
        slabs = [100,200,300,400] #get from the data base  
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
        #if prev reading date >= last change of slabs 
            #simple calculations 
        #else 
            #go uptill prev date >= last change and calculate for every change
        for slab in slabs:
            pass

        #fill the required tables  or return amount 
        #do not forget to update the billing calender

