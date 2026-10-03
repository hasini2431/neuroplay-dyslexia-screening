import sqlite3

connection = sqlite3.connect("users.db")
cursor = connection.cursor()

cursor.execute("PRAGMA table_info(users)")

columns = cursor.fetchall()

for column in columns:
    print(column)

connection.close()