import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Mysql@1234",
    database="flights"
)

cursor = conn.cursor()
cursor.execute("ALTER TABLE flights CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
conn.commit()

print("Table character set converted successfully.")

cursor.close()
conn.close()
