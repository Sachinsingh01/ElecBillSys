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
        slabs = [100,200,300,400] # db 
        #define this functions
        prevReading = self.meterReading.getPreviousReading()
        currentReading = self.meterReading.getCurrentReading()
        consumption = currentReading - prevReading
        for slab in slabs:
            pass
