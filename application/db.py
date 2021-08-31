import pymysql

conn = pymysql.connect(
    host = 'sql6.freemysqlhosting.net',
    database = 'sql6433489',
    user = 'sql6433489',
    password = 'tC7bZ7lzuf',
    charset = 'utf8mb4',
    cursorclass = pymysql.cursors.DictCursor
)

cursor = conn.cursor()

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
createDistributorTable = """ CREATE TABLE Distributor (
    DisID varchar(12) PRIMARY KEY,
    DisName varchar(40) NOT NULL,
    DisAddress varchar NOT NULL,

    DisContact varchar(10) NOT NULL UNIQUE,
    Rate float NOT NULL
);
"""

createSubsidy = """ CREATE TABLE Subsidy (
    SubID varchar(12) PRIMARY KEY,
    SubPercent float NOT NULL,
    Typecon varchar(20) NOT NULL
);
"""

createConMeterReadForMonth =  """ CREATE TABLE Cwmr_Month (
    ConID varchar(12) PRIMARY KEY,
    ReadDate DATE PRIMARY KEY NOT NULL,
    Reading varchar(30) NOT NULL
);
"""

createConBillsDetails = """ CREATE TABLE Con_Bills_Details (
    BillID varchar(12) PRIMARY KEY,
    Amount float NOT NULL,
    DueDate DATE NOT NULL,
    StartDate DATE NOT NULL,
    EndDate DATE NOT NULL,
    ConID varchar(12) NOT NULL
)
"""

createBillCorrecDetails = """ CREATE TABLE Bill_Correc_Details (
    BillID varchar(12) PRIMARY KEY,
    Status varchar(10) NOT NULL,
    Comment varchar(500),
    FieldToCorrect varchar(20) NOT NULL,
    ConID varchar(12) NOT NULL,
    Amount float NOT NULL
)
"""

createNotice = """ CREATE TABLE Notice (
    NoticeID varchar(12) PRIMARY KEY,
    BillID varchar(12) NOT NULL,
    Fine float,
    Days integer
)
"""

#

# createElectricityRates = """ CREATE TABLE Electricity_Rates (
    
# )
# """

# createDiscoms = """ CREATE TABLE Discoms (
    
# )
# """

#cursor.execute(createConsumerTable)
conn.close()
