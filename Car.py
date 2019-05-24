import myTracer;tr = myTracer.glTracer

import tkinter as tk
pbTimeStep = 0.1
pbStep = 1         #Braking / acceleration increment per time step
pbMaxBrake = -10


class CarsMonitor:
    def __init__(self,Cars):
        self.master = tk.Tk()
        self.w = tk.Canvas(self.master, width=500, height=200)
        self.w.pack()
        x = [i for i,j,k in Cars]
        self.element = [self.w.create_rectangle(i, 90, i+10, 100 , fill="black") for i in x]

    def __getitem__(self,n):
        return self.element[n]

    def show(self,ms):
        self.master.after(ms, self.w.quit)
        tk.mainloop()
    
    def update(self,dX):
        for i in range(len(dX)):
            self.w.move(self.element[i],dX[i],0)

class typCar:
    def __init__(self,x,v,a):
        #Attributes:
        self.time = 0
        self.x = x
        self.v = v
        self.a = a
        self.Brakings= []
        self.Accelerations= []
    
    def SetBrakings(self,ListBrakings):
        self.Brakings= ListBrakings
    
    def SetAccelerations(self,ListAccelerations):
        self.Accelerations= ListAccelerations

    def Next(self):
        self.time = self.time + pbTimeStep
        if self.time in self.Brakings:
            self.pvbrake()
        if self.time in self.Accelerations:
            self.pvgas()
        
        self.x = round(self.pvfx(),2)
        self.v = round(self.pvfv(),2)
    
    def RetCar(self):
        return (self.time, self.x, self.v)

    def pvbrake(self):
        if self.a >= pbMaxBrake:
            self.a = self.a-pbStep

    def pvgas(self):
        self.a = self.a+pbStep
    
    def pvfx(self):
        return 0.5*self.a*pbTimeStep*pbTimeStep+self.v*pbTimeStep+self.x

    def pvfv(self):
        return self.a*pbTimeStep + self.v
