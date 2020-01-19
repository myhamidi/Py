import pandas as pd
import random

class typStep:
    def __init__(self, state0 = [0], state1 = [0] , reward = 0, totalreward = 0.0, actionInt = -1, action = "", rg = "r"):
        self.state0 = state0
        self.state1 = state1
        self.reward = reward                # reward of state0
        self.totalreward = totalreward      # totalreward of state0. if terminal: reward of state1
        self.actionInt = actionInt
        self.action = action
        self.rg = rg
        self.StepSampled = 0

# ==============================================================================
# -- API -----------------------------------------------------------------------
# ============================================================================== 

class clsSequence:
    def __init__(self):
        self.Steps = []
        self.len = 0
        self.Nterminal = 0
        self.buffer = 10e5

    def __getitem__(self,idx):
        try:
            return self.Steps[idx]
        except:
            return None

    def AddStep(self, State, Reward):
        return self.xAddStep( State, Reward)

    def SetAction(self, StepIdx = -1, Action = "", ActionInt = -1):
        return self.xSetAction(StepIdx=StepIdx, Action=Action, ActionInt = ActionInt)

    def Export(self, path, SplitCols = False, nthEpoch = 100):
        return self.xExporttoCSV(path, SplitCols=SplitCols, nthEpoch = nthEpoch)

    def Import(self, path, ResetSteps = True):
        return self.xImportFromCSV(path, ResetSteps = ResetSteps)

    def ReturnIdx(self, LastValue=1):
        return self.xReturnIdx(LastValue=LastValue)

    def ReturnStates(self, LastValue=1):
        return self.xReturnStates(LastValue=LastValue)

    def ReturnSample(self, size = 0, idxs = []):
        return self.xReturnSample(size, idxs)

    def AsList(self,multi= 1):
        return self.xAsList(multi=multi)
    
    def Sort(self):
        return self.xSort()

    def RemoveDuplicates(self):
        return self.xRemoveDuplicates()

    def Reset(self):
        return self.xReset()

# ==============================================================================
# -- AddStep -------------------------------------------------------------------
# ============================================================================== 

    def xAddStep(self, State, Reward):
        if State[-1]==1:
            self.Nterminal +=1
        if len(self.Steps)==0:
            self._AppendFirstStep(State, Reward)
            return
        if State[-1]==1:
            self._AppendTerminalStep(State, Reward)
            return
        if self.Steps[-1].state1[-1] == 1:
            self._AppendFirstStep(State, Reward)
            return
        self._AppendNextStep(State, Reward)

    def _AppendFirstStep(self, State, Reward):
        self.Steps.append(typStep(state0 = State, reward = Reward, totalreward = Reward))
        self.len +=1

    def _AppendNextStep(self, State, Reward):
        self.Steps[-1].state1 = State
        self.Steps.append(typStep(state0 = State, reward = Reward))
        self.len +=1
        self.Steps[-1].totalreward = self.Steps[-2].totalreward + Reward 

    def _AppendTerminalStep(self, State, Reward):
        self.Steps[-1].state1 = State
        self.Steps[-1].totalreward = Reward

# ==============================================================================
# -- SetAction -----------------------------------------------------------------
# ============================================================================== 

    def xSetAction(self, StepIdx = -1, Action = "", ActionInt = -1):
        self.Steps[StepIdx].action = Action
        self.Steps[StepIdx].actionInt = ActionInt

# ==============================================================================
# -- Return --------------------------------------------------------------------
# ============================================================================== 

    def xReturnIdx(self, LastValue=None):
        if LastValue == None:
            return [i for i in range(len(self.Steps))]

        ret = []; arr = []
        for i in range(len(self.Steps)):
            if self.Steps[i].state0[-1] == LastValue:    
                ret.append(i)
            if self.Steps[i].state1[-1] == LastValue:    
                if not i in ret:
                    ret.append(i)  
        return ret

    def xReturnStates(self, LastValue=None):
        ret = []
        if LastValue == None:
            for i in range(len(self.Steps)):
                if not self.Steps[i].state0 in ret:
                    ret.append(self.Steps[i].state0)
                if not self.Steps[i].state1 in ret:
                    if len(self.Steps[i].state1) > 1:
                        ret.append(self.Steps[i].state1)
        else:
            for i in range(len(self.Steps)):
                if self.Steps[i].state0[-1] == LastValue:
                    if not self.Steps[i].state0 in ret:    
                        ret.append(self.Steps[i].state0)    	
                if self.Steps[i].state1[-1] == LastValue:    
                    if not self.Steps[i].state1 in ret:
                        if len(self.Steps[i].state1) > 1:
                            ret.append(self.Steps[i].state1)        
        return ret

    def xReturnSample(self, size = 0, idxs = []):
        Sample = clsSequence()
        if idxs == [] and not size == 0:
            if self.len <= size:
                return self
            else:      
                Sample.Steps = random.choices(self.Steps[:-1], k=size)
        if not idxs == [] and size == 0:
            for i in idxs:
                Sample.Steps.append(self.Steps[i])
        for step in Sample.Steps:
            Sample.len +=1
            try:
                if step.state1[-1]==1:
                    Sample.Nterminal +=1
            except:
                Sample.Nterminal = Sample.Nterminal
        return Sample

    def xAsList(self, multi= 1):
        S0 = [step.state0[:-1] for step in self.Steps for i in range(multi)]
        S1 = [step.state1[:-1] for step in self.Steps for i in range(multi)]
        AI = [step.actionInt for step in self.Steps for i in range(multi)]
        RW = [step.reward for step in self.Steps for i in range(multi)]
        TR = [step.totalreward for step in self.Steps for i in range(multi)]
        return (S0, S1, AI, RW, TR)
