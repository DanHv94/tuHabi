'''
File that contains the definition of the MySQL Repository class.
This class is the base class of all repositories and implements the
IRepository interface to connect to MySQL.

Attributes:
    logger(logging.Logger): Configured logger object
'''
import logging
from typing import List

from interfaces.IRepository import IRepository

logger = logging.getLogger(__name__)

class mysqlRepository(IRepository):
    '''
    Generic class to implement database logic for mysql. This agnostic class
    implements CRUD at database level.

    Instance Attributes:

    '''
    def __init__(self) -> None:
        super().__init__()
        self.__connection = None
        self.__table = ""

    def set_connection(self, connection):
        '''
        Sets the connection   

        Args:
            connection: Connection to MySQL
        '''
        self.__connection = connection
    
    def set_table(self, table):
        '''
        Sets the table

        Args:
            table: The name of the table to be handled
        '''
        self.__table = table

    def find_one(self, _projection: str, _filter: str = "", _orderby: str = ""):
        '''
        Method to get one element from db

        Args:
            __projection(str): Fields to be retrieved
            __filter(str): Criteria to filter

        Returns:
            A cursor with the row
        '''
        #with self.__connection:
        with self.__connection.cursor() as cursor:
            sql = f"SELECT {_projection} FROM {self.__table} "
            if(_filter != ""):
                sql += f"WHERE {_filter}"
            if(_orderby != ""):
                sql += f" ORDER BY {_orderby}"
            cursor.execute(sql)
            result = cursor.fetchone()
            return result
        return None 

    def find_many(self, _projection: str, _filter: str = "", _orderby: str = ""):
        '''
        Method to get elements from db

        Args:
            __projection(str): Fields to be retrieved
            __filter(str): Criteria to filter

        Returns:
            A cursor with the rows
        '''
        #with self.__connection:
        with self.__connection.cursor() as cursor:
            sql = f"SELECT {_projection} FROM {self.__table} "
            if(_filter != ""):
                sql += f"WHERE {_filter}"
            if(_orderby != ""):
                sql += f" ORDER BY {_orderby}"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        return None 
