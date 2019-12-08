TEST_GRIDSTD = False
TEST_GRIDPOLICYINJECTION = True

import Env as Envr
import tAgnt
import Render

Env = Envr.clsEnv("Grid",[10,10,-1])
Agt = tAgnt.clsAgent(Env.RetActions(),Env.RetEnvFeatures())
Rnd = Render.clsGrid(10,10,"Policy Injection")

if TEST_GRIDSTD:
    Agt.ImportSeq("csv/test/testSeq.csv")
    Agt.SortSequence()
    Agt.RemoveDuplicateSteps()

    Agt.SetParameter(["alpha","gamma"],[1,1])
    Agt.TrainQ(30)
    Agt.SortStates()
    ret = Agt.ImportQ("csv/test/testQ.csv", CompareMode=True)
    print (ret)

if TEST_GRIDPOLICYINJECTION:
    Env = Envr.clsEnv("Grid",[10,10,-1])
    Agt = tAgnt.clsAgent(Env.RetActions(),Env.RetEnvFeatures())
    Agt.ImportQ("csv/test/testQInjection.csv")
    Agt.SetParameter(["epsilon"],[[0]])

    for i in range(20):
        Agt.PerceiveEnv(Env.RetState(),Env.RetReward(),rmbState=False)
        Env.Step(Agt.NextAction())
        print(Agt._retQ(Env.RetState()))
        Rnd.renderArray(Env.RetStateAsGrid(),"",200)
