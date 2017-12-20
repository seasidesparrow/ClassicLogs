import os

class MissingParser(Exception):
    pass


class MissingLogfileError(Exception):
    pass


class DefaultParser(object):
    def __init__(self):
        raise MissingParser("No parser defined")



#class ClassicLogGenericReader(object):


def read(fp):

    for l in fp.readlines():
        data = fp.read()
            
    return data
