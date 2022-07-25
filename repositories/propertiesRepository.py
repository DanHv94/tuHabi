from logging import getLogger

from typing import List
from fastapi import Depends
from repositories.generic import mysqlRepository

from contexts import get_mysql

logger = getLogger()

class propertiesRepository(mysqlRepository):

    def __init__(self, connection = Depends(get_mysql)) -> None:
        super().__init__()
        self.set_connection(connection)
        self.set_table("property")

    def get_properties(self, projection: str, filter: str = "") -> List:
        '''
        Get all properties that match projection criteria

        Args:
            projection: the fields to be retrieved
            filter: the criteria to filter data
        '''
        properties = self.find_many(projection, filter)
        return properties