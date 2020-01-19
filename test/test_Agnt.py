import sys
sys.path.append("C:\\temp Daten\\Lernbereich\\Git\\myhamidi\\Py")
import Agnt
import EnvGrid
import Render

Agt = Agnt.clsAgent(["jump", "run"],["world","level","terminal"])
# ==============================================================================
# -- Tests ---------------------------------------------------------------------
# ============================================================================== 
# -- Init ---------------------------------------------------------------------
def test_init(): 
    Agt_init = Agnt.clsAgent(["jump", "run"],["world","level","terminal"])
    assert Agt_init.actions == ["jump", "run"]
    assert Agt_init.features == ["world","level","terminal"]
    assert Agt_init.epsilon == [1.0]

# # -- Set Parameter ---------------------------------------------------------------
def test_SetParameter():
    Agt.SetParameter(["alpha","gamma", "epsilon"],[0.8,0.99,[0.5]])
    assert Agt.alpha == 0.8
    assert Agt.gamma == 0.99
    assert Agt.epsilon == [0.5]

    Agt.SetParameter(["epsilon"],[[0.2, 0.3, 0.7]])
    assert Agt.epsilon == [0.2, 0.3, 0.7]

    Agt.SetParameter(parameter=["Mode"], value=["Offline"])
    assert Agt.Mode == "Offline"
    Agt.SetParameter(parameter=["Mode"], value=["Online"])
    assert Agt.Mode == "Online"

    Agt.SetParameter(["buffer"], [2000])
    assert Agt.buffer == 2000

def test_Perception1():
    Agt.PerceiveEnv([2,"hi",0.1,0],-2)
    assert Agt.Sequence.len == 1
    assert Agt.Sequence[0].state0 == [2,"hi",0.1,0]

    Agt.PerceiveEnv([2,0],-1)
    Agt.PerceiveEnv([1,0],-1)
    assert Agt.Sequence[-2].state1 == [1,0]
    assert Agt.Sequence[-1].state0 == [1,0]
 


# # -- Perception ---------------------------------------------------------------------
def test_Perception2():
    Agt.Reset()
    Agt.PerceiveEnv([1,0],-2)
    Agt.PerceiveEnv([2,0],-3)
    Agt.PerceiveEnv([3,0],-4)
    Agt.PerceiveEnv([4,1],-7)
    assert Agt.Sequence[-3].reward == -2
    assert Agt.Sequence[-3].totalreward == -2
    assert Agt.Sequence[-2].reward == -3
    assert Agt.Sequence[-2].totalreward == -5
    assert Agt.Sequence[-1].reward == -4
    assert Agt.Sequence[-1].totalreward == -7


# # # -- Reset ---------------------------------------------------------------------
def test_Reset():
    Agt.PerceiveEnv([1,0],-2)
    Agt.PerceiveEnv([2,1],-2)
    Agt.Reset()
    assert Agt.States.len == 0
    assert Agt.Sequence.len == 0
    assert Agt.Sequence.Nterminal == 0
    assert Agt.Sequence[0] == None
    assert Agt.States[0] == None

    Agt.SetParameter(["alpha","gamma", "epsilon"],[0.8,0.99,[0.5]])
    Agt.SetParameter(["buffer", "batch", "Mode"], [2000,300, "Online"])
    Agt.Reset(True)
    assert Agt.alpha == 0.1
    assert Agt.gamma == 1.0
    assert Agt.epsilon == [1.0]
    assert Agt.buffer == 10**5
    assert Agt.batch == 10**5
    assert Agt.Mode == "Online"

