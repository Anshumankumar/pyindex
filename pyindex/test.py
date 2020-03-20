from pyindex.reader.list_reader import ListReader
from pyindex.reader.json_reader import JsonReader
from pyindex.processor.flat_mapper import FlatMapper
from pyindex.processor.preprocessor import PreProcessor
from pyindex.indexer.indexer import Indexer
from pyindex.query.query import QueryManager

import time

dir = "/home/anshuman/workspace/aashvi/ysaavn_songs"
reader  = ListReader(JsonReader, dir)
fm  = FlatMapper(reader)
pp =  PreProcessor(fm, {"str": ["title", "singers", "music", "category", "stars"], 
                        "int": ["year", "views"],
                        "id": "_id"}) 
indexer = Indexer(pp)
print("Opening")
indexer.open()
indexer.create_index()
qm = QueryManager(indexer)
while(True):
    print("Enter Text")
    q = input()
    t = time.time()
    print(qm.search_secondary(q))
    print(time.time() -t)
