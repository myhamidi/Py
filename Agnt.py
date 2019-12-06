# ==============================================================================
# -- API -----------------------------------------------------------------------
#
# Agnt.clsAgent(["jump", "run"],["world","level","terminal"])   | Initiate Agent
# Agt.SetParameter(["alpha","gamma"],[0.8,0.99])                | Set Agents parameter
# Agt.PerceiveEnv([2,"street",0.1,0],-2)                        | Agent State and Reward Preception. Last index of list:
# Agt.NextAction()                                              | next action according to eps-greedy policy
# Agt.Reset()                                                   | Delete Agt internal states and sequeces
# ExportQ(path) / ImportQ(path)                                 | Export Import Q Table
# ExportSeq(path) / ImportSeq(path)                             | Export Import Step Sequence


import random
from numpy.random import choice as npchoice
import pandas as pd

class typState:
    def __init__(self, features = [] , reward = 0.0, Q = [], QUpdates = 0):
        self.features = features
        self.reward = [reward, reward]
        self.Q = Q
        self.QUpdates = QUpdates

class typStep:
    def __init__(self, state0 = [0], state1 = [0] , reward = 0, totalreward = 0.0, actionInt = -1, action = "", rg = "r"):
        self.state0 = state0
        self.state1 = state1
        self.reward = reward                # reward of state0
        self.totalreward = totalreward      # totalreward of state0. if terminal totalreward of state1
        self.actionInt = actionInt
        self.action = action
        self.rg = rg
        self.StepSampled = 0

class clsAgent:
#Public:
    def __init__(self, actionlist, featurelist = []):
        self.States = []         #Typ: typState. Remembers all (unique) states qUpdated.
        self.Sequence = []
        self.actions = actionlist
        self.features = featurelist
        self.Nterminal = 0

        self.alpha = 0.1
        self.gamma = 1.0
        self.epsilon = [1.0]
        self.buffer = 10**5
        self.batch = 10**5
        self.randIdx = 0
        self.rand1000 = list(range(1000));random.shuffle(self.rand1000)

# ==============================================================================
# -- SetParameter --------------------------------------------------------------
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
            if parameter[i] == "buffer":
                self.buffer = value[i]
                self._UpdateSequenceLen()
            if parameter[i] == "batch":
                self.batch = value[i]

    def _UpdateSequenceLen(self):
        if self.buffer < len(self.Sequence):
            l = len(self.Sequence)
            del self.Sequence[0:l-self.buffer]

# ==============================================================================
# -- PerceiveEnv ---------------------------------------------------------------
# ============================================================================== 
    def PerceiveEnv(self,state,reward):
        self._UpdateSequence(state)
        self._UpdateStatesTable(state)
        self._UpdateNterminal(state)
        self._RewardToStep(reward)

    def _UpdateNterminal(self, state):
            if state[-1] == 1: self.Nterminal +=1
        
    def _UpdateSequence(self,featState):
        if len(self.Sequence)==0:
            self.Sequence.append(typStep(state0 = featState))
            return
        if featState[-1] == 1:
            self.Sequence[-1].state1 = featState
            return
        if len(self.Sequence) >= self.buffer:
            del self.Sequence[0]

        self.Sequence.append(typStep(state0 = featState))
        if self.Sequence[-2].state1 == [0]:self.Sequence[-2].state1 = featState 
            
    
    def _UpdateStatesTable(self,state):
        for i in range(len(self.States)):
             if state == self.States[i].features: 
                return
        self.States.append(typState(features = state, Q =[0]*len(self.actions)))

# ==============================================================================
# -- _Reward ----------------------------------------------------------------
# ============================================================================== 

    def _RewardToStep(self,reward):
        if self.Sequence[-1].state1[-1] == 0:
            self._SetRewardToStep(reward)
        if self.Sequence[-1].state1[-1] == 1:
            self._SetRewardToTerminalState(reward)

        self.Sequence[-1].totalreward = self._RetTotalReward(reward)

    def _SetRewardToStep(self,reward):
        self.Sequence[-1].reward = reward 
    
    def _SetRewardToTerminalState(self,reward):
        sIdx = self._retStatesIdx(self.Sequence[-1].state1)
        self.States[sIdx].reward = reward
    
    def _RetTotalReward(self,reward):
        if len(self.Sequence) == 1:
            return reward
        if self.Sequence[-2].state1[-1] == 1:
            return reward
        if self.Sequence[-1].state1[-1] == 1:
            return reward 
        return self.Sequence[-2].totalreward + reward 