def test_Mode():
    # # |In Online Mode (default), the Agent shall store new perceived states in its States Table and Sequence
    Agt.Reset()
    Agt.SetParameter(parameter=["Mode"],value=["Online"])
    for i in range(100):
        Agt.PerceiveEnv([i%10,100-i%10,0],-1)
    assert Agt.States.len == 10
    assert Agt.Sequence.len == 100

    # |In Silent Mode, the Agent shall not store any new perceived states in its States Table and Sequence
    Agt.Reset()
    Agt.SetParameter(parameter=["Mode"],value=["Silent"])
    for i in range(100):
        Agt.PerceiveEnv([i%10,100-i%10,0],-1)
    assert Agt.States.len == 0
    assert Agt.Sequence.len == 1,Agt.Sequence.len
    Agt.Reset(True)

# # Test Anchor States
def test_AnchorSates():
    Agt.PerceiveEnv(["A",0],-1)
    Agt.PerceiveEnv(["B",0],-1)
    Agt.PerceiveEnv(["C",1],-2)
    Agt.PerceiveEnv(["D",0],-1)
    Agt.PerceiveEnv(["E",0],-1)
    Agt.PerceiveEnv(["F",1],-3)
    Agt.PerceiveEnv(["G",0],-1)
    assert Agt.Sequence.Nterminal == 2
    assert Agt.StatesAnchor[0].features == ["C",1]
    assert Agt.StatesAnchor[1].features == ["F",1]


# # # -- Action ---------------------------------------------------------------------

def test_ActionDemand():
    Agt.PerceiveEnv([1,0],-1)
    Agt.NextAction("jump")
    assert Agt.Sequence[-1].action == "jump"
    assert Agt.Sequence[-1].actionInt == 0
    Agt.PerceiveEnv([3,0],-1)
    Agt.NextAction("run")
    assert Agt.Sequence[-1].action == "run"
    assert Agt.Sequence[-1].actionInt == 1

def test_ActionEpsilon():
    # epsilon == 1 -> radom action -> ~50% jump and ~50%run
    Agt.PerceiveEnv([0,0],0)
    Agt.SetParameter(["epsilon"],[[1]])
    jump = 0;run = 0
    for i in range(1000):
        action = Agt.NextAction()
        if action == "jump": jump +=1
        if action == "run": run +=1
    assert 450 < jump and jump < 550 and 450 < run and run < 550, jump
    assert Agt.Sequence[-1].action == "run" or Agt.Sequence[-1].action == "jump"

    Agt.SetParameter(["epsilon"],[[1, 0.3, 0.7]])
    jump = 0;run = 0
    for i in range(1000):
        action = Agt.NextAction()
        if action == "jump": jump +=1
        if action == "run": run +=1
    assert 250 < jump and jump < 350 and 650 < run and run < 750, jump
    assert Agt.Sequence[-1].action == "run" or Agt.Sequence[-1].action == "jump"
    Agt.Reset()


AgtGrid = Agnt.clsAgent(["up", "down","left","right"],["x","y","terminal"])
AgtGrid.States.Import("csv/test/testQ.csv")
AgtGrid2 = Agnt.clsAgent(["up", "down","left","right"],["x","y","terminal"])

def test_ActionGreedy():
    AgtGreedy = Agnt.clsAgent(["up", "down","left","right"],["x","y","terminal"])
    AgtGreedy.States.Import("csv/test/testQ.csv")
    AgtGreedy.SetParameter(["epsilon"],[[0]])
    AgtGreedy.SetParameter(["Mode"],["Silent"])
    for i in range(10):
        for j in range(10):
            AgtGreedy.PerceiveEnv([i,j,0],-1)
            if not (i == 9 and j == 9):
                nextAction = AgtGreedy.NextAction()
                # assert (nextAction == "down" or nextAction == "right"), str(i) + str(j)
    AgtGreedy.PerceiveEnv([9,9,1],-1)
    assert AgtGreedy.NextAction() == None
    AgtGreedy.PerceiveEnv([1.5,9,0],-1)
    assert AgtGreedy.NextAction() == None

