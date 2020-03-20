from abc import  abstractmethod
from pyindex.reader.reader import Reader

class Processor(Reader):
    def __init__(self, reader):
        self.reader = reader

    def open(self):
        print("Opening " + self.__class__.__name__ )
        self.reader.open()

    def get_next(self):
        current = self.reader.get_next()
        if current == None:
            return None
        return self.process_next(current)

    @abstractmethod
    def process_next(x, current):
        pass

    def __iter__(self):
        return self

    def __next__(self):
        res =  self.get_next()
        if res is None:
             raise StopIteration()
        return res
