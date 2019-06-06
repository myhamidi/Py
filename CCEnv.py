import Car

class clsCCEnv:
    def __init__(self,StartSpeed, StartDistance,BrakeInc):
        self.StartV = StartSpeed/3.6
        self.StartX = StartDistance
        self.Crash = False
        self.Cars = [Car.typCar(0,self.StartV,0),Car.typCar(self.StartX,self.StartV,0)]
        self.Actions = ["brake","releasebrake"]
        self.BrakeInc = BrakeInc
        #tkinter:
        self.SimDauer = 10
        self.Monitor = Car.CarsMonitor(self.Cars)
        self.Monitor.setColor(0,"red")


    def setConstraint(self,a):
        self.Cars[0].SetPlanA(a)
    
    def ReturnActionList(self):
        return self.Actions

    def Next(self,action):
        x,v,a = self.Cars[1].Retxva()
        if action == "brake" and self.Cars[1].v>0:
           self.Cars[1].Setxva(x,v,a-5*self.BrakeInc)
        if action == "releasebrake" and a<0:
           self.Cars[1].Setxva(x,v,min(a+self.BrakeInc,0))
        if action == "gas":
           self.Cars[1].Setxva(x,v,a+self.BrakeInc)
        self.LetRollUntilDeltaV(1,100)

        return self.Cars[1].Retxva()

    def LetRollUntilDeltaV(self,DeltaV,maxRoll):
        _,tmpv,_ = self.Cars[1].Retxva()
        _,v,_ = self.Cars[1].Retxva()
        for _ in range(1,maxRoll):
            if abs(tmpv-v) < DeltaV:
                for j in range(len(self.Cars)):
                    self.Cars[j].Next()
                _,v,_ = self.Cars[1].Retxva()

    def RetState(self):
        _,v,a = self.Cars[1].Retxva()
        if self.pvRetDisance() <=0:
            return str(round(v,0)) + ","+ str(round(2*a,0)/2)+"terminal0"
        _,v0,_ = self.Cars[0].Retxva() 
        if v0 == 0:
            return str(round(v,0)) + ","+ str(round(2*a,0)/2)+"terminal1"
        return str(round(v,0)) + ","+ str(round(2*a,0)/2)
    
    def ReturnReward(self):
        if self.pvRetDisance() <=0:
            return -50*(self.Cars[0].v-self.Cars[1].v)
        return round(-self.Cars[1].a,1)/10
    
    def Reset(self):
        self.Cars[0].Setxva(0,self.StartV,0)
        self.Cars[1].Setxva(self.StartX,self.StartV,0)

    def MonitorStart(self):
        self.Monitor.show(1000)

    def MonitorUpdate(self):
        self.Monitor.update(self.Cars)
        self.Monitor.show(int(1000*Car.pbTimeStep))

    #private:
    # def pvIsTerminal(self):
    #     if self.pvRetDisance() <=0:
    #         return "terminal"
    #     # _,State,_ = self.Cars[1].Retxva()
    #     # if State == 0:
    #     #     return True
    #     return 

    def pvRetDisance(self):
        x0,_,_ = self.Cars[0].Retxva()
        x1,_,_ = self.Cars[1].Retxva()
        return round(x1-x0,1)




