import EnvGrid
import Agt

### Parameter:
GZx = 10
GZy = 10

### Init
Env = EnvGrid.clsEnvironment(GZx,GZy,-1)
Agt = Agt.clsAgent(Env.ReturnActionList())

### Config
Env.SetTerminalState((0,0)); Env.SetRewardAtState((0,0),0)
Env.SetTerminalState((GZx-1,GZy-1)); Env.SetRewardAtState((GZx-1,GZy-1),0)
Env.SetRestartPosition((int(GZx/2),int(GZy/2)))

### Train
c = 0; runs_train = 3000
while c < runs_train:
    Agt.PerceiveState(Env.RetState(),Env.RetReward())
    if Env.IsStateTerminal():
        c+=1
        Env.Reset()
    if c%100 == 0: 
        print("Train Step: " + str(c),end ='\r')
    eps = 1-c/runs_train
    Env.Next(Agt.NextAction(eps))

### Test
tmpState = ""; c = 0; runs_train = 10 #2*(GZ-1)
Env.SetRandomStart()
while c < runs_train:
    Agt.TakeState(Env.RetState(),Env.RetReward())
    Env.render(0.1,"InTKinter")   #"InConsole"
    if Env.RetState() == tmpState:
        print("error - No State Change during Test " + tmpState + " " + str(c))
        break
    tmpState = Env.RetState()
    if Env.IsStateTerminal():
        tmpState = ""; c+=1
        Env.Reset()
        Env.SetRandomStart()
    eps = 0
    Env.Next(Agt.NextAction(eps))

# # myTracer
# arr = EnvGrid.tr.getCalls()
# print(*arr, sep="\n")

### Print Sequences of Run
f = open("SeqRews-Grid.csv","w")
q = open("Q-Grid.csv","w")
f.write("stateIndex,state,reward,actionIndex\n")
for i in range(len(Agt.SequenceRewards)):
    s,r,a,ty = Agt.SequenceRewards[i]
    va = Agt.RewStates[s].state
    f.write(str(s) + "," + str(va) + ","+str(r) + ","+str(a) + "," + str(ty) + "\n")

q.write("state,Q:up,Q:down,Q:left,Q:right,visited\n")
for i in range(len(Agt.Q)):
    va = Agt.RewStates[i].state
    if len(Env.ReturnActionList()) == 2:
        Qi = [round(Agt.Q[i][0],4),round(Agt.Q[i][1],4)]
    if len(Env.ReturnActionList()) == 4:
        Qi = [round(Agt.Q[i][0],4),round(Agt.Q[i][1],4),round(Agt.Q[i][2],4),round(Agt.Q[i][3],4)]
    Q = str(Qi).replace("[","").replace("]","")
    q.write(str(va) + ";" + Q + ";" + str(Agt.RewStates[i].visited) +"\n")