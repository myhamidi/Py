import myTracer;tr = myTracer.glTracer

import random

class typRewState:
    def __init__(self,stateStr,reward,value,visited):
        tr.call("typRewState.init")
        self.state = stateStr
        self.reward = reward
        self.value = value
        self.visited = visited

class clsAgent:
#Public:
    def __init__(self,actionlist):
        tr.call("clsAgent.init")
        self.RewStates = []         #Typ: typRewState. Remembers all (unique) states visited.
        self.SequenceRewards = []   #Typ: (s,r,a,actionType). Remembers state (idx), reward and action
        self.TransitionMatrix = []  #Typ: List of Lists of tuples[[],[],...]
        self.actions = actionlist
        self.LastAction = ""
        self.LastActionType = "" #g,r (greedy, random)
        self.LastActionInt = 0
        self.Q = []
        #Parameters:
        self.alpha = .1
        self.gamma = 1
        self.rand = list(range(1000))
        random.shuffle(self.rand)
        self.randIdx = 0

    def PerceiveState(self,strState,reward):
        tr.call("clsAgent.PerceiveState")
        idx = self.pvRetIndex(strState,reward)
        alpha = max(1/self.RewStates[idx].visited,self.alpha)      # Learning rate adaptation
        if len(self.SequenceRewards) == 0:r=0
        else: _,r,_,_ = self.SequenceRewards[-1]
        self.SequenceRewards.append((idx,round(r+reward,1),self.LastActionInt,self.LastActionType))
        self.pvExtendTransitionMatrix()
        self.pvUpdateQ(alpha,self.gamma)
    
    def TakeState(self,strState,reward):
        idx = self.pvRetIndex(strState,0)
        if len(self.SequenceRewards) == 0:r=0
        else: _,r,_,_ = self.SequenceRewards[-1]
        self.SequenceRewards.append((idx,round(r+reward,1),self.LastActionInt,self.LastActionType))

    def NextAction(self,epsilon):
        # Get Next Random Number from list
        self.randIdx +=1
        if self.randIdx == 1000: self.randIdx = 0
        rand = self.rand[self.randIdx]/1000

        if rand < epsilon:
            return self.RetNextAction("random")
        else:
            return self.RetNextAction("greedy")
    
    def RetNextAction(self,policy):
        if policy == "random":
            self.LastAction = random.choice(self.actions)
            self.LastActionInt =self.actions.index(self.LastAction)
            self.LastActionType = "r"
            return self.LastAction
        if policy == "greedy":
            s,_,_,_ = self.SequenceRewards[-1]        
            self.LastActionInt = self.Q[s].index(max(self.Q[s]))
            self.LastAction = self.actions[self.LastActionInt]
            self.LastActionType = "g"
            return self.LastAction
        #Return
        return ""

    def RetTotalReward(self):
        _,r,_,_ = self.SequenceRewards[-1]
        return r
    
    def SequenceRewardsReset(self):
        self.SequenceRewards = []

    def IntiSequences(self):
        self.SequenceRewards =[]
    
    def InitQ(self,alpha, gamma):
        self.alpha = alpha
        self.gamma = gamma
    
    def DoBellman(self,iterations):
        tmpVF = [self.RewStates[i].value for i in range(len(self.RewStates))]
        for _ in range(iterations):
            for i in range(len(self.TransitionMatrix)):
                tmpVF[i] = self.RewStates[i].reward
                n = len(self.TransitionMatrix[i])
                for j in range(n):
                    _,idx = self.TransitionMatrix[i][j]
                    tmpVF[i] = tmpVF[i] + self.RewStates[idx].value/n
            
            for i in range(len(self.RewStates)):
                self.RewStates[i].value = round(tmpVF[i],4)
    
    def Update_ValueFunctionMC(self):
        _,rsum,_,_ = self.SequenceRewards[-1]
        for i in range(len(self.SequenceRewards)):
            idx,rx,_,_ = self.SequenceRewards[i]
            self.RewStates[idx].visited += 1
            self.RewStates[idx].value += (rsum-rx-self.RewStates[idx].value)/self.RewStates[idx].visited



