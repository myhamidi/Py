import CCEnv
import Agt
import Render
import random

### Parameter:
StartSpeed = 80
BrakeInc = 0.5
M_MAX = 120

### Init Environment and Agent
Env = CCEnv.clsCCEnv(StartSpeed,StartSpeed /3, M_MAX, BrakeInc,"t",0.10)
Env.InitRetStateStyle([True,False,False,True])
Agt = Agt.clsAgent(Env.ReturnActionList())
Rnr = Render.clsGrid(1,M_MAX,"")
# Env.MonitorStart()

### Config
Env.setCar0_Accelerations([(1.5,-6)])
a = -6 #-8*random.random()
Env.setCar1_Accelerations([(0.01,a)])

### Train
m = ""
c=0; runs_train = 50000
while c < runs_train:
    if Env.Cars[1].v > 1:
        Agt.PerceiveState(Env.RetState(),Env.ReturnReward())
    if "terminal" in str(Env.RetState()):
        c+=1
        Env.Reset()
    eps = 1-c/runs_train
    Env.Next(Agt.NextAction(eps),m)
    if c%100 == 0: print(c, end ='\r')


### Test
m = "monitor"; runs_test = 1; c = 0
acc = -6
Env.setCar1_Accelerations([(0.01,acc)])
while c < runs_test:
    Agt.TakeState(Env.RetState(),Env.ReturnReward())
    Env.Next(Agt.NextAction(0),m)
    Rnr.renderArray(Env.RetGridAsArray(),Env.RetState(),50)
    if "terminal" in str(Env.RetState()):
        Agt.TakeState(Env.RetState(),Env.ReturnReward())
        print(str(round(acc,1)) + ")   v0: " + str(round(Env.Cars[0].v,2))+"  v1: " + 
        str(round(Env.Cars[1].v,2))+".Reward: "+ str(round(Agt.RetRewardCurrentState())))
        Env.Reset()
        c+=1; acc = -3-c
        Env.setCar1_Accelerations([(0.01,acc)])
    # Agt.ResetRewardAfterTerminal()

### Print Sequences of Run
Agt.printSequence100("SeqRews.csv","w")
Agt.printSequenceTest("SeqTest.csv","w")
Agt.printQ("Q.csv","w")