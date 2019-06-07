import EnvGrid
import Agt
import random

### Parameter:

### Init Environment and Agent
Env = EnvGrid.clsEnvironment(8,8,-1)
Agt = Agt.clsAgent(Env.ReturnActionList())
Env.MonitorStart()

### Config
Env.setTerminalStates([(0,0),(7,7)])
Env.SetStart((0,7))

### Run
f01 = 100000
for i in range(int(f01)):
    eps = 1
   # eps = 1-i/2*f01
    Agt.PerceiveState(Env.RetState(),Env.RetReward())
#     Env.Next(Agt.RetNextAction("random"))
    Env.Next(Agt.NextAction(eps))
    if "terminal" in str(Env.RetState()):
        Agt.PerceiveState(Env.RetState(),Env.RetReward())
        Env.Reset()
        Env.SetStart((random.randint(0,7),(random.randint(0,7))))
    if i%100 == 0: print(i)

for _ in range(100):
    Env.MonitorUpdate()
    Agt.TakeState(Env.RetState(),Env.RetReward())
    Env.Next(Agt.RetNextAction("greedy"))
    if "terminal" in str(Env.RetState()):
        Env.MonitorUpdate()
        Agt.TakeState(Env.RetState(),Env.RetReward())
        Env.Reset()
        Env.SetStart((random.randint(0,7),(random.randint(0,7))))

### Print Sequences of Run
f = open("SeqRews-Grid.csv","w")
q = open("Q-Grid.csv","w")
f.write("stateIndex,state,reward,actionIndex\n")
for i in range(len(Agt.SequenceRewards)):
    s,r,a = Agt.SequenceRewards[i]
    va = Agt.RewStates[s].state
#     Qs = [round(Agt.Q[s][0]),round(Agt.Q[s][1]),round(Agt.Q[s][2]),round(Agt.Q[s][3])]
#     Q = str(Qs).replace("[","").replace("]","")
    f.write(str(s) + "," + str(va) + ","+str(r) + ","+str(a) +"\n")

q.write("state,Q:up,Q:down,Q:left,Q:right,visited\n")
for i in range(len(Agt.Q)):
    va = Agt.RewStates[i].state
    Qi = [round(Agt.Q[i][0]),round(Agt.Q[i][1]),round(Agt.Q[i][2]),round(Agt.Q[i][3])]
    Q = str(Qi).replace("[","").replace("]","")
    q.write(str(va) + "," + Q + "," + str(Agt.RewStates[i].visited) +"\n")