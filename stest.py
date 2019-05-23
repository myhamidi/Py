#import Tracer
import myTracer
tr = myTracer.glTracer

#improt libs to be tested
import RL
import Agt

#Config Environment
rows = 4; cols = 4; reward = -1
#Config Agent
lactions =["up","down","left","right"]
epochs = 300; maxsteps = 1000

#Test Run
def test_clsEnvironment_vizualize():
    #Init Environment and Agent
    testEnv = RL.clsEnvironment(rows,cols,reward)
    testEnv.setTerminalStates([(0,0),(rows-1,cols-1)])
    testAgent = Agt.clsAgent(lactions)

    for _ in range(epochs):
        for i in range(maxsteps):
            if testAgent.StateIsTerminal():
                #Update Value Function:MC
                testAgent.Update_ValueFunctionMC()
                #Vizualize when Terminal state reached
                testEnv.visualize_update()
                testEnv.visualize_show(10)
                #Init Next Environnment and Agnet
                testEnv.InitRun((0,cols-1))
                testAgent.IntiSequences()
                break

            #Agent performs Action
            testEnv.move(testAgent.RetNextAction())
            #Agent perceives the Environment
            testAgent.PerceiveState(testEnv.RetCurrentEnvState(),testEnv.RetReward())

    #Print MC results
    f = open("Result-MC.txt","w")
    g = open("Result.txt","w")
    for i in range(len(testAgent.RewStates)):
        f.write(testAgent.RewStates[i].state + ": " + str(testAgent.RewStates[i].value) + "\n")

    #Get Value Function from TrMa
    testAgent.DoBellman(200)

    #Print Bellman results
    for i in range(len(testAgent.RewStates)):
        g.write(testAgent.RewStates[i].state + ": " + str(testAgent.RewStates[i].value) + "\n")
  
    f.close()
    g.close()  
    return 0
#</Test>

#Test Call
test_clsEnvironment_vizualize()
arr = tr.getCalls()
for i in range(len(arr)):
    print(arr[i])