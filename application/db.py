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
    Con_ID varchar(12) PRIMARY KEY,
    Consumer_No varchar(12) NOT NULL,
    Con_First_Name varchar(30) NOT NULL,
    Con_Last_Name varchar(30) NOT NULL,
    Con_Address varchar(30) NOT NULL,
    Con_Taluka varchar(15) NOT NULL,
    Con_District varchar(15) NOT NULL,
    Con_Pin_Code varchar(6) NOT NULL,
    Meter_ID varchar(15) NOT NULL UNIQUE,
    Con_Type_ID varchar(3) NOT NULL,
    Con_Sanctioned_Load real NOT NULL,
    ConContact varchar(10) NOT NULL UNIQUE,
    Created Date NOT NULL,
    Updated Date NOT NULL
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

createConType = """ CREATE TABLE Con_Type (
    Con_Type_ID integer(3) NOT NULL,
    Con_Type varchar(10) NOT NULL,
    San_Load varchar(18) NOT NULL,
    Susbsidy_Percent float,
    Created Date NOT NULL,
    Updated Date NOT NULL
);
"""

createMeterReading = """ CREATE TABLE Meter_Reading (
    Meter_No varchar(12) PRIMARY KEY,
    Co_ID integer(18) NOT NULL,
    Meter_Reading varchar(18) NOT NULL,
    Read_Date DATE NOT NULL,
    Meter_Status varchar(10) NOT NULL,
    Created Date NOT NULL,
    Updated Date NOT NULL
);
"""

createNoSlabCharges = """ CREATE TABLE No_Slab_Charges (
    NSC_ID integer(10) PRIMARY KEY,
    Con_Type_ID integer(3) NOT NULL,
    NS_Charge_Type varchar(10) NOT NULL,
    NS_Charges varchar(11) NOT NULL,
    From_Date Date NOT NULL,
    Created Date NOT NULL,
    Updated Date NOT NULL,
);
"""

createSlabCharges = """ CREATE TABLE Slab_Charges (
    SC_ID integer(10) PRIMARY KEY,
    Con_Type_ID integer(3) NOT NULL,
    From_Date DATE NOT NULL,
    S_Charge_Type varchar(10) NOT NULL,
    Slab_ID integer(3) NOT NULL,
    Created Date NOT NULL,
    Updated Date NOT NULL
);
"""

createSlabTypes = """ CREATE TABLE SlabTypes (
    Slab_ID integer(3) PRIMARY KEY,
    Units_From integer(11) NOT NULL,
    Units_To integer(11) NOT NULL,
    S_Charges varchar(11) NOT NULL,
    Created DATE NOT NULL,
    Updated DATE NOT NULL
);
"""

createBillsData = """ CREATE TABLE Bills_Data (
    BD_ID int(18) PRIMARY KEY,
    Meter_No varchar(12),
    Unit varchar(12),
    Current_Read_Date Date,
    Prev_Read_Date Date,
    Prev_Reading varchar(18),
    Reading_Diff varchar(18),
    Consumption varchar(12),
    Reading_Remark varchar(12),
    Created Date NOT NULL,
    Updated Date NOT NULL
);
"""

#TABLE BILL CLACULATION TABLE TO BE ADDED HERE

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
