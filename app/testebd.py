import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="PI",
    password="131297",
    database="Assaltos"
)

mycursor = db.cursor()
# Add new columns to the 'assaltos' table


# Add the 'escolaridade' column to the 'assaltos' table
alter_table_query = "ALTER TABLE assaltos DROP COLUMN ocorrido"
mycursor.execute(alter_table_query)