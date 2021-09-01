class Consumer():
    def __init__(self,cursor,cid="PON12345678",fname="",lname="",address="",taluka="",district="",pinCode="",meterId="",conType="",sanctionedLoad=10,contact=""):
        self.cid = cid
        self.fname = fname
        self.lname = lname
        self.address = address
        self.taluka = taluka
        self.district = district
        self.pinCode = pinCode
        self.meterId = meterId
        self.conType = conType
        self.sanctionedLoad = sanctionedLoad
        self.contact = contact
        self.talukas = ["PONDA", "PANAJI"]
        self.cidTalukas = ["PON", "PAN"]
        self.district = ["SOUTH GOA","NORTH GOA"]
        self.cursor = cursor
    
    def validateTaluka(self):
        if self.taluka in self.talukas:
            return True
        else:
            return False

    def validateCId(self):
        self.cursor.execute('SELECT * FROM consumer WHERE ConID = %s', (self.cid))
        acc = self.cursor.fetchone()
        print(acc)
        if len(self.cid) == 11 and self.cid[:3].upper() in self.cidTalukas and acc == None:
            return True
        else:
            return False
