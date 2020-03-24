from pyindex.processor.processor import Processor
from collections import defaultdict
import numpy as np
import math

class Indexer(Processor):
    
    def __init__(self, reader):
        super(Indexer, self).__init__(reader)
        self.index = defaultdict(list)        
        self.cscore = defaultdict(lambda: 0.0)        
        self.sindex = defaultdict(list)        
        self.imap = []
        self.sindexlist = []
        self.aindex = defaultdict(lambda:defaultdict(lambda: 0.0))

    def process_doc(self, docid, doc, score):
        if type(doc) is not list:
            self.index[doc].append(docid)
            self.cscore[doc] += score
            return
        
        for y in doc:
           for z in y.split():
                self.index[z].append(docid)     
                self.cscore[z] += score
    
    def auto_complete_index(self, doc,  score):
        for y  in doc:
            self.aindex[y[0:3]][y]  += score
        

    def process_next(self, current):
        docid = current[0]
        self.imap.append(current[1])
        score = current[-1]
        
        self.auto_complete_index(current[2], score)
        if (current[2][0] == "jiya dhadak dhadak jaye from quotkalyugquot"):
            print(current)
        for x in current[2:-1]:
            self.process_doc(docid, x, score)
        return True
    
    def create_secondary(self):
        nindex = 0
        for x in self.index.keys():
            if (type(x) is not str or len(x) < 4):
                continue
            for i in range(0,len(x)):
                if (i < len(x)-3):
                    nstr = x[i:i+3]
                else:
                    nstr = x[i:len(x)] + "$" + x[0:i+3-len(x)]
                self.sindex[nstr].append(nindex)
            
            self.sindex['$' + x[0:3] ].append(nindex)
            self.sindex['$' + x[0:4] ].append(nindex)
            
            self.sindexlist.append(x)
            nindex += 1
            if (self.cscore[x] > 0):
                self.cscore[x] = math.log10(self.cscore[x])    
        for x in self.sindex.keys():
            self.sindex[x] = np.array(self.sindex[x])
                           

    def create_index(self):
        i = 0
        while(self.get_next() is not None and i < 1000000):
            i += 1
            continue
        for key in self.index.keys():
            self.index[key] = np.unique(np.array(self.index[key]))
        for key in self.aindex.keys():
            self.aindex[key] = [(x,y) for x,y in self.aindex[key].items()]
            self.aindex[key].sort(key = lambda x:x[1], reverse=True)
            self.aindex[key] = [x[0] for x in self.aindex[key]]

        self.create_secondary()
