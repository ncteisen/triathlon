from tri.time import Time

# Data structure to hold information about an althlete
class Athlete:
    def __init__(self):
        self.data = {}

    def addData(self, key, value):
        self.data[key] = value

    def getTotal(self, aspects):
       return sum([self.data[a] for a in aspects], Time(0,0,0))

    def __repr__(self):
        return "Athlete(%s)" % str(self.data)