import myTracer;tr = myTracer.glTracer

import tkinter as tk

#Parameter
pbTimeStep = 0.01
pbStep = 1         #Braking / acceleration increment per time step
pbMaxBrake = -10


class CarsMonitor:
    def __init__(self,Cars):
        self.master = tk.Tk()
        self.w = tk.Canvas(self.master, width=1800, height=200)
        self.w.pack()
        self.x = [getattr(Cars[i],"x") for i in range(len(Cars))]
        self.element = [self.w.create_rectangle(i*10, 90, i*10+10, 100 , fill="black") for i in self.x]

    def __getitem__(self,n):
        return self.element[n]

    def show(self,ms):
        self.master.after(ms, self.w.quit)
        tk.mainloop()
    
    def update(self,Cars):
        newX = [getattr(Cars[i],"x") for i in range(len(Cars))]
        dX = [newX[i]-self.x[i] for i in range(len(Cars))]
        self.x = newX
        for i in range(len(Cars)):
            self.w.move(self.element[i],dX[i]*10,0)
    
    def setColor(self,n,color):
        self.w.itemconfig(self.element[n],fill=color)

class typCar:
    def __init__(self,x,v,a):
        #Attributes:
        self.time = 0
        self.x = x
        self.v = v
        self.a = a
        self.PlanBrakes= []     #[1,4,20]   #time step when brake inc shall occur
        self.PlanGas= []        #[1,4,20]   #time step when gas inc shall occur
        self.PlanA = []         #[(1,4),(4,-3),(20,0)]   #time step when a shall be set
    
    def Retxva(self):
        return self.x, self.v,self.a
    
    def Setxva(self,x,v,a):
        self.x = x
        self.v = v
        self.a = a
    
    def SetPlanA(self,ListA):
         self.PlanA = ListA
    
    def SetBrakings(self,ListBrakings):
        self.PlanBrakes= ListBrakings
    
    def SetAccelerations(self,ListAccelerations):
        self.PlanGas= ListAccelerations

    def NextTimeCycle(self):
        self.time = round(self.time + pbTimeStep,2)
        self.pcCheckPlanBrakes()
        self.pcCheckPlanGas()
        self.pvCheckPlanSetA()
        self.x = self.pvfx()
        self.v = self.pvfv()
        self.a = self.pvfa()

#private:
    def pcCheckPlanBrakes(self):
        if self.time in self.PlanBrakes:
            self.pvbrake()
    
    def pcCheckPlanGas(self):
        if self.time in self.PlanGas:
            self.pvgas()

    def pvCheckPlanSetA(self):
        t = [i for i,j in self.PlanA]
        a = [j for i,j in self.PlanA]
        for i in range(len(t)):
            if self.time == t[i]:
                self.a = a[i]

    def pvbrake(self):
        if self.a >= pbMaxBrake and self.v>0:
            self.a = self.a-pbStep

    def pvgas(self):
        self.a = self.a+pbStep

    def pvfa(self):
        if self.v >1:
            return self.a
        return 0
    
    def pvfx(self):
        if self.v>1:
            return 0.5*self.a*pbTimeStep*pbTimeStep+self.v*pbTimeStep+self.x
        return self.x

    def pvfv(self):
        if self.v>1:
            return max(self.a*pbTimeStep + self.v,0)
        return 0
