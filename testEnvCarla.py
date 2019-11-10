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
Agt = Agt.clsAgent(Env.ReturnActionList(),Env.ReturnFeatureList())

### Config
Agt.setLearningParameter(0.2,1)
Agt.setModelTrainingParameter(batchsize=16)
inn = len(Env.ReturnActionList()) + len(Env.ReturnFeatureList())-1
Agt.modelInit(inn,2, act= 'relu',NeuronshiddenLayer=64)
Env.ImportWPS("csv/Carla-WPs-5.csv", IsRoute=True)
Env.wp_dis =5
Env.SetStartPosition(STIDX,SPEED,spectator=True)
# Env.SetVehiclesAhead(1,4)
# Env.SetActorsToAutopilot(speed=10)

runs = 800
for i in range(runs):
    lr = 0.01
    Agt.modelSetParameter(Agtlearning_rate=lr,FitAfterNStatePerceptions=10)
    state = Env.RetStateFeatures(runden=0)
    # print(state)okay
    reward = Env.RetReward(runden=0)
    Agt.perceiveState(state,reward, DQN=True, tabular=True)
    if state[-1] == 1 or Env.RetActorSpeed(0)>30:
        # assert Env.terminalPerceived==True, "Error! Terminal state not perceived!"
        Env.RemoveActors()   
        Env.SetStartPosition(STIDX,SPEED,spectator=False)
        # Env.SetVehiclesAhead(1,4)
        # Env.SetActorsToAutopilot(speed=10)
    if i < runs-100:
        Env.Next(Agt.nextAction(epsilon=1-i/runs), timestep = 0.05)
    else:
        Env.Next(Agt.nextAction(epsilon=0), timestep = 0.05)
    print("step "+str(i)+". Speed: " + str(state) + ". Reward: "+str(Agt.Sequence[-1].reward) + \
        ". Total Reward: "+str(Agt.Sequence[-1].totalreward),end ='\r')

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