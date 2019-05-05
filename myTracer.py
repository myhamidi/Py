TRACER = True

class clsTracer():
    def __init__(self):
        self.arr = []

    def calling(self,callName):
        if not callName in self.arr:
            self.arr.append(callName)

    def getCalls(self):
        self.arr.sort()
        return self.arr
    
    def call(self,callName):
        if TRACER:
            if not callName in self.arr:
                self.arr.append(callName)

glTracer = clsTracer()