# ==============================================================================
# -- Reset ---------------------------------------------------------------------
# ==============================================================================
    
    def xReset(self):
        self.Steps = []
        self.len = 0 
        self. Nterminal = 0

# ==============================================================================
# -- Sort ----------------------------------------------------------------
# ============================================================================== 

    def xSort(self):
        # Bubble Sort
        n = len(self.Steps)
        for i in range(n):
            for j in range(0, n-i-1):
                if self.Steps[j].state0 + [self.Steps[j].actionInt] > self.Steps[j+1].state0 + [self.Steps[j+1].actionInt]:
                    self.Steps[j], self.Steps[j+1] = self.Steps[j+1], self.Steps[j]
        return

    def xRemoveDuplicates(self):
        arr = []
        for step in self.Steps:
            if not self._isStepInStepList(step,arr):
                arr.append(step)
        self.Steps = arr
        self.len = len(arr)
        return

    def _isStepInStepList(self, step, steplist):
        for stp in steplist:
            if stp.state0 + [stp.actionInt] + [stp.reward] == \
            step.state0 + [step.actionInt] + [step.reward]:
                return True
        return False

# ==============================================================================
# -- ExporttoCSV ---------------------------------------------------------------
# ==============================================================================
        
    def xExporttoCSV(self, path, SplitCols = False, nthEpoch = 100):
        nthEpoch = nthEpoch-1
        # Create full size data frame
        Seqpd = pd.DataFrame()
        Seqpd["state0"] = [step.state0 for step in self.Steps]
        Seqpd["actionInt"] = [step.actionInt for step in self.Steps]
        Seqpd["action"] = [step.action for step in self.Steps]        
        Seqpd["state1"] = [step.state1 for step in self.Steps]
        Seqpd["reward"] = [step.reward for step in self.Steps]
        Seqpd["treward"] = [step.totalreward for step in self.Steps]
        Seqpd["rnd_gd"] = [step.rg for step in self.Steps]
        Seqpd["sampled"] = [step.StepSampled for step in self.Steps]

        #Create 100evenly distributed indices from 0 to n terminal states-> arr
        arr0 = []; arr1 = []; SeqidxTerminals = []
        for i in range(len(self.Steps)):
            if self.Steps[i].state1[-1] == 1:
                SeqidxTerminals.append(i)
        # if len(SeqidxTerminals) > nthEpoch:
            # for i in range(nthEpoch): 
            #     idx = int(i * len(SeqidxTerminals)/nthEpoch)
            #     arr0.append(SeqidxTerminals[idx])
            #     arr1.append(SeqidxTerminals[idx+1])

            # #Mark all lines between index arr[i] - arr[i+1]
            # Seqpd["mark"] = 0
            # for i in range(nthEpoch):
            #     for j in range(arr0[i]+1, arr1[i]+1):
            #         Seqpd.at[j, "mark"] = 1
                
            # # Filter data frame
            # Seq100pd =  Seqpd[Seqpd["mark"] == 1]
            # Seq100pd = Seq100pd.drop(columns = ["mark"])

            # # WRITE TO FILE:
            # Seq100pd.to_csv(path, sep='|', encoding='utf-8', index = False)
        # else:
        Seqpd.to_csv(path, sep='|', encoding='utf-8', index = False)

    def xImportFromCSV(self, path, ResetSteps = True):
        if ResetSteps: 
            self.Steps = []
        SeqImport = pd.read_csv(path, skiprows = 0, na_values = "?", \
        comment='\t', sep="|", skipinitialspace=True, error_bad_lines=False)

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
            self.Steps.append(typStep(state0=state0,state1=state1, \
                reward=r, totalreward=tr, action = a, actionInt = aint, rg= rg))
            self.len+=1
            if state1[-1] == 1:
                self.Nterminal +=1
        return