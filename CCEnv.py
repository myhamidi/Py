import Car

class clsCCEnv:
    def __init__(self,StartSpeed, StartDistance,BrakeInc):
        self.StartV = StartSpeed/3.6
        self.StartX = StartDistance
        self.Crash = False
        self.Cars = [Car.typCar(0,self.StartV,0),Car.typCar(self.StartX,self.StartV,0)]
        #tkinter:
        self.SimDauer = 20
        self.Monitor = Car.CarsMonitor(self.Cars)
        self.Monitor.setColor(0,"red")
        self.Actions = ["brake","roll"]
        self.BrakeInc = BrakeInc

    def ReturnActionList(self):
        return self.Actions

    def Next(self,action):
        x,v,a = self.Cars[1].Retxva()
        if action == "brake":
           self.Cars[1].Setxva(x,v,a-self.BrakeInc)
        for j in range(len(self.Cars)):
            self.Cars[j].Next()

        return self.Cars[1].Retxva

    def MonitorStart(self):
        self.Monitor.show(1000)

    def MonitorUpdate(self):
        self.Monitor.update(self.Cars)
        self.Monitor.show(int(1000*Car.pbTimeStep))
    
    def RunSim(self):
        
        for _ in range(int(self.SimDauer/Car.pbTimeStep)):
            for j in range(len(self.Cars)):
                self.Cars[j].Next()
            if self.Cars[1].x < self.Cars[0].x and not self.Crash:
                self.Crash = True
                print("v0: ",round(self.Cars[0].v*3.6,1)," km/h. v1: ",round(self.Cars[1].v*3.6,1)," km/h. Delta v:",
                round((self.Cars[0].v-self.Cars[1].v)*3.6,1)," km/h.")
                break
            if  self.Cars[1].v == 0 and self.Cars[0].v == 0:
                print("x0: ",round(self.Cars[0].x,1)," m. x1: ",round(self.Cars[1].x,1)," m. Distance:",
                round(self.Cars[1].x-self.Cars[0].x,1)," m.")
                break



