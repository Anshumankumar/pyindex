from pyindex.processor.processor import Processor

class FlatMapper(Processor):
    
    def __init__(self, reader):
        super(FlatMapper, self).__init__(reader)
        self.init = False

    def get_next_element(self):
        self.elements = self.reader.get_next()
        self.ccount = 0
   
    def process_next():
        return None

    def get_next(self):
        if self.init == False:
            self.get_next_element()
            self.init = True
        if self.elements is None:
            return None
        if self.ccount == len(self.elements):
            self.get_next_element()
            return self.get_next()
        
        res = self.elements[self.ccount]
        self.ccount +=  1
        if "_id" not in res.keys() or len(res["_id"])>12:
            return self.get_next()
        return res
   
