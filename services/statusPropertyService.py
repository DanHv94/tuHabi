import logging
from typing import List

from fastapi import Depends

from repositories.statusPropertyRepository import statuspropertyRepository

logger = logging.getLogger(__name__)

class StatusPropertiesService():
    def __init__(self, repository: statuspropertyRepository = Depends()):
        self.__repository = repository
    
    def get_properties_status(self, properties: List, filter: int = None) -> List:
        properties = self.__repository.get_status_per_property(properties, filter)
        return properties