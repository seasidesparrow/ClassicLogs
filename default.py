import os
import datetime

class DefaultClassicLog(object):

    def __init__(self,filename):
        self.filename = filename
        self.records = []
        self.ts = self.timestamp()


    def data(self):
        with open(self.filename) as fp:
            self.data = fp.read()


    def parse(self):
        for line in self.data.split('\n'):
            rec = {'error_msg': line, 'timestamp': self.ts}
            self.records.append(rec)

            
    def timestamp(self):
        self.ts = str(datetime.datetime.fromtimestamp(os.path.getmtime(self.filename)))
        return self.ts
