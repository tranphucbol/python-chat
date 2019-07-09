import mysql.connector

# Connect with the MySQL Server
config = {
    'user': 'root',
    'password': 'password',
    'host': '127.0.0.1',
    'database': 'chat'
}

def createConnect():
    return mysql.connector.connect(**config)