from pyindex.reader.reader import Reader
import json


class JsonReader(Reader):
    
    def __init__(self, filename):
        self.filename = filename
    
    
    def open(self):
        self.f = open(self.filename, 'r')


    def get_next(self):
        if self.f:
            line = self.f.readline()
            if line != "":
                js = json.loads(line)
                return js
        return None
