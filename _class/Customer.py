from ModelHelper import *
from Address import *

class Customer(ModelHelper):
    def __init__(self):
        self.id = 0
        self.name = 0
        self.branch = ''
        self.rfc = ''
        #self.address = Address()