from pyindex.processor.processor import Processor
from collections import defaultdict

class Indexer(Processor):
    
    def __init__(self, reader):
        super(Indexer, self).__init__(reader)
        self.index = defaultdict(list)        
        self.sindex = defaultdict(lambda:defaultdict(list))        

    def process_doc(self, docid, doc):
        if type(doc) is not list:
            self.index[doc].append(docid)
            return
 
        for y in doc:
           for z in y.split():
                self.index[z].append(docid)     
    
    def process_next(self, current):
        docid = current[0]
        for x in current[2:]:
            self.process_doc(docid, x)
        return True
    
    def create_secondary(self):
        for x in self.index.keys():
            if (type(x) is not str or len(x) < 4):
                continue
            for i in range(0,len(x)):
                if (i < len(x)-3):
                    nstr = x[i:i+3]
                else:
                    nstr = x[i:len(x)] + "$" + x[0:i+3-len(x)]
                self.sindex[nstr][min(10,len(x))].append(x)
                   

    def create_index(self):
        i = 0
        while(self.get_next() is not None and i < 1000000):
            i += 1
            continue
        self.create_secondary()