# ==============================================================================
# -- Sort ----------------------------------------------------------------
# ============================================================================== 
    def SortStates(self):
        # Bubble Sort
        n = len(self.States)
        for i in range(n):
            for j in range(0, n-i-1):
                if self.States[j].features > self.States[j+1].features:
                    self.States[j], self.States[j+1] = self.States[j+1], self.States[j]
        return

    def SortSequence(self):
        # Bubble Sort
        n = len(self.Sequence)
        for i in range(n):
            for j in range(0, n-i-1):
                if self.Sequence[j].state0 + [self.Sequence[j].actionInt] > self.Sequence[j+1].state0 + [self.Sequence[j+1].actionInt]:
                    self.Sequence[j], self.Sequence[j+1] = self.Sequence[j+1], self.Sequence[j]
        return

    def RemoveDuplicateSteps(self):
        arr = []
        for step in self.Sequence:
            if not self._isStepInStepList(step,arr):
                arr.append(step)
        self.Sequence = arr

    def _isStepInStepList(self, step, steplist):
        for stp in steplist:
            if stp.state0 + [stp.actionInt] + [stp.reward] == \
                step.state0 + [step.actionInt] + [step.reward]:
                return True
        return False

# ==============================================================================
# -- Reset ----------------------------------------------------------------
# ============================================================================== 

    def Reset(self):
        self.States = []
        self.Sequence = []
        self.Nterminal = 0

# ==============================================================================
# -- NextAction ----------------------------------------------------------------
# ==============================================================================  
    def NextAction(self, action = "\_(ツ)_/"):
        if self.Sequence[-1].state1[-1] == 1:
            return ""
        if action == "\_(ツ)_/":
            retNextAction = self._RetRandomAction() if self._NextActionIsRandom() else self.actions[0]
        else:
            assert self.actions.index(action)>-1
            retNextAction = action 
        self._SetActionToLastStep(retNextAction)
        return retNextAction

    def _NextRand1000(self):
        self.randIdx +=1
        if self.randIdx == 1000: self.randIdx = 0
        return self.rand1000[self.randIdx]

    def _RetRandomAction(self):
        if len(self.epsilon)>1:
            return npchoice(a=self.actions,size=1,p=self.epsilon[1:])[0]
        else:
            return random.choice(self.actions)

    def _SetActionToLastStep(self,action):
        self.Sequence[-1].action = action
        self.Sequence[-1].actionInt = self.actions.index(action)
    
    def _NextActionIsRandom(self):
        rand = self._NextRand1000()/1000
        if rand <= self.epsilon[0]: # Random (x-case epsilon == 1)
            return True
        else:
            return False
# ==============================================================================
# -- Basis --------------------------------------------------------------------
# ==============================================================================

    def _retStatesIdx(self,state):
        for i in range(len(self.States)):
            if self.States[i].features == state:
                return i


# ==============================================================================
# -- Import --------------------------------------------------------------------
# ==============================================================================
    def ImportQ(self,dataset_path, ResetStates = True, CompareMode = False):
        if CompareMode:
            self.StatesCopy = []
        else:
            if ResetStates:self.States = []
        QImport = pd.read_csv(dataset_path, skiprows = 0, na_values = "?", \
        comment='\t', sep="|", skipinitialspace=True, error_bad_lines=False)

        for col, _ in QImport.iterrows():
            features = QImport.at[col, "State"].replace("[","").replace("]","").split(",")
            Q = QImport.at[col, "Q"].replace("[","").replace("]","").split(",")
            QUpdates = QImport.at[col, "QUpdates"]
            for i in range(len(features)): features[i] = float(features[i]); features[-1] = int(features[-1])
            for i in range(len(Q)): Q[i] = float(Q[i])
            if CompareMode:
                self.StatesCopy.append(typState(features = features, Q = Q, QUpdates = QUpdates))
            else:
                self.States.append(typState(features = features, Q = Q, QUpdates = QUpdates))

        if CompareMode:
            for i in range(len(self.States)):
                if not self.States[i].Q == self.StatesCopy[i].Q:
                    return i+1
            return 0

    def ImportSeq(self,dataset_path, ResetSequence = True):
        if ResetSequence:self.Sequence = []
        SeqImport = pd.read_csv(dataset_path, skiprows = 0, na_values = "?", \
        comment='\t', sep="|", skipinitialspace=True, error_bad_lines=False)

        #Rebuild Seq
        for col, _ in SeqImport.iterrows():
            state0 = SeqImport.at[col, "state0"].replace("[","").replace("]","").split(",")
            state1 = SeqImport.at[col, "state1"].replace("[","").replace("]","").split(",")
            r = float(SeqImport.at[col, "reward"])
            tr = SeqImport.at[col, "treward"]
            a = SeqImport.at[col, "action"]
            aint = int(SeqImport.at[col, "actionInt"])
            rg = SeqImport.at[col, "rnd_gd"]
            for i in range(len(state0)): state0[i] = float(state0[i]); state0[-1] = int(state0[-1])
            for i in range(len(state1)): state1[i] = float(state1[i]); state1[-1] = int(state1[-1])
            self.Sequence.append(typStep(state0=state0,state1=state1, \
                reward=r, totalreward=tr, action = a, actionInt = aint, rg= rg))

        #Rebuild State Table
        for step in self.Sequence:
            self._UpdateStatesTable(step.state0)
            if len(step.state1) > 1:
                self._UpdateStatesTable(step.state1)