#Private:
    def pvAppendNewState(self,RewardState):
        self.RewStates.append(RewardState)
        self.TransitionMatrix.append([])
        self.pvExtendQ()

    def pvRetIndex(self,strState,reward):
        tr.call("clsAgent.pvRetIndex")
        for i in range(len(self.RewStates)):
            if strState == self.RewStates[i].state:
                self.RewStates[i].visited +=1
                return i
        # NewRewSate = typRewState(state,0,0,0)
        self.pvAppendNewState(typRewState(strState,reward,0,0))
        i = len(self.RewStates) - 1
        self.RewStates[i].visited +=1
        return i #return index

    def pvExtendTransitionMatrix(self): #Type StateTransition: (1,3). From 1 to 3
        tr.call("clsAgent.pvExtendTransitionMatrix")
        if len (self.SequenceRewards)>1: #start from 2nd step
            FromIdx,_,_,_ = self.SequenceRewards[-2]
            ToIdx,_,_,_ = self.SequenceRewards[-1]
            if not (self.LastAction,ToIdx) in self.TransitionMatrix[FromIdx]:
                self.TransitionMatrix[FromIdx].append((self.LastAction,ToIdx))
                self.TransitionMatrix[FromIdx].sort()

    def pvExtendQ(self):
        self.Q.append([])
        for  _ in range(len(self.actions)):
            self.Q[-1].append(0)
    
    def pvUpdateQ(self,alpha, gamma):
        if len(self.SequenceRewards)<3: 
            return
        s1,r1,a,_ = self.SequenceRewards[-1]
        s,r,_,_ = self.SequenceRewards[-2]
        r = r1-r
        self.ResetRewardAfterTerminal()
        self.Q[s][a] = self.Q[s][a] + alpha*(r +gamma*max(self.Q[s1]) - self.Q[s][a])

    def ResetRewardAfterTerminal(self):
        s,_,_,_ = self.SequenceRewards[-2]
        s1,_,a,ty = self.SequenceRewards[-1]
        if "terminal" in str(self.RewStates[s].state):
            self.SequenceRewards[-1] = (s1,0,a,ty)

    def printTransitions(self,textfile,xwr):
        f = open(textfile,xwr)
        f.write("Transitions\n")
        f.write("state|visited|q1|q2\n")    
        for i in range(len(self.TransitionMatrix)):
            tmpstr = self.RewStates[i].state + "|" + str(self.RewStates[i].visited) + "|" 
            for j in range(len(self.TransitionMatrix[i])):
                a,toState = self.TransitionMatrix[i][j]
                aIdx = self.actions.index(a)
                tmpstr += a + self.RewStates[toState].state + "Q:" + str(round(self.Q[i][aIdx],4)) + "|"
            f.write(tmpstr + "\n")

    def printQ(self,textfile,xwr):  
        f = open(textfile,xwr)
        f.write("Transitions\n")
        f.write("state|visited|q1|q2\n")
        for i in range(len(self.TransitionMatrix)):
            tmpstr = self.RewStates[i].state.replace(",","|") + "|" + str(self.RewStates[i].visited) + "|" 
            for j in range(len(self.Q[i])):
                a = self.actions[j]
                tmpstr += a + "| Q:" + str(round(self.Q[i][j],4)) + "|"
                # tmpstr += a + self.RewStates[toState].state + "Q:" + str(round(self.Q[i][aIdx],4)) + "|"
            f.write(tmpstr + "\n")

    def printSequence100(self,textfile,xwr):
        f = open(textfile,xwr)
        f.write("Sequences 100\n")
        f.write("stateIndex|state|reward|actionIndex|greed\n")
        #Create evenly distributed indices
        arr = []; arrTerminal = []; c = 0
        for i in range(len(self.SequenceRewards)):
            s,_,_,_ = self.SequenceRewards[i]
            if "terminal" in str(self.RewStates[s].state):
                arrTerminal.append(i)
        for i in range(100):
            arr.append(int(i * len(arrTerminal)/99))
        # for i in range(len(self.SequenceRewards)):
        for i in range(99):
            # s,r,a,ty = self.SequenceRewards[arrTerminal[arr[i]]+1]
            for j in range(arrTerminal[arr[i]+1] - arrTerminal[arr[i]]):
                    s,r,a,ty = self.SequenceRewards[arrTerminal[arr[i]]+j+1]
                    va = self.RewStates[s].state
                    f.write(str(s) + "|" + str(va) + "|" + str(r) + "|" + str(a) + "|" + str(ty) + "\n")         


