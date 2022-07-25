import logging
from typing import List

from fastapi import Depends

from repositories.propertiesRepository import propertiesRepository

logger = logging.getLogger(__name__)

class PropertiesService():
    def __init__(self, repository: propertiesRepository = Depends()):
        self.__repository = repository
    
    def get_properties(self, projection: str, filter: str = None) -> List:
        if not filter:
            filter = ""
        properties = self.__repository.get_properties(projection, filter)
        return properties