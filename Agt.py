import myTracer;tr = myTracer.glTracer

class typRewState:
    def __init__(self,stateStr,reward,value,visited):
        tr.call("typRewState.init")
        self.state = stateStr
        self.reward = reward
        self.value = value
        self.visited = visited

class clsAgent:
#Public:
    def __init__(self):
        tr.call("clsAgent.init")
        self.RewStates = [] #Typ: typRewState. Remembers all (unique) states visited.
        self.SequenceRewards = []  #Typ: (s,r). Remembers the sequence of states and commulative reward at step i
        self.TransitionMatrix = [] #Typ: List of Lists [[],[],...]

    def PerceiveState(self,RewardState):
        tr.call("clsAgent.PerceiveState")
        idx = self.pvRetIndex(RewardState)
        self.SequenceRewards.append((idx,0))
        self.pvExtendTransitionMatrix()

#Private:
    def pvAppendNewState(self,RewardState):
        self.RewStates.append(RewardState)
        self.TransitionMatrix.append([])

    def pvRetIndex(self,RewardState):
        tr.call("clsAgent.pvRetIndex")
        for i in range(len(self.RewStates)):
            if RewardState.state == self.RewStates[i].state:
                return i
        self.pvAppendNewState(RewardState)
        return len(self.RewStates)-1 #return index

    def pvExtendTransitionMatrix(self): #Type StateTransition: (1,3). From 1 to 3
        tr.call("clsAgent.pvExtendTransitionMatrix")
        if len (self.SequenceRewards)>1: #start from 2nd step
            FromIdx,_ = self.SequenceRewards[-2]
            ToIdx,_ = self.SequenceRewards[-1]
            if not ToIdx in self.TransitionMatrix[FromIdx]:
                self.TransitionMatrix[FromIdx].append(ToIdx)




