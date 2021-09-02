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
    DisAddress varchar NOT NULL,
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
#createConMeterReadForMonth stores the query to create a new consumer wise meter reading per month table
createConMeterReadForMonth =  """ CREATE TABLE Cwmr_Month (
    ConID varchar(12),
    ReadDate DATE NOT NULL,
    Reading varchar(30) NOT NULL,
    CONSTRAINT meterread_pk PRIMARY KEY (ConID,ReadDate)
);
"""

#createConBillsDetails stores the query to create a new consumer bills details table
createConBillsDetails = """ CREATE TABLE Con_Bills_Details (
    BillID varchar(12) PRIMARY KEY,
    Amount float NOT NULL,
    DueDate DATE NOT NULL,
    StartDate DATE NOT NULL,
    EndDate DATE NOT NULL,
    ConID varchar(12) NOT NULL
);
"""

#createConsumerTable stores the query to create a new Bill correction details table
createBillCorrecDetails = """ CREATE TABLE Bill_Correc_Details (
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
ConType varchar(3),
ApplicableFrom DATE,
FromUnits integer(10),
ToUnits integer(10),
Rate real,
CONSTRAINT elecrates_pk PRIMARY KEY (ConType,ApplicableFrom)
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
# cursor.execute(createDistributorTable)
# cursor.execute(createSubsidy)
# cursor.execute(createConMeterReadForMonth)
# cursor.execute(createConBillsDetails)
# cursor.execute(createBillCorrecDetails)
# cursor.execute(createBillingCalInfo)
# cursor.execute(createElectricityRates)
# cursor.execute(createDiscoms)
# cursor.execute(createPaymentInfo)
conn.close()
