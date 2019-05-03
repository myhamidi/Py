TRACER = True

class clsTracer():
    def __init__(self):
        self.arr = []

    def calling(self,callName):
        if not callName in self.arr:
            self.arr.append(callName)

    def getCalls(self):
        return self.arr

glTracer = clsTracer()