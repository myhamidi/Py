#import Tracer
import myTracer
tr = myTracer.glTracer

#improt libs to be tested
import RL
import Agt

#Config
rows = 4; cols = 4; reward = -1

#Test
def test_clsEnvironment_vizualize():
    #Init Environment and Agent
    testEnv = RL.clsEnvironment(rows,cols,reward)
    testEnv.setTerminalStates([(0,0),(rows-1,cols-1)])
    testAgent = Agt.clsAgent(["up","down","left","right"])
    for k in range(30):
        for i in range(1000):

            if testAgent.StateIsTerminal():
                #Vizualize when Terminal state reached
                testEnv.visualize_update()
                testEnv.visualize_show(10)
                #Init Envirinment and Agnet
                testEnv.InitRun((0,cols-1))
                testAgent.IntiSequences()
                break

            #Agent performs Action
            testEnv.move(testAgent.RetNextAction())

            #Agent perceives the Environment
            testAgent.PerceiveState(testEnv.RetCurrentEnvState(),testEnv.RetReward())

    testAgent.DoBellman(200)
    f = open("Result.txt","w")
    for i in range(len(testAgent.RewStates)):
        f.write(testAgent.RewStates[i].state + ": " + str(testAgent.RewStates[i].value) + "\n")
    return 0
#</Test>

#Test Call
test_clsEnvironment_vizualize()
arr = tr.getCalls()
for i in range(len(arr)):
    print(arr[i])