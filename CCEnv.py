import Car


#Parameter
BrakeRatio = 1      # Ratio Braking/Gas -> Brake more than Accelerate in random actions
MaxTimeCycles = 100 # after 1 sec

class clsCCEnv:
    def __init__(self,StartSpeed, StartDistance,MaxSimLength,BrakeInc,StateReturnOnNextxvat,StateReturnOnDelta):
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
        self.m_max = MaxSimLength
        # self.Monitor = Car.CarsMonitor(self.Cars)
        # self.Monitor.setColor(0,"red")

    def setCar0_Accelerations(self,a):
        self.Cars[0].SetPlanA(a)

    def setCar1_Accelerations(self,a):
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
        
        #round values:
        x,v,a = self.Cars[1].Retxva()
        x = round(x)-0.49 # Set m values to lower bound of round
        v = round(v,1)
        self.Cars[0].time = round(self.Cars[0].time,1)
        self.Cars[1].time = round(self.Cars[1].time,1)
        self.Cars[1].Setxva(x, v, a)

        return self.Cars[1].Retxva()

    def LetRollUntilNextState(self,monitor):
        tx,tv,ta = self.Cars[1].Retxva()
        tt = self.Cars[1].time
        for _ in range(1,self.StateReturnAfterMaxTimeCycles):
            x,v,a = self.Cars[1].Retxva()
            t = self.Cars[1].time
            if self.StateReturnOnNextxvat == "x":
                if  abs(tx-x) < self.StateReturnOnDelta:
                    self.Cars[0].NextTimeCycle()
                    self.Cars[1].NextTimeCycle()
                else:
                    return
            if self.StateReturnOnNextxvat == "v":
                if  abs(tv-v) < self.StateReturnOnDelta:
                    self.Cars[0].NextTimeCycle()
                    self.Cars[1].NextTimeCycle()
                else:
                    return
            if self.StateReturnOnNextxvat == "a":
                if  abs(ta-a) < self.StateReturnOnDelta:
                    self.Cars[0].NextTimeCycle()
                    self.Cars[1].NextTimeCycle()    
                else:
                    return
            if self.StateReturnOnNextxvat == "t":
                if  abs(tt-t) < self.StateReturnOnDelta:
                    self.Cars[0].NextTimeCycle()
                    self.Cars[1].NextTimeCycle()
                else:
                    return

    def RetState(self): 
        Ret = ""
        x,v,a = self.Cars[1].Retxva()
        t = self.Cars[1].time
        if self.RetStateStyle[0] == True: Ret += str(round(x)) + " , "      #  12 m
        if self.RetStateStyle[1] == True: Ret += str(round(v,1))+ " , "       #  12,1 m/s
        if self.RetStateStyle[2] == True: Ret += str(round(2*a,0)/2)+ " , " #  -2,5m/s^2
        if self.RetStateStyle[3] == True: Ret += str(round(t,1))              #  2.1 s

        if self.pvRetDisance() <= 0:
            self.terminal = "Crash"
            Ret = "terminalCrash"
        _,v0,_ = self.Cars[0].Retxva() 
        if v0 == 0:
            self.terminal = "Safe"
            Ret = "terminalSafe"
        return Ret

    def RetStateFeatures(self):
        x,v,a = self.Cars[1].Retxva()
        t = self.Cars[1].time
        if self.RetStateStyle[0] == False: x=0
        if self.RetStateStyle[1] == False: v=0
        if self.RetStateStyle[2] == False: a=0
        if self.RetStateStyle[3] == False: t=0
        
        return [x,v,a,t]
    
    def ReturnReward(self):
        if self.terminal == "Crash":
            dv = self.Cars[0].v-self.Cars[1].v
            return -1*dv*dv*100
        if self.terminal == "Safe":
            return 10000
        return round(-1*self.Cars[1].a,1)
    
    def Reset(self):
        self.Cars[0].Setxva(0,self.StartV,0)
        self.Cars[1].Setxva(self.StartX,self.StartV,0)
        self.Cars[0].time = 0
        self.Cars[1].time = 0
        self.terminal = ""

    # def MonitorStart(self):
    #     self.Monitor.show(1000)

    # def MonitorUpdate(self):
    #     self.Monitor.update(self.Cars)
    #     self.Monitor.show(int(100*Car.pbTimeStep))
    #     # self.Monitor.show(int(tim*1000*Car.pbTimeStep))

    def pvRetDisance(self):
        x0,_,_ = self.Cars[0].Retxva()
        x1,_,_ = self.Cars[1].Retxva()
        return x1-x0

    def render(self,xva):
        info0 ="";info1 = ""
        String = self.RetState(); flag0 = True; flag1 = True
        x0,v0,a0 = self.Cars[0].Retxva()
        x1,v1,a1 = self.Cars[1].Retxva()
        if "x" in xva:
            info0 += "x:" + str(round(x0));info1 += "x:" + str(round(x1))
        if "v" in xva: 
            info0 += "v:" + str(round(v0));info1 +="v:" + str(round(v1))
        if "a" in xva:
            info0 += "a:" + str(round(a0,1));info1 +="a:" + str(round(a1,1))

        for i in range(150):    #1m = textsign
            if self.Cars[0].x < i and flag0:
                flag0 = False
                String += "0: " + info0
            if self.Cars[1].x < i and flag1:
                flag1 = False
                String += repr("1: ") + info1
            String += " "
        print(repr(String), end ='\r')
            
    def RetGridAsArray(self):
        arr = []
        arrRow = []
        flag1= True; flag2 = True
        for i in range(self.m_max):    #1m = textsign
            a = 0
            if self.Cars[0].x < i and flag1:flag1 = False;a = 1
            if self.Cars[1].x < i and flag2:flag2 = False;a = 2
            arrRow.append(a)
        arr.append(arrRow)
        return arr


