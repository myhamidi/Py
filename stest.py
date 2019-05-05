#import Tracer
import myTracer
tr = myTracer.glTracer

#improt libs to be tested
import RL
import Agt

#Config
rows = 5; cols = 10; reward = -1

#Test
def test_clsEnvironment_vizualize():
    #Init Environment and Agent
    testEnv = RL.clsEnvironment(rows,cols,reward)
    testAgent = Agt.clsAgent(["up","down","left","right"])
    for i in range(2000):
        #Agent performs Action
        testEnv.move(testAgent.RetNextAction())

        #Agent perceives the Environment
        testAgent.PerceiveState(str(testEnv.currentposition),testEnv.RetReward())

        #Update Visualization after 50 steps
        if i %50 == 0:
            testEnv.visualize_update()
            testEnv.visualize_show(10)

    return 0
#</Test>

#Test Call
test_clsEnvironment_vizualize()
arr = tr.getCalls()
for i in range(len(arr)):
    print(arr[i])