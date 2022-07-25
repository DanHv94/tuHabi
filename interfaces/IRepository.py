'''
File that contains the abstract class of a repository
'''
from abc import ABC, abstractmethod

class IRepository(ABC):
    '''
    Abstract class that defines some methods that every repository must have
    '''
    @abstractmethod
    def __init__(self):
        '''
        Method that inits the repository object
        '''
    
    @abstractmethod
    def find_one(self, _projection, _filter, _orderby):
        '''
        Method to get one element from the table

        Args:
            _projection: The fields to be retrieved
            _filter: The conditions to filter the ResultSet
        '''

    @abstractmethod
    def find_many(self, _projection, _filter, _orderby):
        '''
        Method to get multiple elements from the table

        Args:
            _projection: The fields to be retrieved
            _filter: The conditions to filter the ResultSet
        '''