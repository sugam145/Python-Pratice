import mysql.connector

# Connect to the database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="roomsewa"
)

cursor = connection.cursor()

# Example query: Fetching all rows from a table
cursor.execute("SELECT * FROM tblguest")

# Fetching all rows from the executed query
rows = cursor.fetchall()

for row in rows:
    print(row)

# Closing the cursor and connection
cursor.close()
connection.close()
