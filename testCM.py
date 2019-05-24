import myTracer
tr = myTracer.glTracer

import Car

testCM = Car.CarsMonitor([(100,2,3),(0,0,0),(50,10,10)])
testCM.show(3000)
dX = [100,20,30]
testCM.update(dX)
testCM.show(1000)
