import CCEnv
import Agt
import random

### Parameter:
StartSpeed = 80
BrakeInc = 0.5

### Init Environment and Agent
Env = CCEnv.clsCCEnv(StartSpeed ,StartSpeed /3,BrakeInc,"x",1)
Env.InitRetStateStyle([False,True,True,True])
Agt = Agt.clsAgent(Env.ReturnActionList())
Env.MonitorStart()

### Config
Env.setCar0_Accelerations([(2,-8)])

### Train
m = ""; runs_train = 30000; c=0
a = -7 #-8*random.random()
Env.setCar1_Accelerations([(0.01,a)])
while c < runs_train:
    eps = 1#-c/runs_train
    if Env.Cars[1].v > 1:
        Agt.PerceiveState(Env.RetState(),Env.ReturnReward())
        Env.Next(Agt.NextAction(eps),m)
    else:
        Env.Next("", m)
    if "terminal" in str(Env.RetState()):
        c+=1
        Agt.PerceiveState(Env.RetState(),Env.ReturnReward())
        Env.Reset()
        #Agt.SequenceRewardsReset()
        a = -7 #-8*random.random()
        Env.setCar1_Accelerations([(0.01,a)])
        if c%100 == 0: 
            print(c, end ='\r')

### Test
m = "monitor"; runs_test = 6; c = 0
a = -3-c
Env.setCar1_Accelerations([(0.01,a)])
while c < runs_test:
    Agt.TakeState(Env.RetState(),Env.ReturnReward())
    Env.Next(Agt.NextAction(0),m)
    Env.render("xa")
    if "terminal" in str(Env.RetState()):
        Agt.TakeState(Env.RetState(),Env.ReturnReward())
        print(str(round(-2-c,1)) + ")   v0: " + str(round(Env.Cars[0].v,2))+"  v1: " + 
        str(round(Env.Cars[1].v,2))+".Reward: "+str(round(Agt.RetTotalReward())))
        Env.Reset()
        c+=1; a = -3-c
        Env.setCar1_Accelerations([(0.01,a)])   

### Print Sequences of Run
Agt.printSequence("SeqRews.csv","w")
Agt.printQ("Q.csv","w")