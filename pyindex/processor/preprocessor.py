from pyindex.processor.processor import Processor
import string

class PreProcessor(Processor):
    
    def __init__(self, reader, fields):
        super(PreProcessor, self).__init__(reader)
        self.fields = fields
        self.str_fields = self.fields.get("str", [])
        self.int_fields = self.fields.get("int", [])
        self.id = self.fields["id"]
        self.current_id = 0

    def process_next(self, current):
        fresult = []
        fresult.append(self.current_id)
        fresult.append(current[self.id])

        for x in self.str_fields:
            cr = current.get(x, [])
            if type(cr) is not list:
                cr = [cr]
            fresult.append([t.lower().translate(str.maketrans('','',string.punctuation)) for t in cr])
        
        for x in self.int_fields:
            t = current.get(x,-1)
            if t  == "":
                t = None
            else:
                t = int(t)
            fresult.append(t)

        self.current_id +=  1
        return fresult
