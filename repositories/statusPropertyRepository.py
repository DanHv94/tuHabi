from logging import getLogger

from typing import List
from fastapi import Depends
from repositories.generic import mysqlRepository

from contexts import get_mysql

logger = getLogger()

class statuspropertyRepository(mysqlRepository):

    def __init__(self, connection = Depends(get_mysql)) -> None:
        super().__init__()
        self.set_connection(connection)
        self.set_table("status_history")

    def get_status_per_property(self, data: List, filter: int = None) -> List:
        '''
        Set the status per property

        Args:
            data: data to be consulted
        '''
        new_data = []
        _filter = [filter] if filter else range(3,6)
        for datum in data:
            try:
                status = self.find_one("status_id", "property_id = " + str(datum["id"]), 
                                    "update_date DESC")
                if(status):
                    status_id = status["status_id"]
                    if(status_id in _filter):
                        datum["status"] = "preventa" if status_id == 3 else ("en venta" if status_id == 4 else "vendido")
                        new_data.append(datum)
            except Exception as error:
                logger.error("Error when trying to retrieve property data with id " + str(datum["id"]) + f" {error}")
                continue
            
        return new_data