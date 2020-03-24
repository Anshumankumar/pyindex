import string
from collections import defaultdict
import time
import numpy as np
from Levenshtein import distance
import re

class QueryManager():
    def __init__(self, indexer):
        self.indexer = indexer
        self.sindexlist = indexer.sindexlist
        self.sindexlen  = np.array([len(x) for x in self.sindexlist])

    def auto_complete(self, x):
        qlist = [ '$' + x[0:3] ]
        if len(x) > 3:
            qlist.append('$' + x[0:4])
         
        arrlist = []
        for q in qlist:
            res = self.indexer.sindex.get(q, [])
            if len(res) > 0:
                arrlist.append(res)
        if len(arrlist) == 0:
            return []
        
        carr, counts = np.unique(np.concatenate(arrlist), return_counts=True )
        
        
        flist = [(self.sindexlist[txt],(sc + 0.2*self.indexer.cscore[self.sindexlist[txt]]))  for txt,sc in zip(carr, counts)  ]
        flist.sort(key=lambda x:x[1], reverse=True)
        return flist[0:10]



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
        sindex = 0
        if (x == flist[0][0]):
            sindex = 1
        return flist[sindex:sindex+3]


    def intersect(self, l1, l2):
        return np.intersect1d(l1, l2, assume_unique=True)

    def get_top_list(self, indexes):
        indexes.sort(key = lambda x: len(x))
        if len(indexes) == 0:
            return []
        it  = indexes[0]
        for x in indexes[1:]:
            it  = self.intersect(it, x)
        return it
 
    def autocomplete(self, qstring):
        qstring = qstring.lower().translate(str.maketrans('','',string.punctuation))
        res = self.indexer.aindex.get(qstring[0:3])
        if res is None:
            return []
        collected = []
        pattern = re.compile("^" + qstring)
        for x in res:
            if pattern.match(x):
                collected.append(x)
                if (len(collected)) > 9:
                    break
        return collected


    def query(self, qstring):
        qstring = qstring.lower().translate(str.maketrans('','',string.punctuation))
        qlist = qstring.split()
        indexes = []
        for x in qlist:
            dt = self.indexer.index.get(x)
            if dt is None and len(x) > 3:
                nq = self.search_secondary(x)
                if len(nq) > 0:
                    indexes.append(self.indexer.index.get(nq[0][0]))
            if dt is not None:
                indexes.append(self.indexer.index.get(x, []))
        it = list(self.get_top_list(indexes))
        if (len(it) < 10):
            for i in range(len(qlist)):
                indexes = []
                for  j in range(len(qlist)):
                    if (i==j):
                        nq = self.search_secondary(qlist[j])
                        if (len(nq) > 0):
                            print ("searching {}".format(nq[0][0]))
                            indexes.append(self.indexer.index.get(nq[0][0]))
                    else:
                        indexes.append(self.indexer.index.get(qlist[j], []))
                it.extend(self.get_top_list(indexes))
                  
        return [self.indexer.imap[x] for x in it]

