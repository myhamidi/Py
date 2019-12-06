import Env as Envr
import tAgnt
import Render

Env = Envr.clsEnv("Grid",[10,10,-1])
Env.SetStart([0,4]); Env.SetState([0,7],terminal = 1, reward = 0)
Agt = tAgnt.clsAgent(Env.RetActions(),Env.RetEnvFeatures())
Rnd = Render.clsGrid(1,10,"")

Agt.ImportSeq("csv/test/testSeq.csv")
Agt.SortSequence()
Agt.RemoveDuplicateSteps()

Agt.SetParameter(["alpha","gamma"],[1,1])
Agt.TrainQ(30)
Agt.SortStates()
ret = Agt.ImportQ("csv/test/testQ.csv", CompareMode=True)
print (ret)


