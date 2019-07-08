import mysql.connector
import sys
from mysql.connector import errorcode

config = {
    'user': 'root',
    'password': 'password',
    'host': '127.0.0.1',
    'database': 'chat'
}

if __name__ == '__main__':

    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor.close()
        cnx.close()