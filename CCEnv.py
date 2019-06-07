import Car


#Parameter
BrakeRatio = 2      # Ratio Braking/Gas -> Brake more than Accelerate in random actions
MaxTimeCycles = 100 # after 1 sec

class clsCCEnv:
    def __init__(self,StartSpeed, StartDistance,BrakeInc,StateReturnOnNextxvat,StateReturnOnDelta):
        self.StartV = StartSpeed/3.6
        self.StartX = StartDistance
        self.terminal = ""
        self.Cars = [Car.typCar(0,self.StartV,0),Car.typCar(self.StartX,self.StartV,0)]
        self.Actions = ["brake","releasebrake"]
        self.BrakeInc = BrakeInc
        self.StateReturnAfterMaxTimeCycles = MaxTimeCycles # after 1 sec
        self.StateReturnOnNextxvat = StateReturnOnNextxvat  #x OR v OR a OR t
        self.StateReturnOnDelta = StateReturnOnDelta
        self.RetStateStyle = [True,True,True,True] #x,v,a,t
        #tkinter:
        self.SimDauer = 10
        self.Monitor = Car.CarsMonitor(self.Cars)
        self.Monitor.setColor(0,"red")

    def setConstraint0(self,a):
        self.Cars[0].SetPlanA(a)

    def setConstraint1(self,a):
        self.Cars[1].SetPlanA(a)

    def InitRetStateStyle(self,StateStyle):
        self.RetStateStyle[0],self.RetStateStyle[1],self.RetStateStyle[2],self.RetStateStyle[3] = StateStyle
    
    def ReturnActionList(self):
        return self.Actions

    def Next(self,action,monitor):
        x,v,a = self.Cars[1].Retxva()
        if action == "brake" and v>0:
           self.Cars[1].Setxva(x, v, a - BrakeRatio * self.BrakeInc)
        if action == "releasebrake" and a < 0:
           self.Cars[1].Setxva(x ,v ,min(a + self.BrakeInc, 0))
        if action == "gas":
           self.Cars[1].Setxva(x, v, a + self.BrakeInc)
        
        self.LetRollUntilNextState(monitor)

        return self.Cars[1].Retxva()

    def LetRollUntilNextState(self,monitor):
        tx,tv,ta = self.Cars[1].Retxva()
        tt = self.Cars[1].time
        for _ in range(1,self.StateReturnAfterMaxTimeCycles):
            if monitor == "monitor": self.MonitorUpdate()
            x,v,a = self.Cars[1].Retxva()
            t = self.Cars[1].time
            if self.StateReturnOnNextxvat == "x":
                if  abs(tx-x) < self.StateReturnOnDelta:
                    self.Cars[0].NextTimeCycle()
                    self.Cars[1].NextTimeCycle()
            if self.StateReturnOnNextxvat == "v":
                if  abs(tv-v) < self.StateReturnOnDelta:
                    self.Cars[0].NextTimeCycle()
                    self.Cars[1].NextTimeCycle()
            if self.StateReturnOnNextxvat == "a":
                if  abs(ta-a) < self.StateReturnOnDelta:
                    self.Cars[0].NextTimeCycle()
                    self.Cars[1].NextTimeCycle()
            if self.StateReturnOnNextxvat == "t":
                if  tt-t < self.StateReturnOnDelta:
                    self.Cars[0].NextTimeCycle()
                    self.Cars[1].NextTimeCycle()
        

    def RetState(self): 
        if self.pvRetDisance() <= 0:
            self.terminal = "Crash"
            return "terminalCrash"
        _,v0,_ = self.Cars[0].Retxva() 
        if v0 == 0:
            self.terminal = "Safe"
            return "terminalSafe"
        x,v,a = self.Cars[1].Retxva()
        t = self.Cars[1].time
        Ret = ""
        if self.RetStateStyle[0] == True: Ret += str(round(x)) + " , "
        if self.RetStateStyle[1] == True: Ret += str(round(v))+ " , "
        if self.RetStateStyle[2] == True: Ret += str(round(2*a,0)/2)+ " , "
        if self.RetStateStyle[3] == True: Ret += str(round(t))
        return Ret
    
    def ReturnReward(self):
        if self.terminal == "Crash":
            return -50*(self.Cars[0].v-self.Cars[1].v)-1000
        if self.terminal == "Safe":
            return 1000
        return round(-1*self.Cars[1].a,1)/10
    
    def Reset(self):
        self.Cars[0].Setxva(0,self.StartV,0)
        self.Cars[1].Setxva(self.StartX,self.StartV,0)
        self.Cars[0].time = 0
        self.Cars[1].time = 0
        self.terminal = ""

    def MonitorStart(self):
        self.Monitor.show(1000)

    def MonitorUpdate(self):
        self.Monitor.update(self.Cars)
        self.Monitor.show(int(100*Car.pbTimeStep))
        # self.Monitor.show(int(tim*1000*Car.pbTimeStep))

    def pvRetDisance(self):
        x0,_,_ = self.Cars[0].Retxva()
        x1,_,_ = self.Cars[1].Retxva()
        return x1-x0




