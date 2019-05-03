#import Tracer
import myTracer
tr = myTracer.glTracer

#improt libs to be tested
import RL

#import libs to support testing
import random

#Test
def test_clsEnvironment_vizualize():
    rows = 5; cols = 10
    testGridviz = RL.clsEnvironment(rows,cols,-2)
    testGridviz.visualize_show(100)
    for i in range(2000):
        rndActions = ["up","down","left","right"]
        rndStep = random.choice(rndActions)
        testGridviz.move(rndStep)
        if i %50 == 0:
            testGridviz.visualize_update()
            testGridviz.visualize_show(10)
    return 0

test_clsEnvironment_vizualize()
#</Test>



#Result: print traced Fucntion Calls
for i in range(len(tr.getCalls())):
    print(tr.getCalls()[i])