# ==============================================================================
# -- Export --------------------------------------------------------------------
# ==============================================================================
    def ExportQtoCSV(self, path, SplitCols = False):
        Qpd = pd.DataFrame()
        Qpd["State"] = [state.features for state in self.States]
        Qpd["Q"] = [state.Q for state in self.States]
        Qpd["QUpdates"] = [state.QUpdates for state in self.States]
        
        if SplitCols:
            Qlistpd = pd.DataFrame()
            new = pd.DataFrame(Qpd["State"].values.tolist())  
            for i in range(len(new.columns)-1):
                Qlistpd["Statefeat"+str(i)] = new[i]
            Qlistpd["terminal"] = new[len(new.columns)-1]
            new = pd.DataFrame(Qpd["Q"].values.tolist(), columns = self.actions)  
            Qlistpd = pd.concat([Qlistpd, new], axis=1, sort=False)
            Qlistpd["QUpdates"] = Qpd["QUpdates"]
            Qlistpd.to_csv(path, sep='|', encoding='utf-8', index = False)
        else:
            Qpd.to_csv(path, sep='|', encoding='utf-8', index = False)

        
    def ExportSeqtoCSV(self, path, SplitCols = False, nthEpoch = 100):
        nthEpoch = nthEpoch-1
        # Create full size data frame
        Seqpd = pd.DataFrame()
        Seqpd["state0"] = [step.state0 for step in self.Sequence]
        Seqpd["actionInt"] = [step.actionInt for step in self.Sequence]
        Seqpd["action"] = [step.action for step in self.Sequence]
        
        if SplitCols == True:
            for i in range(len(self.actions)):
                Seqpd["blaction"+str(i)] = 0
            for index, row in Seqpd.iterrows():
                for i in range(len(self.actions)):
                    if row["actionInt"] == i: 
                        Seqpd.at[index, "blaction"+str(i)] = 1
        
        Seqpd["state1"] = [step.state1 for step in self.Sequence]
        Seqpd["reward"] = [step.reward for step in self.Sequence]
        Seqpd["treward"] = [step.totalreward for step in self.Sequence]
        Seqpd["rnd_gd"] = [step.rg for step in self.Sequence]
        Seqpd["sampled"] = [step.StepSampled for step in self.Sequence]

        #Create 100evenly distributed indices from 0 to n terminal states-> arr
        arr0 = []; arr1 = []; SeqidxTerminals = []
        for i in range(len(self.Sequence)):
            if self.Sequence[i].state0[-1] == 1:
                SeqidxTerminals.append(i)
        if len(SeqidxTerminals) > nthEpoch:
            for i in range(nthEpoch): 
                idx = int(i * len(SeqidxTerminals)/nthEpoch)
                arr0.append(SeqidxTerminals[idx])
                arr1.append(SeqidxTerminals[idx+1])

            #Mark all lines between index arr[i] - arr[i+1]
            Seqpd["mark"] = 0
            for i in range(nthEpoch):
                for j in range(arr0[i]+1, arr1[i]+1):
                    Seqpd.at[j, "mark"] = 1
                
            # Filter data frame
            Seq100pd =  Seqpd[Seqpd["mark"] == 1]
            Seq100pd = Seq100pd.drop(columns = ["mark"])

            # WRITE TO FILE:
            Seq100pd.to_csv(path, sep='|', encoding='utf-8', index = False)
        else:
            Seqpd.to_csv(path, sep='|', encoding='utf-8', index = False)
