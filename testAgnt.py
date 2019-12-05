import Agnt

# -- Init ---------------------------------------------------------------------

# Test1
Agt = Agnt.clsAgent(["jump", "run"],["world","level","terminal"])
assert Agt.actions == ["jump", "run"]
assert Agt.features == ["world","level","terminal"]
assert Agt.alpha == 0.1
assert Agt.gamma == 1.0
assert Agt.epsilon == [1.0]

# Test2
Agt.SetParameter(["alpha","gamma", "epsilon"],[0.8,0.99,[0.5]])
assert Agt.alpha == 0.8
assert Agt.gamma == 0.99
assert Agt.epsilon == [0.5]

# Test2
Agt.SetParameter(["epsilon"],[[0.2, 0.3, 0.7]])
assert Agt.epsilon == [0.2, 0.3, 0.7]

# Review 
# print(Agt.rand1000)

# -- Perception ---------------------------------------------------------------------

# Test3
assert len(Agt.States) == 0
assert len(Agt.Sequence) == 0
Agt.PerceiveEnv([2,"hi",0.1,0],-2)
assert len(Agt.States) == 1
assert len(Agt.Sequence) == 1
assert Agt.States[0].features == [2,"hi",0.1,0]
assert Agt.Sequence[0].state0 == [2,"hi",0.1,0]

# Test4
Agt.Reset()
assert len(Agt.States) == 0
assert len(Agt.Sequence) == 0

# Test5
Agt.Reset()
for i in range(100):
    Agt.PerceiveEnv([i%10,100-i%10,0],-1)
assert len(Agt.States) == 10
assert len(Agt.Sequence) == 100

# Test6
Agt.PerceiveEnv([2,0],-1)
Agt.PerceiveEnv([1,0],-1)
assert Agt.Sequence[-2].state1 == [1,0]
assert Agt.Sequence[-1].state0 == [1,0]

# Test reward
Agt.Reset()
Agt.PerceiveEnv([1,0],-2)
Agt.PerceiveEnv([2,0],-3)
Agt.PerceiveEnv([3,0],-4)
Agt.PerceiveEnv([4,1],-5)
assert Agt.Sequence[-3].reward == -2
assert Agt.Sequence[-3].totalreward == -2
assert Agt.Sequence[-2].reward == -3
assert Agt.Sequence[-2].totalreward == -5
assert Agt.Sequence[-1].reward == -4,Agt.Sequence[-1].reward
assert Agt.Sequence[-1].totalreward == -14
assert Agt.States[3].reward == -5

#Test reward
Agt.Reset()
for i in range(100):
    Agt.PerceiveEnv([i%10,100-i%10,0],-1)
assert Agt.Sequence[-1].totalreward == -100



# -- Terminal ---------------------------------------------------------------------

# Test: 
Agt.Reset()
Agt.PerceiveEnv(["A",0],-1)
Agt.PerceiveEnv(["B",0],-1)
Agt.PerceiveEnv(["C",1],-2)
Agt.PerceiveEnv(["D",0],-1)
Agt.PerceiveEnv(["E",0],-1)
assert Agt.Sequence[-4].state0 == ["A",0]
assert Agt.Sequence[-4].state1 == ["B",0]
assert Agt.Sequence[-4].reward == -1
assert Agt.Sequence[-4].totalreward == -1

assert Agt.Sequence[-3].state0 == ["B",0]
assert Agt.Sequence[-3].state1 == ["C",1]
assert Agt.Sequence[-3].reward == -1
assert Agt.Sequence[-3].totalreward == -4
assert Agt.States[2].reward == -2

assert Agt.Sequence[-2].state0 == ["D",0]
assert Agt.Sequence[-2].state1 == ["E",0]
assert Agt.Sequence[-2].reward == -1
assert Agt.Sequence[-2].totalreward == -1

assert Agt.Sequence[-1].state0 == ["E",0]
assert Agt.Sequence[-1].reward == -1
assert Agt.Sequence[-1].totalreward == -2

# Test: 
Agt.Reset()
Agt.PerceiveEnv(["A",0],-1)
Agt.PerceiveEnv(["B",1],-2)
assert Agt.Sequence[-1].reward == -1
assert Agt.Sequence[-1].totalreward == -3

# Test
Agt.Reset()
Agt.PerceiveEnv(["A",0],-1)
Agt.PerceiveEnv(["B",1],-2)
Agt.PerceiveEnv(["B",1],-2)
Agt.PerceiveEnv(["B",1],-0)
assert Agt.Nterminal == 3,Agt.Nterminal


# -- Reward ---------------------------------------------------------------------
Agt.Reset()
Agt.PerceiveEnv(["A",0],-1)
Agt.NextAction()
Agt.PerceiveEnv(["T",1],0)
Agt.NextAction()
Agt.PerceiveEnv(["A",0],-1)
Agt.NextAction()
assert Agt.Sequence[-1].totalreward == -1
Agt.ExportSeqtoCSV("csv/testSeqReward.csv")

Agt.Reset()
for i in range(2):
    Agt.PerceiveEnv([i%5+1,0],-1)
    Agt.NextAction()
    if i%5 == 0:
        Agt.PerceiveEnv([7,1],0)
Agt.ExportSeqtoCSV("csv/testSeq.csv")


