#import Tracer
import myTracer
tr = myTracer.glTracer

#improt libs to be tested
import RL
import Agt

#import libs to support testing
import random

#Test
def test_clsEnvironment_vizualize():
    rows = 5; cols = 10
    testGrid = RL.clsEnvironment(rows,cols,-2)
    testGrid.visualize_show(100)
    testAgent = Agt.clsAgent()
    for i in range(2000):
        #Randomize Step
        rndActions = ["up","down","left","right"]
        rndStep = random.choice(rndActions)
        #Walk in Env
        testGrid.move(rndStep)
        #Interpretation for Agent
        testRewState = Agt.typRewState(str(testGrid.currentposition),-1,0,0)
        testAgent.PerceiveState(testRewState)
        #Update after 50 steps
        if i %50 == 0:
            testGrid.visualize_update()
            testGrid.visualize_show(10)
    return 0

test_clsEnvironment_vizualize()
#</Test>



#Result: print traced Fucntion Calls
arr = tr.getCalls()
for i in range(len(arr)):
    print(arr[i])