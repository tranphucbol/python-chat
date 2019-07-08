import mysql.connector
from mysql.connector import errorcode

config = {
    'user': 'root',
    'password': 'password',
    'host': '127.0.0.1',
    'database': 'chat'
}

def create_database(cursor):
    try:
        cursor.execute(file('chat.sql').read())
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

if __name__ == '__main__':

    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        create_database(cursor)
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

