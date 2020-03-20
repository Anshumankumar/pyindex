import string
from collections import defaultdict
import time

class QueryManager():
    def __init__(self, indexer):
        self.indexer = indexer

    def search_secondary(self, x):
        t = time.time()
        x = x.lower().translate(str.maketrans('','',string.punctuation))
        qlist = []
        for i in range(0,len(x)):
            if (i < len(x)-3):
                nstr = x[i:i+3]
            else:
                nstr = x[i:len(x)] + "$" + x[0:i+3-len(x)]
            qlist.append(nstr)
        
        score_map = defaultdict(lambda :0)
        for q in qlist:
            res = self.indexer.sindex[q]
            for j in range(len(x)-1, 11):
                for k in  res[j]:
                    score_map[k] = score_map[k]+1

        print(time.time() -t) 
        print(len(score_map))

        slist = [(m, score/(len(x) + len(m) - score)) for m,score in score_map.items()]
        slist.sort(key=lambda x:x[1], reverse=True)
        print(time.time() -t) 
        return slist[:10]


    def intersect(self, l1, l2):
        i=0
        j=0
        fint = []
        while(i < len(l1) and j < len(l2)):
            if l1[i] == l2[j]:
                fint.append(l1[i])
                i = i+1
                j = j+1
            elif l1[i] < l2[j]:
                i = i+1
            else:
                j = j+1 
        return fint

    def query(self, qstring):
        qstring = qstring.lower().translate(str.maketrans('','',string.punctuation))
        qlist = qstring.split()
        indexes = []
        for x in qlist:
            print(x)
            indexes.append(self.indexer.index.get(x, []))
        it  = indexes[0]
        for x in indexes[1:]:
            it = self.intersect(it, x) 
        return it