# -- Action ---------------------------------------------------------------------
# Test
Agt.SetParameter(["epsilon"],[[1]])
jump = 0;run = 0
for i in range(1000):
    action = Agt.NextAction()
    if action == "jump": jump +=1
    if action == "run": run +=1
assert 450 < jump and jump < 550 and 450 < run and run < 550, jump
assert Agt.Sequence[-1].action == "run" or Agt.Sequence[-1].action == "jump", Agt.Sequence[-1].action

# Test
Agt.SetParameter(["epsilon"],[[1, 0.3, 0.7]])
jump = 0;run = 0
for i in range(1000):
    action = Agt.NextAction()
    if action == "jump": jump +=1
    if action == "run": run +=1
assert 250 < jump and jump < 350 and 650 < run and run < 750, jump
assert Agt.Sequence[-1].action == "run" or Agt.Sequence[-1].action == "jump", Agt.Sequence[-1].action

# Test
Agt.Reset()
Agt.PerceiveEnv([1,0],-1)
Agt.NextAction("jump")
Agt.PerceiveEnv([2,0],-1)
assert Agt.Sequence[-2].action == "jump"
assert Agt.Sequence[-2].actionInt == 0
Agt.NextAction("run")
Agt.PerceiveEnv([3,0],-1)
assert Agt.Sequence[-2].action == "run"
assert Agt.Sequence[-2].actionInt == 1

# -- Export Import Q ---------------------------------------------------------------------
# Test
Agt.Reset()
for i in range(100):
    Agt.PerceiveEnv([i%5+1,0],-1)
    Agt.NextAction()
    if i%5 == 0:
        Agt.PerceiveEnv([7,1],-2)
Agt.ExportQtoCSV("csv/testQ.csv")
AgtTestQ = Agnt.clsAgent(["jump", "run"],["world","level","terminal"])
AgtTestQ.ImportQ("csv/testQ.csv")

for i in range(len(Agt.States)):
    assert Agt.States[-1*i].features == AgtTestQ.States[-1*i].features
    assert Agt.States[-1*i].Q == AgtTestQ.States[-1*i].Q
    # assert Agt.State[-1*i].QUpdated == AgtTestQ.State[-1*i].QUpdated  this is not imported

# -- Export Import Seq ---------------------------------------------------------------------
# Test
Agt.Reset()
for i in range(100):
    Agt.PerceiveEnv([i%5+1,0],-1)
    Agt.NextAction()
    if i%5 == 0:
        Agt.PerceiveEnv([7,1],-2)
Agt.ExportSeqtoCSV("csv/testSeq.csv")
AgtTestS = Agnt.clsAgent(["jump", "run"],["world","level","terminal"])
AgtTestS.ImportSeq("csv/testSeq.csv")

for i in range(100):
    assert Agt.Sequence[-1*i].state0 == AgtTestS.Sequence[-1*i].state0
    assert Agt.Sequence[-1*i].state1 == AgtTestS.Sequence[-1*i].state1
    assert Agt.Sequence[-1*i].reward == AgtTestS.Sequence[-1*i].reward
    assert Agt.Sequence[-1*i].totalreward == AgtTestS.Sequence[-1*i].totalreward
    assert Agt.Sequence[-1*i].action == AgtTestS.Sequence[-1*i].action
    assert Agt.Sequence[-1*i].actionInt == AgtTestS.Sequence[-1*i].actionInt
    assert Agt.Sequence[-1*i].rg == AgtTestS.Sequence[-1*i].rg
    # assert Agt.Sequence[-1*i].StepSampled == AgtTest.Sequence[-1*i].StepSampled  this is not imported
assert Agt.States[0].features == [1.0,0]
assert Agt.States[2].features == [2.0,0]
assert Agt.States[3].features == [3.0,0]
assert Agt.States[4].features == [4.0,0]
assert Agt.States[5].features == [5.0,0]
assert Agt.States[1].features == [7.0,1]

# Test
Agt.Reset()
for i in range(2*10**2):
    Agt.PerceiveEnv([i,0],-1)
    Agt.NextAction()
    print(i,end = "\r")
assert len(Agt.Sequence) == 2*10**2
Agt.SetParameter(["buffer","batch"],[10**2,10**2])
assert Agt.buffer == 10**2
assert Agt.batch == 10**2
assert len(Agt.Sequence) == 10**2

# Test
Agt.Reset()
Agt.SetParameter(["buffer"],[5])
for i in range(5):
    Agt.PerceiveEnv([i,0],-1)
assert Agt.Sequence[0].state0 == [0,0]
assert Agt.Sequence[-1].state0 == [4,0]
Agt.PerceiveEnv([5,0],-1)
assert Agt.Sequence[0].state0 == [1,0]
assert Agt.Sequence[-1].state0 == [5,0]

# Test Sort
Agt.Reset()
Agt.ImportSeq("csv/test/testSeq.csv")
Agt.SortSequence()
Agt.RemoveDuplicateSteps()
c = 0
for i in range(10):
    for j in range(10):
        if i == 9 and j == 9:
            assert Agt.Sequence[c-1].state1 == [float(i), float(j), 1]
            break
        for k in range(4):
            assert Agt.Sequence[c].state0 == [float(i), float(j), 0],c
            assert Agt.Sequence[c].actionInt == k,str(c) + " " + str(k)
            c +=1
Agt.ExportSeqtoCSV("csv/test/testSeqSorted.csv")


assert False, "testAgnt sucessfull"