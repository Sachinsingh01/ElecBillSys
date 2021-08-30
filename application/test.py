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
# id = "1"
# pas = "rajesh"
# sql_query = """INSERT INTO user_1 (uid, password) VALUES (%s, %s)"""

# cursor.execute(sql_query,(id, pas))
# conn.commit()

# id = 1
# pas = "rajesh"
# sql_query = """INSERT INTO user (id, password) VALUES (%s, %s)"""

# cursor.execute(sql_query,(id, pas))
# conn.commit()

cursor.execute("SELECT * FROM user")

print(cursor.fetchall())