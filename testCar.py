import myTracer
tr = myTracer.glTracer

import Car

testCars = [Car.typCar(0,20,0),Car.typCar(100,20,0)]
CarsXVA = [testCars[i].Retxva() for i in range(len(testCars))]
testCM = Car.CarsMonitor(CarsXVA)


testCars[1].SetA([(0.5,-4)])

testCM.show(1000)
for i in range(100):
    for j in range(len(testCars)):
        testCars[j].Next()
    CarsXVA = [testCars[i].Retxva() for i in range(len(testCars))]
    testCM.update(CarsXVA)
    testCM.show(100)
