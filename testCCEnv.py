import CCEnv
import Agt

### Parameter:
StartSpeed = 80
BrakeInc = 0.2

### Init Environment and Agent
Env = CCEnv.clsCCEnv(StartSpeed ,StartSpeed /3,BrakeInc)
Agt = Agt.clsAgent(Env.ReturnActionList())
Env.MonitorStart()

### Config
Env.setConstraint([(2,-10)])

### Run
for i in range(int(100/0.01)):
    if i > int(100/0.01)-100: Env.MonitorUpdate()
    if Env.Cars[1].v > 1:
        Agt.PerceiveState(Env.RetState(),Env.ReturnReward())
        Env.Next(Agt.RetNextAction())
    else:
        Env.Next("")
    if "terminal" in str(Env.RetState()):
        Agt.PerceiveState(Env.RetState(),Env.ReturnReward())
        Env.Reset()

### Print Sequences of Run
f = open("SeqRews.csv","w")
q = open("Q.csv","w")
f.write("state,reward,action,state:v,state:a\n")
for i in range(len(Agt.SequenceRewards)):
    s,r,a = Agt.SequenceRewards[i]
    va = Agt.RewStates[s].state
    Q = str(Agt.Q[s]).replace("[","").replace("]","")
    f.write(str(s) + ","+str(r) + ","+str(a) + "," + str(va) + Q + "\n")

q.write("state:v,state:a,q1,q2,visited\n")
for i in range(len(Agt.Q)):
    va = Agt.RewStates[i].state
    Q = str(Agt.Q[i]).replace("[","").replace("]","")
    q.write(str(va) + "," + Q + "," + str(Agt.RewStates[i].visited) +"\n")