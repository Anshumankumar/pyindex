import os
from pyindex.reader.reader import Reader
from collections import deque

class ListReader(Reader):
    def __init__(self, reader_class, dir):
        self.reader_class = reader_class
        self.dir = dir

    def open(self):
        self.files = os.listdir(self.dir)
        self.queue  = deque([os.path.join(self.dir, x) for x in self.files])
        self._get_new_reader()
    
    def _get_new_reader(self):
        if self.queue:
            self.creader = self.reader_class(self.queue.popleft())
            self.creader.open()
        else:
            self.creader = None

    def get_next(self):
        if (self.creader == None):
            return None
        st = self.creader.get_next()
        if st != None:
            return st
        self._get_new_reader()
        return self.get_next()
