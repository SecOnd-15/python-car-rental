import mysql.connector
from Database.DatabaseManager import DatabaseManager
from Database.Insert import Insert

config = {
    'host': 'localhost',
    'user': 'root',
    'password': ''
}

conn = mysql.connector.connect(**config)
cursor = conn.cursor()

# Set up database and tables
db_manager = DatabaseManager(conn, cursor)
db_manager.bootstrap()