# ==============================================================================
# -- API -----------------------------------------------------------------------
#
# Agnt.clsAgent(["jump", "run"],["world","level","terminal"])   | Initiate Agent
# Agt.SetParameter(["alpha","gamma"],[0.8,0.99])                | Set Agents parameter
# Agt.PerceiveEnv([2,"street",0.1,0],-2)                        | Agent State and Reward Preception. Last index of list:
#                                                               | 0 = non terminal; 1 = terminal state
# Agt.Reset()                                                   | Delete Agt internal states and sequeces


import random
from numpy.random import choice as npchoice

class typState:
    def __init__(self, features = [] , reward = 0.0, Q = []):
        self.features = features
        self.reward = [reward, reward]
        self.Q = Q
        self.QUpdates = 0

class typStep:
    def __init__(self, state0 = [0], state1 = [0] , reward = 0, totalreward = 0.0, actionInt = -1, action = "", rg = "r"):
        self.state0 = state0
        self.state1 = state1
        self.reward = reward
        self.totalreward = totalreward
        self.actionInt = actionInt
        self.action = action
        self.rg = rg
        self.StepSampled = 0

class clsAgent:
#Public:
    def __init__(self, actionlist, featurelist = []):
        self.States = []         #Typ: typState. Remembers all (unique) states qUpdated.
        self.Sequence = []
        self.TerminalRewards = []       # idx, reward
        self.actions = actionlist
        self.actionsConstrains = actionlist
        self.features = featurelist
        self.Nterminal = 0

        self.alpha = .1
        self.gamma = 1.0
        self.epsilon = 1.0
        self.randIdx = 0
        self.rand1000 = list(range(1000));random.shuffle(self.rand1000)
        self.FitDQNStepSize = 10
        self.DQNCounter = 0
        self.ModelAlpha = 0.001

        self.batchsize = 0
        self.SequenceSampleLIST = []
        self.SequenceSampleLISTXA = []
        self.SequenceSampleLISTX = []
        self.SequenceSampleTYP = []

# ==============================================================================
# -- Init ----------------------------------------------------------------------
# ==============================================================================   
    def SetParameter(self, parameter = [],value = []):
        assert len(parameter)>0 and len(parameter)== len(value)
        for i in range(len(parameter)):
            if parameter[i] == "alpha":self.alpha = value[i]
            if parameter[i] == "gamma":self.gamma = value[i]
            if parameter[i] == "epsilon":
                assert len(value[i]) == 1 or len(value[i]) == len(self.actions)+1
                if len(value[i]) > 1:
                    assert sum(value[i]) == 1 + value[i][0]
                self.epsilon = value[i]


# ==============================================================================
# -- Perception ----------------------------------------------------------------
# ============================================================================== 
    def PerceiveEnv(self,state,reward):
        self._UpdateSequence(state)
        self._UpdateStatesTable(state)
        self._RewardToStep(reward)
        # self._UpdateNumTerminal()

        
    def _UpdateSequence(self,featState):
        if len(self.Sequence)==0:
            self.Sequence.append(typStep(state0 = featState))
            return

        if featState[-1] == 0:
            self.Sequence.append(typStep(state0 = featState))
            if self.Sequence[-2].state1 == [0]:self.Sequence[-2].state1 = featState 
        else:
            self.Sequence[-1].state1 = featState
    
    def _UpdateStatesTable(self,state):
        for i in range(len(self.States)):
             if state == self.States[i].features: 
                return
        self.States.append(typState(features = state, Q =[0]*len(self.actions)))

    def _RewardToStep(self,reward):
        self.Sequence[-1].reward = reward
        self.Sequence[-1].totalreward = \
        self.Sequence[-2].totalreward + reward if len(self.Sequence) > 1 else reward


    def Reset(self):
        self.States = []
        self.Sequence = []

# ==============================================================================
# -- Return ---------------------------------------------------------------------
# ==============================================================================     
    def Info(self):
        retStr = "Actions: " + str(self.actions) +"\n"
        retStr += "State Features: " + str(self.features)
        return retStr

# ==============================================================================
# -- Action --------------------------------------------------------------------s
# ==============================================================================  
    def NextAction(self):
        rand = self._NextRand1000()/1000
        if rand <= self.epsilon[0]: # Random (x-case epsilon == 1)
            if len(self.epsilon)>1:
                return npchoice(a=self.actions,size=1,p=self.epsilon[1:])[0]
            else:
                return random.choice(self.actions)

    def _NextRand1000(self):
        self.randIdx +=1
        if self.randIdx == 1000: self.randIdx = 0
        return self.rand1000[self.randIdx]