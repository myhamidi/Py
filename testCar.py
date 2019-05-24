import myTracer
tr = myTracer.glTracer

import Car

testLane = Car.clsLane([(1,2,3),(0,0,0),(10,10,10)])
testCM = Car.CarMonitor([(1,2,3),(0,0,0),(10,10,10)])
testCM.show(1000)
dX = [0,0]
#each time step
testLane[1].PlanBrakings([0.2])
testLane[1].PlanAccelerations([0.5])
for time in range(500):
    #each Car
    for j in range(len(testLane.Cars)):
        #remember X (using dX)
        dX[j] = testLane[j].x
        #Action
        testLane[j].roll()
        #determine dX
        dX[j] = testLane[j].x -dX[j]
    testCM.update(dX)
    testCM.show(10)
