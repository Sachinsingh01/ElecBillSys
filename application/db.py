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


createConnectionTable = """ CREATE TABLE Connection (
    Co_ID integer(18) PRIMARY KEY,
    Co_Address varchar(40) NOT NULL,
    Co_Taluka varchar(20) NOT NULL,
    Co_District varchar(20) NOT NULL,
    Co_Pin integer(6) NOT NULL,
    Meter_No integer(18) NOT NULL,
    Conn_Type_ID int(3) NOT NULL,
    Con_ID int(18) NOT NULL,
    Installation_ID integer(18) NOT NULL,
    Installation_Date Date NOT NULL,
    Connection_Status varchar(8) NOT NULL,
    Created DATE NOT NULL,
    Updated DATE NOT NULL,
    CONSTRAINT FK_connectionconID 
    FOREIGN KEY (Con_ID)
    REFERENCES Consumer(Con_ID)
);
"""

#FK for contype to be added
#createConsumerTable stores the query to create a new consumer table
createConsumerTable = """ CREATE TABLE Consumer (
    Con_ID integer(18) PRIMARY KEY AUTO_INCREMENT,
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
    Created DATE NOT NULL,
    Updated DATE NOT NULL
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
createConBillsDetails = """ CREATE TABLE Con_Bills_Details (
    Bill_ID varchar(12) PRIMARY KEY,
    Amount float NOT NULL,
    Due_Date DATE NOT NULL,
    Start_Date DATE NOT NULL,
    End_Date DATE NOT NULL,
    Con_ID integer(18) NOT NULL,
    CONSTRAINT FK_conbilldetailsconID 
    FOREIGN KEY (Con_ID)
    REFERENCES Consumer(Con_ID)
    ON DELETE CASCADE
);
"""

#createConsumerTable stores the query to create a new Bill correction details table
createBillCorrecDetails = """ CREATE TABLE Bill_Correc_Details (
    Bill_Corr_ID integer(10) PRIMARY KEY,
    Bill_ID varchar(12) NOT NULL,
    Status varchar(10) NOT NULL,
    Comment varchar(500),
    Field_To_Correct varchar(20) NOT NULL,
    Con_ID integer(18) NOT NULL,
    Amount float NOT NULL,
    CONSTRAINT FK_billcorrecdetconID 
    FOREIGN KEY (Con_ID)
    REFERENCES Consumer(Con_ID)
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
createBillingCalInfo = """ CREATE TABLE Billing_Calendar_Info (
    Bill_Type_ID integer(3) PRIMARY KEY,
    Start_From DATE NOT NULL,
    Bill_Type varchar(8) NOT NULL,
    Time_Unit_Passed integer(2) NOT NULL,
    Time_Delta varchar(4) NOT NULL
);
"""

createConType = """ CREATE TABLE Con_Type (
    Con_Type_ID integer(3) PRIMARY KEY,
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
    Updated Date NOT NULL,
    CONSTRAINT FK_meterreadcoid 
    FOREIGN KEY (Co_ID)
    REFERENCES Connection(Co_ID)
);
"""
#fkcontype to be added
createNoSlabCharges = """ CREATE TABLE No_Slab_Charges (
    NSC_ID integer(10) PRIMARY KEY,
    Con_Type_ID integer(3) NOT NULL,
    NS_Charge_Type varchar(10) NOT NULL,
    NS_Charges varchar(11) NOT NULL,
    From_Date Date NOT NULL,
    Created Date NOT NULL,
    Updated Date NOT NULL,
    CONSTRAINT FK_noslabchargecontypeid
    FOREIGN KEY (Con_Type_ID)
    REFERENCES Con_Type(Con_Type_ID)
);
"""

#fk ontypeid to be added
createSlabCharges = """ CREATE TABLE Slab_Charges (
    SC_ID integer(10) PRIMARY KEY,
    Con_Type_ID integer(3) NOT NULL,
    From_Date DATE NOT NULL,
    S_Charge_Type varchar(10) NOT NULL,
    Slab_ID integer(3) NOT NULL,
    Created Date NOT NULL,
    Updated Date NOT NULL,
    CONSTRAINT FK_slabchargecontypeid
    FOREIGN KEY (Con_Type_ID)
    REFERENCES Con_Type(Con_Type_ID),
    CONSTRAINT FK_slabchargesslabid
    FOREIGN KEY (Slab_ID)
    REFERENCES Slab_Types(Slab_ID)
);
"""

createSlabTypes = """ CREATE TABLE Slab_Types (
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
    Discom_ID varchar(12) PRIMARY KEY,
    Discom_Name varchar(20) NOT NULL,
    Discom_Add varchar(30) NOT NULL,
    Discom_Taluka varchar(15) NOT NULL,
    Discom_District varchar(15) NOT NULL,
    Discom_Pin varchar(6) NOT NULL,
    Discom_Contact varchar(10) NOT NULL
);
"""

#createPaymentInfo stores query to create a new payment information table
createPaymentInfo = """ CREATE TABLE Payment_Info (
    Transaction_ID varchar(12) PRIMARY KEY,
    Bill_ID varchar(12) NOT NULL,
    Mode_Of_Payment varchar(8) NOT NULL,
    Payment_Date DATE NOT NULL,
    Amount_Paid float NOT NULL
);
"""
# cursor.execute(createConsumerTable)
# cursor.execute(createConType)
# cursor.execute(createConnectionTable)
#cursor.execute(createMeterReading)
#cursor.execute(createSlabTypes)
# cursor.execute(createSlabCharges)
# cursor.execute(createNoSlabCharges)
#cursor.execute(createBillsData)

#cursor.execute(createDistributorTable)

#cursor.execute(createConBillsDetails)
# cursor.execute(createBillCorrecDetails)
# cursor.execute(createBillingCalInfo)
# cursor.execute(createDiscoms)
# cursor.execute(createPaymentInfo)

conn.close()
