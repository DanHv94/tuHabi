'''
File that creates a database connection with MySQL and yields a
connection objects as a singleton
'''

from pymysql import connect
from pymysql.cursors import DictCursor

from config import MYSQL_HOST, MYSQL_DB, MYSQL_PASSWORD, MYSQL_PORT, MYSQL_USER
from models.singleton import Singleton

class mysqlConnection(metaclass=Singleton):
    '''Class that creates the connection with MySQL'''
    def __init__(self):
        self.connection = connect(host=MYSQL_HOST, 
        user=MYSQL_USER, password=MYSQL_PASSWORD, port=MYSQL_PORT,
        database=MYSQL_DB, cursorclass=DictCursor)

def get_mysql():
    '''
    Creates a MySQLConnection instance and returns it

    Returns:
        connection: MySQL connection
    '''
    mysql = mysqlConnection()
    yield mysql.connection