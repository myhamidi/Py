import CCEnv
import Agt
import random

### Parameter:
StartSpeed = 80
BrakeInc = 0.1

### Init Environment and Agent
Env = CCEnv.clsCCEnv(StartSpeed ,StartSpeed /3,BrakeInc,"v",1)
Env.InitRetStateStyle([False,True,True,True])
Agt = Agt.clsAgent(Env.ReturnActionList())
Env.MonitorStart()

### Config
Env.setConstraint0([(0.1,1)])
Env.setConstraint1([(0.01,-8*random.random())])

### Run
m = ""
dur_train = 1000
c=0
for i in range(int(dur_train/CCEnv.Car.pbTimeStep)):
    # eps = 1-i/(dur_train/CCEnv.Car.pbTimeStep)
    eps = 1
    if Env.Cars[1].v > 1:
        Agt.PerceiveState(Env.RetState(),Env.ReturnReward())
        Env.Next(Agt.NextAction(eps),m)
    else:
        Env.Next("", m)
    if "terminal" in str(Env.RetState()):
        c+=1
        Agt.PerceiveState(Env.RetState(),Env.ReturnReward())
        Env.Reset()
        Env.setConstraint1([(0.01,-8*random.random())])
        print(c)

m = "monitor"
dur_test = 2
c=0
Agt.SequenceRewardsReset()
for i in range(int(dur_test/CCEnv.Car.pbTimeStep)):
    Agt.TakeState(Env.RetState(),Env.ReturnReward())
    Env.Next(Agt.NextAction(0),m)
    if "terminal" in str(Env.RetState()):
        c+=0.2
        Agt.TakeState(Env.RetState(),Env.ReturnReward())
        print(str(round(-2-c,1)) + ")   v0: " + str(round(Env.Cars[0].v,2))+"  v1: " + 
        str(round(Env.Cars[1].v,2))+".Reward: "+str(round(Agt.RetTotalReward())))
        Env.setConstraint1([(0.1,-2-c)])
        Env.Reset()
        Agt.SequenceRewardsReset()

Env.setConstraint1([(0.1,-7)])
for i in range(1,40):
    Agt.TakeState(Env.RetState(),Env.ReturnReward())
    Env.Next(Agt.actions[1],m)
    if "terminal" in str(Env.RetState()):
        Agt.TakeState(Env.RetState(),Env.ReturnReward())
        print(str(round(-7,1)) + "opt)   v0: " + str(round(Env.Cars[0].v,2))+"  v1: " + 
        str(round(Env.Cars[1].v,2))+".Reward: "+str(round(Agt.RetTotalReward())))
        Env.Reset()
        Agt.SequenceRewardsReset()
        Env.setConstraint1([(0.1,-7)])

### Print Sequences of Run
f = open("SeqRews.csv","w")
q = open("Q.csv","w")
f.write("stateIndex,state,reward,actionIndex\n")
for i in range(len(Agt.SequenceRewards)):
    s,r,a = Agt.SequenceRewards[i]
    va = Agt.RewStates[s].state
    f.write(str(s) + ","+str(va) + ","+str(r) + "," + str(a) + "\n")

q.write("state:v,state:a,q1,q2,visited\n")
for i in range(len(Agt.Q)):
    va = Agt.RewStates[i].state
    Qi = [round(Agt.Q[i][0],2),round(Agt.Q[i][1],2)]
    Q = str(Qi).replace("[","").replace("]","")
    q.write(str(va) + "," + Q + "," + str(Agt.RewStates[i].visited) +"\n")