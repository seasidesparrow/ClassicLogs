class MissingParser(Exception):
    pass



class DefaultParser(object):
    def __init__(self):
        raise MissingParser("No parser defined")



class ClassicLogGenericParser(object):
