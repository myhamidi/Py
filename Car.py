import myTracer;tr = myTracer.glTracer
time_step = 0.1
v_step = 1

class typCar:
    def __init__(self,timeStep,vStep):
        #Parameters:
        self.timeStep = timeStep
        self.vStep = vStep
        #Attributes:
        self.time = 0
        self.x = 0
        self.v = 0
        #self.a = 0
    
    def brake(self):
        if self.v >=self.vStep:
            self.v = self.v-self.vStep
        self.pvNextTimeStep()

    def gas(self):
        self.v = self.v+self.vStep
        self.pvNextTimeStep()

    def roll(self):
        self.pvNextTimeStep()

    def pvNextTimeStep(self):
        self.time = self.time + self.timeStep
        self.x = round(self.x+self.v*time_step,2)
    
    def RetCar(self):
        return (self.time, self.x, self.v)
