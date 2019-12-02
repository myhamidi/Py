import Agnt

# -- Init ---------------------------------------------------------------------

# Test1
Agt = Agnt.clsAgent(["jump", "run"],["world","level","terminal"])
retStr = "Actions: ['jump', 'run']"+"\n";retStr += "State Features: ['world', 'level', 'terminal']"
assert Agt.Info() == retStr

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

# Test7
Agt.Reset()
Agt.PerceiveEnv([1,0],-2)
Agt.PerceiveEnv([2,0],-3)
assert Agt.Sequence[-2].reward == -2
assert Agt.Sequence[-2].totalreward == -2
assert Agt.Sequence[-1].reward == -3
assert Agt.Sequence[-1].totalreward == -5

#Test8
Agt.Reset()
for i in range(100):
    Agt.PerceiveEnv([i%10,100-i%10,0],-1)
assert Agt.Sequence[-1].totalreward == -100

# -- Terminal ---------------------------------------------------------------------

# Test: 
Agt.PerceiveEnv(["A",0],-1)
Agt.PerceiveEnv(["B",0],-1)
Agt.PerceiveEnv(["C",1],-1)
Agt.PerceiveEnv(["D",0],-1)
Agt.PerceiveEnv(["E",0],-1)
assert Agt.Sequence[-4].state0 == ["A",0]
assert Agt.Sequence[-4].state1 == ["B",0]

assert Agt.Sequence[-3].state0 == ["B",0]
assert Agt.Sequence[-3].state1 == ["C",1]

assert Agt.Sequence[-2].state0 == ["D",0]
assert Agt.Sequence[-2].state1 == ["E",0]

assert Agt.Sequence[-1].state0 == ["E",0]

# -- Action ---------------------------------------------------------------------
# Test
Agt.SetParameter(["epsilon"],[[1]])
jump = 0;run = 0
for i in range(1000):
    action = Agt.NextAction()
    if action == "jump": jump +=1
    if action == "run": run +=1
assert 450 < jump and jump < 550 and 450 < run and run < 550, jump

# Test
Agt.SetParameter(["epsilon"],[[1, 0.3, 0.7]])
jump = 0;run = 0
for i in range(1000):
    action = Agt.NextAction()
    if action == "jump": jump +=1
    if action == "run": run +=1
assert 250 < jump and jump < 350 and 650 < run and run < 750, jump