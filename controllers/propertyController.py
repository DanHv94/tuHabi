from logging import getLogger

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from starlette.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR)

from services import PropertiesService, StatusPropertiesService
from typing import Optional, Union

router = APIRouter()
logger = getLogger(__name__)

@router.get("/PropertiesInfo")
async def getPropertiesInfo(year: Optional[int] = None, city: Optional[str] = None, 
        status: Optional[Union[str, int]] = None,
        service: PropertiesService = Depends(), serviceStatus: StatusPropertiesService = Depends()):
    '''
    Endpoint that gets properties' info

    Query parameters:
    ---
        year: The year of the property
        city: The city where the property is located
        status: The status in which the property is. Values can be 'preventa' [3], 'en venta' [4], 'vendido' [5]
    '''
    filter_property = ""
    status_dict = {"preventa": 3, "en venta": 4, "vendido": 5, "3": 3, "4": 4, "5": 5}
    if(year):
        if(type(year) != int):
            return JSONResponse("Year parameter must be integer", HTTP_400_BAD_REQUEST)
        filter_property = f"year = {year} AND "
    if(city):
        filter_property += f"city LIKE '%{city}%'"
    filter_property = filter_property.rstrip("AND ")
    #In the case of status, we map strings to the id of the status
    if(status):
        if(type(status) == int and status in [3, 4, 5]):
            pass
        elif (type(status) == str):
            status = status_dict.get(status.lower(), None)
            if(not status):
                return JSONResponse("Status parameter value is not supported.", HTTP_400_BAD_REQUEST)
        else:
            return JSONResponse("Status parameter value is not supported.", HTTP_400_BAD_REQUEST)

    properties = service.get_properties("id, address, city, price, description", filter_property)
    properties = serviceStatus.get_properties_status(properties, status)
    return JSONResponse(properties, HTTP_200_OK)