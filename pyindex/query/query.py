import string
from collections import defaultdict
import time
import numpy as np
from Levenshtein import distance

class QueryManager():
    def __init__(self, indexer):
        self.indexer = indexer
        self.sindexlist = indexer.sindexlist
        self.sindexlen  = np.array([len(x) for x in self.sindexlist])

    def search_secondary(self, x):
        qlist = []
        for i in range(0,len(x)):
            if (i < len(x)-3):
                nstr = x[i:i+3]
            else:
                nstr = x[i:len(x)] + "$" + x[0:i+3-len(x)]
            qlist.append(nstr)
        
        arrlist = []
        for q in qlist:
            res = self.indexer.sindex.get(q, [])
            if len(res) > 0:
                arrlist.append(res)
        if len(arrlist) == 0:
            return []
        
        carr, counts = np.unique(np.concatenate(arrlist), return_counts=True )
        
        sc  = counts/(self.sindexlen[carr] - counts + len(x))
        
        if len(x) > 6:
            THRESHOLD = 0.3
        else: 
            THRESHOLD = 0.05
        flist = [self.sindexlist[txt] for txt in carr[sc > THRESHOLD] ]
        flist = [ (txt,distance(x,txt) - 0.5*self.indexer.cscore[txt] ) for txt in flist]
        flist.sort(key=lambda x:x[1])
        return flist[0:3]


    def intersect(self, l1, l2):
        return np.intersect1d(l1, l2, assume_unique=True)

    def query(self, qstring):
        qstring = qstring.lower().translate(str.maketrans('','',string.punctuation))
        qlist = qstring.split()
        indexes = []
        for x in qlist:
            print((x, len(self.indexer.index.get(x, []))))
            indexes.append(self.indexer.index.get(x, []))
        indexes.sort(key = lambda x: len(x))
        it  = indexes[0]
        for x in indexes[1:]:
            it  = self.intersect(it, x)
        return [self.indexer.imap[x] for x in it]

