import EnvCarla
import Agt
import Render
import time
import carla

#Parameter
SPEED = 12
STIDX = 2
ROUTE = ""

### Init
Env = EnvCarla.clsCarlaEnv(nWorld = 4, smode=False, rmode=False)
Agt = Agt.clsAgent(Env.ReturnActionList(),featurelist=["x","y","terminal"])

### Config
Agt.setLearningParameter(0.2,1)
Agt.setModelTrainingParameter(batchsize=16)
Agt.modelInit(4,2,act= 'relu')
Env.ImportWPS("csv/Carla-WPs-5.csv", IsRoute=True)
Env.wp_dis =5
Env.SetStartPosition(STIDX,SPEED,spectator=True)
Env.SetVehiclesAhead(1,4)
Env.SetActorsToAutopilot(speed=10)

runs = 5000
for i in range(runs):
    state = Env.RetStateFeatures()
    Agt.perceiveState(state, Env.RetReward(), DQN=True)
    if state[-1] == 1:
        assert Env.terminalPerceived==True, "Error! Terminal state not perceived!"
        Env.RemoveActors()   
        Env.SetStartPosition(STIDX,SPEED,spectator=False)
        Env.SetVehiclesAhead(1,4)
        Env.SetActorsToAutopilot(speed=10)
    if i < runs-100:
        Env.Next(Agt.nextAction(epsilon=1-i/runs), timestep = 0.05)
    else:
        Env.Next(Agt.nextAction(epsilon=0), timestep = 0.05)
    print("step "+str(i)+". Reward: "+str(Agt.Sequence[-1].totalreward),end ='\r')

### Destroy actors
Env.RemoveActors()

### Env Log
Env.ExportDrivenWPSIdxtoCSV("csv/EnvCarlav-DrivenWPIdx.csv")

### Agt Log
Agt.ExportSeqtoCSV("csv/Seq-EnvCarlav2.csv",SplitCols=True, nthEpoch=1000)
Agt.SortStates()
Agt.QapxToStates()
Agt.RoundQ(1)
Agt.ExportQtoCSV("csv/Q-EnvCarlav2.csv")