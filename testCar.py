import myTracer
tr = myTracer.glTracer

import Car

StartV = 100/3.6
StartDistance = StartV*3.6/3    # Third of Ego Speed 

testCars = [Car.typCar(0,StartV,0),Car.typCar(StartDistance,StartV,0)]
testCM = Car.CarsMonitor(testCars)
testCM.setColor(0,"red")

testCars[0].SetA([(0.1,1)])
testCars[1].SetA([(0.1,-1)])

testCM.show(1000)
crash = False
for i in range(70):
    for j in range(len(testCars)):
        testCars[j].Next()
    if getattr(testCars[1],"x") < getattr(testCars[0],"x") and not crash:
        crash = True
        print("v0: ",round(testCars[0].v*3.6,1)," km/h. v1: ",round(testCars[1].v*3.6,1)," km/h. Delta v:",
        round((testCars[0].v-testCars[1].v)*3.6,1)," km/h.")
        break
    testCM.update(testCars)
    testCM.show(100)
