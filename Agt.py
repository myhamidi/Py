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
        self.SequenceRewards = []   #Typ: (s,r). Remembers the sequence of states and commulative reward at step i
        self.TransitionMatrix = []  #Typ: List of Lists [[],[],...]
        self.actions = actionlist

    def PerceiveState(self,strState,reward):
        tr.call("clsAgent.PerceiveState")
        idx = self.pvRetIndex(strState,reward)
        self.SequenceRewards.append((idx,reward))
        self.pvExtendTransitionMatrix()

    def RetNextAction(self):
        tr.call("clsAgent.RetNextAction")
        return random.choice(self.actions)

    def IntiSequences(self):
        self.SequenceRewards =[]

    def StateIsTerminal(self):
        tr.call("clsAgent.StateIsTerminal")
        if len(self.SequenceRewards) == 0:
            return False
        idx,_ = self.SequenceRewards[-1]
        if self.RewStates[idx].state[-8:] == "terminal":
            return True
        return False

#Private:
    def pvAppendNewState(self,RewardState):
        self.RewStates.append(RewardState)
        self.TransitionMatrix.append([])

    def pvRetIndex(self,strState,reward):
        tr.call("clsAgent.pvRetIndex")
        for i in range(len(self.RewStates)):
            if strState == self.RewStates[i].state:
                return i
        # NewRewSate = typRewState(state,0,0,0)
        self.pvAppendNewState(typRewState(strState,reward,0,0))
        return len(self.RewStates) - 1 #return index

    def pvExtendTransitionMatrix(self): #Type StateTransition: (1,3). From 1 to 3
        tr.call("clsAgent.pvExtendTransitionMatrix")
        if len (self.SequenceRewards)>1: #start from 2nd step
            FromIdx,_ = self.SequenceRewards[-2]
            ToIdx,_ = self.SequenceRewards[-1]
            if not ToIdx in self.TransitionMatrix[FromIdx]:
                self.TransitionMatrix[FromIdx].append(ToIdx)




