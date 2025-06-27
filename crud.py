import mysql.connector
from mysql.connector import Error

conn = None  # Define conn here so it exists even if connection fails

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mysql@1234",
        database = "indigo"
    )
    if conn.is_connected():
        print("Connected to MySQL")
        mycursor = conn.cursor()
        # You can use mycursor here

except Error as err:
    print(f"Error: {err}")


# #Create a database on the db server
# mycursor.execute("CREATE DATABASE IF NOT EXISTS indigo")
# conn.commit()


# # Create a table
# # airport -> airport_id | code | name
# mycursor.execute("""
# CREATE TABLE airport(
#     airport_id INTEGER PRIMARY KEY,
#     code VARCHAR(10) NOT NULL,
#     city VARCHAR(50) NOT NULL,
#     name VARCHAR(255) NOT NULL
# )
# """)
# conn.commit()



# # Insert data to the table
# mycursor.execute("""
# INSERT INTO airporT VALUES
#     (1 , 'DEL' , 'New Delhi', 'IGIA'),
#     (2, 'CCU', 'Kolkata', 'NSCA'),
#     (3, 'BOM', 'Mumbai', 'CSMA')
#
# """)
# conn.commit()

#Search / Retrieve (Data Comes under tuples or list of tuples)
mycursor.execute("select * from airport WHERE airport_id >1")
data = mycursor.fetchall()
print(data)

for i in data:
    print(i[3])

#Update the data
mycursor.execute("""
UPDATE airport
SET city = "Bombay"
    WHERE airport_id  = 3
""")

#Search / Retrieve (Data Comes under tuples or list of tuples)
mycursor.execute("select * from airport")
data = mycursor.fetchall()
print(data)

#DELETE the data
mycursor.execute("DELETE FROM airport WHERE airport_id = 3")
conn.commit()

#Search / Retrieve (Data Comes under tuples or list of tuples)
mycursor.execute("select * from airport")
data = mycursor.fetchall()
print(data)


# finally:
#     if conn and conn.is_connected():
#         mycursor.close()
#         conn.close()
#         print("MySQL connection is closed")
