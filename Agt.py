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
        self.SequenceRewards = []   #Typ: (s,r,a). Remembers state (idx), reward and action
        self.TransitionMatrix = []  #Typ: List of Lists [[],[],...]
        self.actions = actionlist
        self.LastAction = ""
        self.LastActionInt = 0
        self.Q = []
        #Parameters:
        self.alpha = .2
        self.gamma = 1

    def PerceiveState(self,strState,reward):
        tr.call("clsAgent.PerceiveState")
        idx = self.pvRetIndex(strState,reward)
        if len(self.SequenceRewards) == 0:r=0
        else: _,r,_ = self.SequenceRewards[-1]
        self.SequenceRewards.append((idx,round(r+reward,1),self.LastActionInt))
        self.pvExtendTransitionMatrix()
        self.pvUpdateQ(self.alpha,self.gamma)

    def RetNextAction(self):
        tr.call("clsAgent.RetNextAction")
        #Random
        self.LastAction = random.choice(self.actions)
        self.LastActionInt =self.actions.index(self.LastAction)
        # #Greedy
        # s,_,_ = self.SequenceRewards[-1]        
        # self.LastActionInt = self.Q[s].index(max(self.Q[s]))
        # self.LastAction = self.actions[self.LastActionInt]
        #Return
        return self.LastAction

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
        _,rsum,_ = self.SequenceRewards[-1]
        for i in range(len(self.SequenceRewards)):
            idx,rx,_ = self.SequenceRewards[i]
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
            FromIdx,_,_ = self.SequenceRewards[-2]
            ToIdx,_,_ = self.SequenceRewards[-1]
            if not (self.LastAction,ToIdx) in self.TransitionMatrix[FromIdx]:
                self.TransitionMatrix[FromIdx].append((self.LastAction,ToIdx))

    def pvExtendQ(self):
        self.Q.append([])
        for  _ in range(len(self.actions)):
            self.Q[-1].append(0)
    
    def pvUpdateQ(self,alpha, gamma):
        if len(self.SequenceRewards)<3: return
        s1,r1,a = self.SequenceRewards[-1]
        s,r,_ = self.SequenceRewards[-2]
        r = r1-r
        if "terminal" in str(self.RewStates[s].state):
            self.SequenceRewards[-1] = (s1,0,a)
            return
        self.Q[s][a] = self.Q[s][a] + alpha*(r +gamma*max(self.Q[s1]) - self.Q[s][a])
                       


