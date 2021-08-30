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

sql_query = """ DROP TABLE user
"""
cursor.execute(sql_query)
conn.close()
