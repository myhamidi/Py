import myTracer;tr = myTracer.glTracer

import tkinter as tk
pbTimeStep = 0.1
pbStep = 1         #Braking / acceleration increment per time step
pbMaxBrake = -10


class CarsMonitor:
    def __init__(self,Cars):
        self.master = tk.Tk()
        self.w = tk.Canvas(self.master, width=1000, height=200)
        self.w.pack()
        self.x = [i for i,j,k in Cars] #current x position of Cars
        self.element = [self.w.create_rectangle(i, 90, i+10, 100 , fill="black") for i in self.x]

    def __getitem__(self,n):
        return self.element[n]

    def show(self,ms):
        self.master.after(ms, self.w.quit)
        tk.mainloop()
    
    def update(self,Cars):
        newX = [i for i,j,k in Cars]
        dX = [newX[i]-self.x[i] for i in range(len(Cars))]
        for i in range(len(Cars)):
            self.w.move(self.element[i],dX[i],0)

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
    
    def SetA(self,ListA):
         self.PlanA = ListA
    
    def SetBrakings(self,ListBrakings):
        self.PlanBrakes= ListBrakings
    
    def SetAccelerations(self,ListAccelerations):
        self.PlanGas= ListAccelerations

    def Next(self):
        self.time = round(self.time + pbTimeStep,2)
        self.pcCheckPlanBrakes()
        self.pcCheckPlanGas()
        self.pvCheckPlanA()
        self.x = round(self.pvfx(),2)
        self.v = round(self.pvfv(),2)

#private:
    def pcCheckPlanBrakes(self):
        if self.time in self.PlanBrakes:
            self.pvbrake()
    
    def pcCheckPlanGas(self):
        if self.time in self.PlanGas:
            self.pvgas()

    def pvCheckPlanA(self):
        t = [i for i,j in self.PlanA]
        a = [j for i,j in self.PlanA]
        for i in range(len(t)):
            if self.time == t[i]:
                self.a = a[i]

    def pvbrake(self):
        if self.a >= pbMaxBrake:
            self.a = self.a-pbStep

    def pvgas(self):
        self.a = self.a+pbStep
    
    def pvfx(self):
        return 0.5*self.a*pbTimeStep*pbTimeStep+self.v*pbTimeStep+self.x

    def pvfv(self):
        return self.a*pbTimeStep + self.v
