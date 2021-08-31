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
# cursor.execute(createConsumerTable)
# conn.close()
