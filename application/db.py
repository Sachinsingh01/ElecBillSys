import pymysql
#create a conection object storing the database connection details
conn = pymysql.connect(
    host = 'localhost',
    database = 'test',
    user = 'root',
    password = '',
    cursorclass = pymysql.cursors.DictCursor
)

cursor = conn.cursor()

#createConsumerTable stores the query to create a new consumer table
createConsumerTable = """ CREATE TABLE Consumer (
    ConID varchar(12) PRIMARY KEY,
    ConFirstName varchar(30) NOT NULL,
    ConLastName varchar(30) NOT NULL,
    ConAddress varchar(30) NOT NULL,
    ConTaluka varchar(15) NOT NULL,
    ConDistrict varchar(15) NOT NULL,
    ConPinCode varchar(6) NOT NULL,
    MeterID varchar(15) NOT NULL UNIQUE,
    ConType varchar(3) NOT NULL,
    ConSanctionedLoad integer NOT NULL,
    ConContact varchar(10) NOT NULL UNIQUE
);
"""

#createDistributorTable stores the query to create a new distributor table
createDistributorTable = """ CREATE TABLE Distributor (
    DisID varchar(12) PRIMARY KEY,
    DisName varchar(40) NOT NULL,
    DisAddress varchar(40) NOT NULL,
    DisTaluka varchar(15) NOT NULL,
    DisDistrict varchar(15) NOT NULL,
    DisPincode varchar(6) NOT NULL,
    SupplyPerMonth real NOT NULL,
    DisContact varchar(10) NOT NULL UNIQUE,
    SupplyRate real NOT NULL
);
"""

#createSubsidy stores the query to create a new subsidy table
createSubsidy = """ CREATE TABLE Subsidy (
    SubID varchar(12) PRIMARY KEY,
    SubPercent float NOT NULL,
    TypeCon varchar(20) NOT NULL
);
"""
#createCWMRMonthReading stores the query to create a new consumer wise meter reading  table to store monthly reading values
createCWMRMonthReading =  """ CREATE TABLE CwmrMonthReading (
    ReadingID varchar(12) PRIMARY KEY,
    Reading varchar(30) NOT NULL
);
"""

#createCWMRMonthDate stores the query to create a new cwmrMonthDate table to store the reading date
createCWMRMonthDate = """ CREATE TABLE CwmrMothDate (
    ReadingID varchar(12) PRIMARY KEY,
    ReadDate DATE NOT NULL,
    ConID varchar(12) NOT NULL
);
"""

#createConBillsDetails stores the query to create a new consumer bills details table
createConBillsDetails = """ CREATE TABLE ConBillsDetails (
    BillID varchar(12) PRIMARY KEY,
    Amount float NOT NULL,
    DueDate DATE NOT NULL,
    StartDate DATE NOT NULL,
    EndDate DATE NOT NULL,
    ConID varchar(12) NOT NULL
);
"""

#createConsumerTable stores the query to create a new Bill correction details table
createBillCorrecDetails = """ CREATE TABLE BillCorrecDetails (
    BillCorrID integer(10) PRIMARY KEY,
    BillID varchar(12) NOT NULL,
    Status varchar(10) NOT NULL,
    Comment varchar(500),
    FieldToCorrect varchar(20) NOT NULL,
    ConID varchar(12) NOT NULL,
    Amount float NOT NULL
);
"""
#createNotice stores the query to create a new notice table
# createNotice = """ CREATE TABLE Notice (
#     NoticeID varchar(12) PRIMARY KEY,
#     BillID varchar(12) NOT NULL,
#     Fine float,
#     Days integer
# );
# """

#

#billingCalInfo stores query to create a new BillingCalendarInfo table
createBillingCalInfo = """ CREATE TABLE BillingCalendarInfo (
    BillTypeID integer(3) PRIMARY KEY,
    StartFrom DATE NOT NULL,
    BillType varchar(8) NOT NULL,
    TimeUnitPassed integer(2) NOT NULL,
    TimeDelta varchar(4) NOT NULL
);
"""
#createElectricityRates stores query to create a new ElectricityRates table
createElectricityRates = """ CREATE TABLE ElectricityRates (
    ErID varchar(12) PRIMARY KEY,
    ConType varchar(3) NOT NULL,
    ApplicableFrom DATE NOT NULL
);
"""

#createGenCharges stores query to create a new General Charges table
createGenCharges = """ CREATE TABLE GenCharges (
    ErID varchar(12) PRIMARY KEY,
    FromUnits int(10),
    ToUnits int(10),
    GenCharges real,
    CONSTRAINT FK_ErID1 
    FOREIGN KEY (ErID)
    REFERENCES ElectricityRates(ErID)
    ON DELETE CASCADE
);
"""

#createFPPCACharges stores query to create a new FPPCA charges table
createFPPCACharges = """ CREATE TABLE FPPCACharges (
    ErID varchar(12) PRIMARY KEY,
    FromUnits int(10),
    ToUnits int(10),
    FPPCACharges real,
    CONSTRAINT FK_ErID2 
    FOREIGN KEY (ErID)
    REFERENCES ElectricityRates(ErID)
    ON DELETE CASCADE
);
"""

createFixedCharges = """ CREATE TABLE FixedCharges (
    ErID varchar(12) PRIMARY KEY,
    FixedCharges real,
    CONSTRAINT FK_ErID3 
    FOREIGN KEY (ErID)
    REFERENCES ElectricityRates(ErID)
    ON DELETE CASCADE
);
"""

#createDiscoms stores query to create a new Discoms table
createDiscoms = """ CREATE TABLE Discoms (
    DiscomID varchar(12) PRIMARY KEY,
    DiscomName varchar(20) NOT NULL,
    DiscomAdd varchar(30) NOT NULL,
    DiscomTaluka varchar(15) NOT NULL,
    DiscomDistrict varchar(15) NOT NULL,
    DiscomPin varchar(6) NOT NULL,
    DiscomContact varchar(10) NOT NULL
);
"""

#createPaymentInfo stores query to create a new payment information table
createPaymentInfo = """ CREATE TABLE PaymentInfo (
    TransactionID varchar(12) PRIMARY KEY,
    BillID varchar(12) NOT NULL,
    ModeOfPayment varchar(8) NOT NULL,
    PaymentDate DATE NOT NULL,
    AmountPaid float NOT NULL
);
"""
# testTable =  """ CREATE TABLE user (
#     id integer PRIMARY KEY,
#     password varchar(12) NOT NULL
# );
# """
#testInsert = """ INSERT INTO user VALUES (1,"rajesh");
#"""

#cursor.execute(createConsumerTable)
#cursor.execute(createDistributorTable)
#cursor.execute(createSubsidy)
#cursor.execute(createConMeterReadForMonth)
#cursor.execute(createConBillsDetails)
#cursor.execute(createBillCorrecDetails)
#cursor.execute(createBillingCalInfo)
#cursor.execute(createElectricityRates)
#cursor.execute(createDiscoms)
#cursor.execute(createPaymentInfo)
cursor.execute(createElectricityRates)
cursor.execute(createGenCharges)
cursor.execute(createFPPCACharges)
cursor.execute(createFixedCharges)
conn.close()
