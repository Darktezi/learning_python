from abc import ABC, abstractmethod

class TableRepository(ABC):
    @abstractmethod
    def get(self, id: int) -> tuple:
        pass
    
    @abstractmethod
    def get_all(self) -> list:
        pass
    
    @abstractmethod
    def add(self, entity):
        pass
    
    # @abstractmethod
    # def delete(self, id: int):
    #     pass