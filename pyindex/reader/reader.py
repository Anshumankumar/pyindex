from abc import ABC, abstractmethod

class Reader(ABC):
    
    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def get_next(self):
        pass

    def __iter__(self):
        return self

    def __next__(self):
        res =  self.get_next()
        if res is None:
             raise StopIteration()
        return res