def test_ReturnQ():
    assert AgtGrid.RetQ([8,8,0]) == [-4.0, -2.0, -4.0, -2.0] 
    assert AgtGrid.RetQ([8,9,0]) == [-3.0, -1.0, -3.0, -2.0]
    assert AgtGrid.RetQ([8,8.1,0]) == None

def test_TrainQ():
    AgtTrain = Agnt.clsAgent(["up", "down","left","right"],["x","y","terminal"])
    AgtCheck = Agnt.clsAgent(["up", "down","left","right"],["x","y","terminal"])
    AgtCheck.States.Import("csv/test/testQ.csv")
    AgtTrain.Sequence.Import("csv/test/testSeq.csv")
    # AgtTrain2.Sequence.RemoveDuplicates()
    AgtTrain.SetParameter(["alpha"],[1])
    for i in range(AgtTrain.Sequence.len):
        step = AgtTrain.Sequence[i]
        AgtTrain.States.Update(step.state0, Q=[0]*len(AgtTrain.actions))
        AgtTrain.States.Update(step.state1, Q=[0]*len(AgtTrain.actions))
    AgtTrain.States.Sort()
    AgtTrain.TrainQ(20)
    AgtTrain.States.Export("csv/test/exports/test_TrainQ.csv")

    for i in range(AgtTrain.States.len):
        assert AgtTrain.States[i].Q == AgtCheck.States[i].Q
        

def test_OnlineLearning():
    Agt = Agnt.clsAgent(["up", "down","left","right"],["x","y","terminal"])
    Agt.SetParameter(["Mode", "alpha"],["Online",1])
    Env = EnvGrid.clsEnvironment(10, 10, -1)
    Env.SetTerminalState([9,9],0)
    for i in range(3*10**4):
        Agt.PerceiveEnv(Env.State(), Env.Reward())
        Env.Step(Agt.NextAction())
    Agt.States.Sort()
    Agt.Sequence.Export("csv/test/exports/test_OnlineLearningSeq.csv")
    Agt.States.Export("csv/test/exports/test_OnlineLearningQ.csv")

    AgtTrain = Agnt.clsAgent(["up", "down","left","right"],["x","y","terminal"])
    AgtTrain.States.Import("csv/test/testQ.csv")
    for i in range(AgtTrain.States.len):
        assert AgtTrain.States[i].Q == Agt.States[i].Q

def test_OnlineLearningGreedy():
    Agt = Agnt.clsAgent(["up", "down","left","right"],["x","y","terminal"])
    Agt.SetParameter(["Mode", "alpha","epsilon"],["Online",1,[0]])
    Env = EnvGrid.clsEnvironment(5, 5, -1)
    Env.SetTerminalState([4,4],0)
    Rnr = Render.clsGrid(5,5,"")
    for i in range(800):
        Agt.PerceiveEnv(Env.State(), Env.Reward())
        Env.Step(Agt.NextAction())
        # Rnr.show(Env.RetGridAsArray(),text=str(i), tim=50)
    flag = False
    for i in range(8):
        Agt.PerceiveEnv(Env.State(), Env.Reward())
        Env.Step(Agt.NextAction())
        # Rnr.show(Env.RetGridAsArray(),text=str(i), tim=50)
        if Env.State() == [4.0, 4.0, 1]:
            flag = True

test_init();print("test_init()")
test_SetParameter();print("test_SetParameter()")
test_Perception1();print("test_Perception1()")
test_Perception2();print("test_Perception2()")
test_Reset();print("test_Reset()")
test_Mode();print("test_Mode()")
test_AnchorSates();print("test_AnchorSates()")
test_ActionDemand();print("test_ActionDemand()")
test_ActionEpsilon();print("test_ActionEpsilon()")
test_ActionGreedy();print("test_ActionGreedy()")
test_ReturnQ();print("test_ReturnQ()")
test_TrainQ();print("test_TrainQ()")
test_OnlineLearning();print("test_OnlineLearning()")
test_OnlineLearningGreedy(); print("test_OnlineLearningGreedy()")