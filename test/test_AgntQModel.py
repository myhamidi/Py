import sys
sys.path.append("C:\\temp Daten\\Lernbereich\\Git\\myhamidi\\Py")
# import Agnt_DQN
import Agnt
import EnvGrid
import Render

def test_ImportExportWeights():
    Agt = Agnt.clsAgent(["up", "down", "left", "right"],["x","y","terminal"])
    Agt.Sequence.Import("csv/test/testSeq.csv")
    Agt.Sequence.RemoveDuplicates()
    Agt.Sequence.Sort()
    Agt.QModel.SetUp()
    Agt.QModel.batch = Agt.Sequence.len
    Agt.QModel.TrainToReward(Agt.Sequence, StopAt=[5.0e-03,0])
    Agt.QModel.Train(Agt.Sequence, 30, StopAt=[5.0e-03,0])
    Agt.QModel.ExportWeights("csv/test/exports/", "test_Main")

    AgtCopy = Agnt.clsAgent(["up", "down", "left", "right"],["x","y","terminal"])
    AgtCopy.QModel.SetUp()
    AgtCopy.QModel.ImportWeights("csv/test/exports/test_Main_6-relu64-linear1.h5")

    X = Agt.Sequence.ReturnStates(None)
    Y1 = Agt.QModel.Predict(X,rund=1)
    Y2 = AgtCopy.QModel.Predict(X,rund=1)
    assert Y1 == Y2

    Agt.States.Update(X, Q=Y1)
    Agt.States.Export("csv/test/exports/test_ImportExportWeightsQ.csv")

def test_Main():
    Agt = Agnt.clsAgent(["up", "down", "left", "right"],["x","y","terminal"])
    Agt.Sequence.Import("csv/test/testSeq.csv")
    Agt.Sequence.RemoveDuplicates()
    Agt.Sequence.Sort()
    Agt.QModel.SetUp()
    Agt.QModel.batch = 200
    # Agt.QModel.ImportWeights("csv/test/exports/test_Main3_6-relu64-linear1.h5")
    Agt.QModel.TrainToReward(Agt.Sequence, StopAt=[5.0e-04,0])
    Agt.QModel.Train(Agt.Sequence, 250, StopAt=[5.0e-04,0])
    Agt.QModel.ExportWeights("csv/test/exports/", "test_Main")

    X = Agt.Sequence.ReturnStates(None)
    Y = Agt.QModel.Predict(X,rund=2)

    Agt.States.Update(X, Q=Y)
    Agt.States.Export("csv/test/exports/test_Main-QReward.csv")

def test_OnlineRandomWalk():
    Agt = Agnt.clsAgent(["up", "down", "left", "right"],["x","y","terminal"])
    Agt.SetParameter(["Mode", "epsilon"],["Online",[1]])
    Agt.QModel.SetUp()
    Agt.QModel.batch = 50
    Env = EnvGrid.clsEnvironment(5, 5, -1)
    Env.SetTerminalState([4,4],0)
    Rnr = Render.clsGrid(5,5,"")
    for i in range(100):
        Agt.PerceiveEnv(Env.State(), Env.Reward())
        Agt.QModel.TrainToReward(Agt.Sequence)
        Env.Step(Agt.NextAction())
        Rnr.show(Env.RetGridAsArray(),text=str(i), tim=50)
    for i in range(200):
        Agt.PerceiveEnv(Env.State(), Env.Reward())
        Agt.QModel.Train(Agt.Sequence)
        Env.Step(Agt.NextAction())
        Rnr.show(Env.RetGridAsArray(),text=str(i), tim=50)

    X = Agt.Sequence.ReturnStates(None)
    Y = Agt.QModel.Predict(X, rund=2)

    Agt.States.Update(X, Q=Y)
    Agt.States.Sort()
    Agt.States.Export("csv/test/exports/test_OnlineRandomWalkQ.csv")

def test_OnlineGreedyWalk():
    Agt = Agnt.clsAgent(["up", "down", "left", "right"],["x","y","terminal"])
    Agt.SetParameter(["Mode", "epsilon"],["Online",[1]])
    Agt.QModel.SetUp()
    Agt.QModel.batch = 200
    Env = EnvGrid.clsEnvironment(10, 10, -1)
    Env.SetTerminalState([9,9],0)
    Rnr = Render.clsGrid(10,10,"")
    for i in range(1000):
        Agt.PerceiveEnv(Env.State(), Env.Reward())
        Agt.QModel.TrainToReward(Agt.Sequence)
        Env.Step(Agt.NextAction())
        # Rnr.show(Env.GridStateAsList(),text=str(i), tim=50)
    Agt.SetParameter(["epsilon"],[[0.2]])
    for i in range(1000):
        Agt.PerceiveEnv(Env.State(), Env.Reward())
        Agt.QModel.Train(Agt.Sequence, StopAt=[5.0e-03,0])
        Env.Step(Agt.NextAction())
        print(i)
        # Rnr.show(Env.GridStateAsList(),text=str(i), tim=50)
    Agt.SetParameter(["epsilon"],[[1]])
    for i in range(100):
        Agt.PerceiveEnv(Env.State(), Env.Reward())
        Env.Step(Agt.NextAction())
        Rnr.show(Env.GridStateAsList(),text=str(i), tim=50)

    X = Agt.Sequence.ReturnStates(None)
    Y = Agt.QModel.Predict(X, rund=2)

    Agt.States.Update(X, Q=Y)
    Agt.States.Sort()
    Agt.States.Export("csv/test/exports/test_OnlineGreedyWalkQ.csv")
    Agt.Sequence.Export("csv/test/exports/test_OnlineGreedyWalkSeq.csv")

# test_ImportExportWeights()
# test_Main()
# test_OnlineRandomWalk()
test_OnlineGreedyWalk()