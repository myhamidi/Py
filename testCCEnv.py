import CCEnv
import Agt

### Parameter:
StartSpeed = 80
BrakeInc = 0.1

### Init Environment and Agent
Env = CCEnv.clsCCEnv(StartSpeed ,StartSpeed /3,BrakeInc)
Agt = Agt.clsAgent(Env.ReturnActionList())
Env.MonitorStart()

### Run
for _ in range(int(10/0.01)):
    Env.MonitorUpdate()
    _,State,_ = Env.Cars[1].Retxva()
    Agt.PerceiveState(State,0)
    if State == 0: break
    #nextAction = Agt.RetNextAction()
    Env.Next(Agt.RetNextAction())

### Print Sequences of Run
f = open("SeqRews.txt","w")
for i in range(len(Agt.SequenceRewards)):
    f.write(str(Agt.SequenceRewards[i]) +"\n")