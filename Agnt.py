import random
import numpy as np
from numpy.random import choice as npchoice
import pandas as pd

import Sequence as Seq
import States as Stt
import QModel
import Constraints
# ==============================================================================
# -- API -----------------------------------------------------------------------
# ============================================================================== 

class clsAgent:
#Public:
    def __init__(self, actionlist, featurelist = []):
        # own:
        self.States = Stt.clsStatesTable()
        self.StatesAnchor = Stt.clsStatesTable()
        self.Sequence = Seq.clsSequence()
        self.QModel = QModel.clsQModel(actionlist, featurelist)
        self.Constraints = Constraints.clsConstraints(actionlist)
        self.actions = actionlist
        self.features = featurelist
        # parameter:
        self.epsilon = [1.0]
        self.buffer = 10**5
        self.alpha = 0.1
        self.gamma = 1
        # self.batch = 10**5
        self.Mode = "Offline"
        # random set
        self.randIdx = 0
        self.rand1000 = list(range(1000));random.shuffle(self.rand1000)
            
    def SetParameter(self, parameter, value):
        return self.xSetParameter(parameter,value)

    def PerceiveEnv(self,state,reward):
        return self.xPerceiveEnv(state,reward)

    def NextAction(self, action = "\_(ツ)_/"):
        return self.xNextAction(action = action)

    def RetQ(self, state, rund = 1):
        return self.xRetQ(state, rund = rund)

    def TrainQ(self, Bellman_Iterations):
        return self.xTrainQ(Bellman_Iterations)

    def Reset(self, InclParameter = False):
        return self.xReset(InclParameter= InclParameter)

# ==============================================================================
# -- SetParameter --------------------------------------------------------------
# ==============================================================================   
    def xSetParameter(self, parameter, value):
        assert len(parameter)>0 and len(parameter)== len(value)
        for i in range(len(parameter)):
            if parameter[i] == "alpha":self.alpha = value[i]
            if parameter[i] == "gamma":self.gamma = value[i]
            if parameter[i] == "epsilon":
                assert len(value[i]) == 1 or len(value[i]) == len(self.actions)+1
                if len(value[i]) > 1:
                    assert sum(value[i]) == 1 + value[i][0]
                self.epsilon = value[i]
            if parameter[i] == "buffer":
                self.buffer = value[i]
                self._UpdateSequenceLen()
            if parameter[i] == "Mode":
                assert (value[i] == "Online" or value[i] == "Offline" or value[i] == "Silent")
                self.Mode = value[i]

    def _UpdateSequenceLen(self):
        # if self.buffer < self.Sequence.len:
        #     l = len(self.Sequence)
        #     del self.Sequence[0:l-self.buffer]
        pass
# ==============================================================================
# -- PerceiveEnv ---------------------------------------------------------------
# ============================================================================== 
    def xPerceiveEnv(self,state,reward):
        if self.Mode == "Silent":
            try:
                self.Sequence[0].state0 = state
                self.Sequence[0].reward = reward
            except:
                self.Sequence.AddStep(state,reward)
        if self.Mode == "Offline" or self.Mode == "Online":
            self.Sequence.AddStep(state,reward)
            self.States.Update(state,reward,[0]*len(self.actions))
            if state[-1] == 1:
                self.StatesAnchor.Update(state,Q=[reward]*len(self.actions))
        if self.Mode == "Online" and self.QModel.batch == 0:
            try:
                self._BellmanUpdate(self.Sequence[-2])
            except:
                pass
        return       

# ==============================================================================
# -- Reset ----------------------------------------------------------------
# ============================================================================== 

    def xReset(self, InclParameter = False):
        self.States.Reset()
        self.StatesAnchor.Reset()
        self.Sequence.Reset()
        if InclParameter:
            self.alpha = 0.1
            self.gamma = 1.0
            self.epsilon = [1.0]
            self.buffer = 10**5
            self.batch = 10**5
            self.Mode = "Online"

# ==============================================================================
# -- NextAction ----------------------------------------------------------------
# ==============================================================================  
    def xNextAction(self, action = "\_(ツ)_/"):
        if self.Sequence[-1].state1[-1] == 1 or self.Sequence[0].state0[-1] == 1:
            return None
        if action == "\_(ツ)_/":
            if self._IsRandomAction():
                act = self._RetRandomAction()
            else:
                act = self._RetGreedyAction()
        else:
            act = action

        if not act == None:
            assert act in self.actions 
            self.Sequence.SetAction(-1, act, self.actions.index(act))
        return act

    def _NextRand1000(self):
        self.randIdx +=1
        if self.randIdx == 1000: self.randIdx = 0
        return self.rand1000[self.randIdx]

    
    def _IsRandomAction(self):
        rand = self._NextRand1000()/1000
        if rand <= self.epsilon[0]: # Random (x-case epsilon == 1)
            return True
        else:
            return False

    def _RetRandomAction(self):
        if len(self.epsilon)>1:
            return npchoice(a=self.actions,size=1,p=self.epsilon[1:])[0]
        else:
            return random.choice(self.actions)

    def _RetGreedyAction(self):
        Q = self.xRetQ(self.Sequence[-1].state0)
        if Q == None:
            return None
        if np.array(Q).ndim == 2:
            Q = Q[0]
        return self.actions[Q.index(max(Q))]
    
# ==============================================================================
# -- TrainQ --------------------------------------------------------------------
# ==============================================================================
    def xTrainQ(self, Bellman_Iterations):
        for k in range(Bellman_Iterations):
            CopyStates = Stt.clsStatesTable(CopyFrom=self.States)
            for i in range(self.Sequence.len-1):
                self._BellmanUpdate(self.Sequence[i])
            if CopyStates.AsList(SRQ="Q") == self.States.AsList(SRQ="Q"):
                print("No further progress in Q Training. Stopped at iteration: " + str(k))
                break

    def _BellmanUpdate(self, step):
        if step == None:
            return
        s0 = step.state0
        s1 = step.state1
        r = step.reward
        a = step.actionInt
        self.States[s0].Q[a] = self.States[s0].Q[a] + self.alpha*(r +self.gamma*max(self.States[s1].Q) - self.States[s0].Q[a])
        if step.state1[-1]==1:
            s1 = step.state1
            self.States[s1].Q = [step.totalreward]*4
# ==============================================================================
# -- RetQ--------------------------------------------------------------------
# ==============================================================================
    
    def xRetQ(self,state, rund = 1):
        if self.QModel.batch == 0:
            ret = self.States[state]
            if ret == None:
                return None
            else:
                return ret.Q
        else:
            return self.QModel.Predict([state], rund)
