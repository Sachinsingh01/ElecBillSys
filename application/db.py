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

#FK for contype to be added
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
    SubsidyID varchar(12) PRIMARY KEY,
    SubPercent float NOT NULL
);
"""
#createCWMRMonthReading stores the query to create a new consumer wise meter reading  table to store monthly reading values
createCWMRMonthReading =  """ CREATE TABLE CwmrMonthReading (
    ReadingID varchar(12) PRIMARY KEY,
    Reading varchar(30) NOT NULL,
    CONSTRAINT FK_ReadingID 
    FOREIGN KEY (ReadingID)
    REFERENCES CwmrMonthDate(ReadingID)
    ON DELETE CASCADE
);
"""

#createCWMRMonthDate stores the query to create a new cwmrMonthDate table to store the reading date
createCWMRMonthDate = """ CREATE TABLE CwmrMonthDate (
    ReadingID varchar(12) PRIMARY KEY,
    ReadDate DATE NOT NULL,
    ConID varchar(12) NOT NULL,
    CONSTRAINT FK_cwmrconID 
    FOREIGN KEY (ConID)
    REFERENCES Consumer(ConID)
    ON DELETE CASCADE
);
"""

#createConBillsDetails stores the query to create a new consumer bills details table
createConBillsDetails = """ CREATE TABLE ConBillsDetails (
    BillID varchar(12) PRIMARY KEY,
    Amount float NOT NULL,
    DueDate DATE NOT NULL,
    StartDate DATE NOT NULL,
    EndDate DATE NOT NULL,
    ConID varchar(12) NOT NULL,
    CONSTRAINT FK_conbilldetailsconID 
    FOREIGN KEY (ConID)
    REFERENCES Consumer(ConID)
    ON DELETE CASCADE
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
    Amount float NOT NULL,
    CONSTRAINT FK_billcorrecdetconID 
    FOREIGN KEY (ConID)
    REFERENCES Consumer(ConID)
    ON DELETE CASCADE
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
    RatesRefID varchar(12),
    ConType varchar(3),
    ApplicationFrom DATE,
    GenChargeID varchar(12) NOT NULL,
    FPPCAChargeID varchar(12) NOT NULL,
    FixedChargeID varchar(12) NOT NULL,
    SusbsidyID varchar(12) NOT NULL,
    CONSTRAINT PK_elecrates PRIMARY KEY (RatesRefID,ConType,ApplicationFrom),
    CONSTRAINT FK_elecratesgencharge
    FOREIGN KEY (GenChargeID)
    REFERENCES GenCharges(GenChargeID),
    CONSTRAINT FK_elecratesfppcacharge 
    FOREIGN KEY (FPPCAChargeID)
    REFERENCES FPPCACharges(FPPCAChargeID),
    CONSTRAINT FK_elecratesfixedcharge 
    FOREIGN KEY (FixedChargeID)
    REFERENCES FixedCharges(FixedChargeID)
);
"""

#createGenCharges stores query to create a new General Charges table
createGenCharges = """ CREATE TABLE GenCharges (
    GenChargeID varchar(3),
    MaxUnits real,
    GenCharges real NOT NULL,
    CONSTRAINT PK_gencharges PRIMARY KEY (GenChargeID, MaxUnits)
);
"""

#createFPPCACharges stores query to create a new FPPCA charges table
createFPPCACharges = """ CREATE TABLE FPPCACharges (
    FPPCAChargeID varchar(3),
    MaxUnits real,
    FPPCACharges real NOT NULL,
    CONSTRAINT PK_fppcacharge PRIMARY KEY (FPPCAChargeID,MaxUnits)
);
"""

#createFixedCharges stores query to create a new Fixed Charges table
createFixedCharges = """ CREATE TABLE FixedCharges (
    FixedChargeID varchar(3) PRIMARY KEY,
    FixedCharges real NOT NULL
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
    AmountPaid float NOT NULL,
    CONSTRAINT FK_paymentinfobillID 
    FOREIGN KEY (BillID)
    REFERENCES ConBillsDetails(BillID)
    ON DELETE CASCADE
);
"""
# testTable =  """ CREATE TABLE user (
#     id integer PRIMARY KEY,
#     password varchar(12) NOT NULL
# );
# """
#testInsert = """ INSERT INTO user VALUES (1,"rajesh");
#"""
# cursor.execute(createGenCharges)
# cursor.execute(createFPPCACharges)
#cursor.execute(createFixedCharges)
#cursor.execute(createElectricityRates)
#cursor.execute(createConsumerTable)
#cursor.execute(createDistributorTable)
#cursor.execute(createSubsidy)
#cursor.execute(createCWMRMonthDate)
#cursor.execute(createCWMRMonthReading)
#cursor.execute(createConBillsDetails)
#cursor.execute(createBillCorrecDetails)
#cursor.execute(createBillingCalInfo)
#cursor.execute(createDiscoms)
#cursor.execute(createPaymentInfo)
conn.close()
