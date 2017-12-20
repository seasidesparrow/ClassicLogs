import os
import json
import datetime

class GenericClassicLog(object):

    def __init__(self,filename):
        self.filename = filename
        self.records = []
        self.ts = self.timestamp()

    def data(self):
        with open(self.filename) as fp:
            self.data = fp.read()
#       return 

    def parse(self):
        for line in self.data.split('\n'):
            rec = {'error_msg': line, 'timestamp': self.ts}
            self.records.append(rec)
#       return
            
    def timestamp(self):
        self.ts = str(datetime.datetime.fromtimestamp(os.path.getmtime(self.filename)))
        return self.ts




fn = '/Users/mtempleton/notes.txt'

foo = GenericClassicLog(fn)

foo.data()

foo.parse()

print foo.records

#print json.dumps(foo.records, sort_keys = True, indent = 4)
