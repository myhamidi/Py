import EnvGrid
import Agt as Ag
import Render

import tensorflow as tf
# from tf_agents.agents.dqn import dqn_agent

### Parameter:
GZx = 10
GZy = 10
runs = 500  # N training runs

### Init
Env = EnvGrid.clsEnvironment(GZx,GZy,-1)
Agt = Ag.clsAgent(Env.ReturnActionList(),featurelist=["x","y","terminal"])
Rnr = Render.clsGrid(GZx,GZy,"")

def AgtImport():
    Agt.ImportQ("csv/Q-EnvGrid.csv")

def RunAgtOnGrid():
    ### Config
    Env.SetTerminalState((0,0)); Env.SetRewardAtState((0,0),0)
    Env.SetTerminalState((GZx-1,GZy-1)); Env.SetRewardAtState((GZx-1,GZy-1),0)
    Env.SetStartPosition((int(GZx/2),int(GZy/2)))
    Agt.setLearningParameter(0.2,1)
    Agt.setModelTrainingParameter(batchsize=16)
    # Agt.SetActionConstrains(forbiddenActions=["right"])
    inn = len(Env.ReturnActionList()) + len(Env.ReturnFeatureList())-1
    Agt.modelInit(inn,1,act= 'tanh',NeuronshiddenLayer=32,TreeMaxDepth=1000)
    Agt.modelSetParameter(Agtlearning_rate=0.01)

    ### Train
    while Agt.Nterminal < runs:
        state = Env.RetStateFeatures()
        reward = Env.RetReward()
        Agt.perceiveState(state, Env.RetReward(), DQN=True,DQNTrainSteps=20)
        forbact = []
        if Agt.LastAction == "left" or state[1] == GZy-1:
            forbact.append("right")
        if Agt.LastAction == "right" or state[1] == 0:
            forbact.append("left")
        if Agt.LastAction == "up" or state[0] == GZx-1:
            forbact.append("down")
        if Agt.LastAction == "down" or state[0] == 0:
            forbact.append("up")
        # if not forbact == []:
        #     Agt.SetActionConstrains(forbiddenActions=forbact)
        Env.Next(Agt.nextAction(epsilon=1-Agt.Nterminal/runs))
        Agt.EchoPrint(1, "train ")
        print(Agt.loss, end= '\r')
        
        
    Agt.SortStates()
    Agt.QapxToStates()
    Agt.RoundQ(1)
    Agt.ExportWeights("csv/w.csv")

    # Export results
    Agt.ExportQtoCSV("csv/Q-EnvGrid.csv")
    # Agt.ExportQtoCSV("csv/QList-EnvGrid.csv", SplitCols=True)
    Agt.ExportSeqtoCSV("csv/Seq-EnvGrid.csv",SplitCols=True)

    ### Test
    TestAgt = Ag.clsAgent(Env.ReturnActionList())
    TestAgt.ImportQ("csv/Q-EnvGrid.csv")
    # for i in range(len(Agt.States)):
        # assert Agt.States[i].features == TestAgt.States[i].features, str(Agt.States[i].features) + " is not " + str(TestAgt.States[i].features)
        # assert Agt.States[i].Q == TestAgt.States[i].Q, str(Agt.States[i].Q) + " is not " + str(TestAgt.States[i].Q)
    
    tmpState = []; c = 0; runs_test = 10;imax = 20;i=0 #2*(GZ-1);
    Env.SetRandomStart()
    while c < runs_test and i < imax:
        TestAgt.perceiveState(Env.RetStateFeatures(), Env.RetReward(),learn = False)
        Rnr.renderArray(Env.RetGridAsArray(), Env.RetState(),50)
        assert Env.RetStateFeatures()  != tmpState ,"No State Change during Test. State is: " + str(tmpState) 
        i +=1
        tmpState = Env.RetState()
        if Env.IsCurrentStateTerminal():
            tmpState = []; c+=1;i=0
            # Env.Reset()
            Env.SetRandomStart()
        eps = 0
        Env.Next(TestAgt.nextAction(eps))

RunAgtOnGrid()