import pathlib
import pandas as pd
import random

import NN

class typState:
    def __init__(self, features = [] , reward = 0.0, Q = [], value= 0.0 , visited = 0):
        self.features = features
        self.reward = reward
        self.Q = Q
        self.value = value 
        self.visited = visited

class typStep:
    def __init__(self, state0 = [0], state1 = [0] , reward = 0.0, totalreward = 0.0, Q = [], actionInt = -1, action = "", rg = "r"):
        self.state0 = state0
        self.state1 = state1
        self.reward = reward
        self.totalreward = totalreward
        self.actionInt = actionInt
        self.action = action
        self.rg = rg

class clsAgent:
#Public:
    def __init__(self, actionlist):
        self.States = []         #Typ: typState. Remembers all (unique) states visited.
        self.Sequence = []
        self.actions = actionlist
        self.LastAction = ""
        self.LastActionType = "" #g,r (greedy, random)
        self.LastActionInt = -1
        self.Nterminal = 0

        self.alpha = .2
        self.gamma = 1
        self.rand = list(range(1000))
        random.shuffle(self.rand)
        self.randIdx = 0

        self.batchsize = 64
        self.SequenceSample = []
        self.SequenceSamplePD = pd.DataFrame()

#####################################################################
# Public                                                            #
#####################################################################
    
    def perceiveState(self, state, reward, learn = True, tabular = True):
        self._SequenceAppend(state, reward)
        self._UpdateNumTerminal()

        if tabular == True:
            self._UpdateStates(state, reward)
            self._UpdateQOfLastSequenceStep(self.alpha, self.gamma)
        else:
            if len(self.Sequence) > self.batchsize:
                self._NewSequenceSample()
                self.SequenceSamplePD = self._ReturnPDFromSequence(self.SequenceSample)


    def nextAction(self,epsilon = 0):
        if self.Sequence[-1].state1[-1] == 1:
            self.LastActionType = ""
            self.LastAction = ""
            self.LastActionInt = -1
            return self.actions[0] # Update Env before returning  ""

        rand = self._NextRandInt()
        if rand < epsilon: # Random (x-case epsilon == 1)
            self.LastActionType = "r"
            self.LastAction = random.choice(self.actions)
            self.LastActionInt =self.actions.index(self.LastAction)
        else: # Greedy (x-case epsilon == 0)
            self.LastActionType = "g"
            statefeatures = [state.features for state in self.States]
            s = statefeatures.index(self.Sequence[-1].state1)
            self.LastActionInt = self.States[s].Q.index(max(self.States[s].Q))
            self.LastAction = self.actions[self.LastActionInt]     
        return self.LastAction

    def SortStates(self):
        # Bubble Sort
        n = len(self.States)
        for i in range(n):
            for j in range(0, n-i-1):
                if self.States[j].features > self.States[j+1].features:
                    self.States[j], self.States[j+1] = self.States[j+1], self.States[j]

    def RoundQ(self, numdec):
        for state in self.States:
            for j in range(len(state.Q)):
                state.Q[j] = round(state.Q[j],numdec)

    def EchoPrint(self,afterNSteps = 10, prefix = ""):
        if self.Nterminal%afterNSteps == 0:
            print(prefix + "step: " + str(self.Nterminal),end ='\r')

    def setLearningParameter(self,alpha, gamma):
        self.alpha = alpha
        self.gamma = gamma

    def setModelTrainingParameter(self, batchsize = 64, replaybuffer = 1e5):
        self.batchsize = batchsize
        self.buffer = replaybuffer
    # def SetModel(self, featurelist, NLayer = 1, Noutputs = 1):
    #     self.Model = NN.clsNN(len(featurelist)+len(self.actionlist), NLayer, Noutputs)

#####################################################################
# Private                                                           #
#####################################################################

    def _NextRandInt(self):
        # Get Next Random Number from list
        self.randIdx +=1
        if self.randIdx == 1000: 
            self.randIdx = 0
        return self.rand[self.randIdx]/1000

    def _SequenceAppend(self,featState,reward):#MOHI
        if len(self.Sequence) == 0 or self.Sequence[-1].state1[-1] == 1: 
            totalrew_  = 0
            state0 = [0]
        else:
            totalrew_ = self.Sequence[-1].totalreward
            state0 = self.Sequence[-1].state1

        self.Sequence.append(typStep(state0 = state0, actionInt = self.LastActionInt, action = self.LastAction, \
            state1 = featState, reward = reward, totalreward = totalrew_ + reward, rg = self.LastActionType))

    def _UpdateStates(self,state, reward):
        for i in range(len(self.States)):
            if state == self.States[i].features:
                self.States[i].visited +=1
                return
        self.States.append(typState(features = state, reward = reward))
        self.States[-1].Q = [0]*len(self.actions)
        self.States[-1].visited +=1
    
    def _UpdateQOfLastSequenceStep(self, alpha, gamma):
        if len(self.Sequence)<3: 
            return
        state1 = self.Sequence[-1].state1; s1 = [state.features for state in self.States].index(state1)
        state = self.Sequence[-2].state1; s = [state.features for state in self.States].index(state)
        r = self.Sequence[-1].reward
        a = self.Sequence[-1].actionInt

        alpha = max(1/self.States[s1].visited,self.alpha)
        if self.States[s].features[-1] == 0: # non terminal
            self.States[s].Q[a] = self.States[s].Q[a] + alpha*(r +gamma*max(self.States[s1].Q) - self.States[s].Q[a])

    def _UpdateNumTerminal(self):
        if len(self.Sequence) > 0:
            if self.Sequence[-1].state1[-1] == 1: 
                self.Nterminal +=1

    def _ReturnPDFromSequence(self, Sequence, SplitState = False, SplitActions = False):
        sample = self._ReturnPandasFromSequence(Sequence)
        
        if SplitState == True:
            sample["0state"] = [str(step.state0).replace("[","").replace("]","") for step in Sequence]
            new = sample["0state"].str.split(",", expand = True).astype('float')
            for i in range(len(new.columns)-1):
                sample["0feat"+str(i)] = new[i]
            sample["0terminal"]= new[len(new.columns)-1]

        if SplitActions == True:
            for i in range(len(self.actions)):
                sample["blaction"+str(i)] = 0
            for index, row in sample.iterrows():
                for i in range(len(self.actions)):
                    if row["actionInt"] == i: 
                        sample.at[index, "blaction"+str(i)] = 1

        if SplitState == True:
            sample["1state"] = [str(step.state1).replace("[","").replace("]","") for step in Sequence]
            new = sample["1state"].str.split(",", expand = True).astype('float')
            for i in range(len(new.columns)-1):
                sample["1feat"+str(i)] = new[i]
            sample["1terminal"]= new[len(new.columns)-1]

        return sample

    def _ReturnPandasFromSequence(self,Sequence):
        sample = pd.DataFrame()
        sample["0state"] = [step.state0 for step in Sequence]
        sample["actionInt"] = [step.actionInt for step in Sequence]
        sample["action"] = [step.action for step in Sequence]
        sample["1state"] = [step.state1 for step in Sequence]
        sample["reward"] = [step.reward for step in Sequence]
        sample["tot reward"] = [step.totalreward for step in Sequence]
        sample["rnd_grd"] = [step.rg for step in Sequence]
        return sample

    def _NewSequenceSample(self):
        idx = list(range(len(self.Sequence)-1)); random.shuffle(idx)
        self.SequenceSample = []
        for i in range(self.batchsize):
            self.SequenceSample.append(self.Sequence[idx[i]])

    def _ReturnColsByKeywords(self, dataframe, keywords):
        tmp = pd.DataFrame({})
        for col in dataframe.columns:
            for keyword in keywords:
                if col.find(keyword)>-1:
                    tmp[col] = dataframe[col]
        return tmp

    def ping(self):
        print("Agent here")

#####################################################################
# IMPORT AND EXPORT                                                 #
#####################################################################

    def ImportQ(self,dataset_path, ):
        self.States = []
        QImport = pd.read_csv(dataset_path, skiprows = 0, na_values = "?", \
        comment='\t', sep="|", skipinitialspace=True, error_bad_lines=False)

        for col, _ in QImport.iterrows():
            features = QImport.at[col, "State"].replace("[","").replace("]","").split(",")
            Q = QImport.at[col, "Q"].replace("[","").replace("]","").split(",")
            visited = QImport.at[col, "visited"]
            for i in range(len(features)): features[i] = int(features[i])
            for i in range(len(Q)): Q[i] = float(Q[i])
            self.States.append(typState(features = features, Q = Q,visited = visited))

    def ExportQtoCSV(self, path, SplitCols = False):
        self.RoundQ(2)
        Qpd = pd.DataFrame()
        Qpd["State"] = [state.features for state in self.States]
        Qpd["Q"] = [state.Q for state in self.States]
        Qpd["visited"] = [state.visited for state in self.States]
        if SplitCols == False:
            # WRITE TO FILE:
            Qpd.to_csv(path, sep='|', encoding='utf-8', index = False)
        
        if SplitCols == True:
            Qlistpd = pd.DataFrame()
            new = pd.DataFrame(Qpd["State"].values.tolist())  
            for i in range(len(new.columns)-1):
                Qlistpd["Statefeat"+str(i)] = new[i]
            Qlistpd["terminal"] = new[len(new.columns)-1]
            new = pd.DataFrame(Qpd["Q"].values.tolist(), columns = self.actions)  
            Qlistpd = pd.concat([Qlistpd, new], axis=1, sort=False)
            Qlistpd["visited"] = Qpd["visited"]
            # WRITE TO FILE:
            Qlistpd.to_csv(path, sep='|', encoding='utf-8', index = False)

    def ExportSeqtoCSV(self, path, SplitCols = False):
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
        Seqpd["tot reward"] = [step.totalreward for step in self.Sequence]
        Seqpd["rnd_grd"] = [step.rg for step in self.Sequence]

        #Create 100evenly distributed indices from 0 to n terminal states-> arr
        arr0 = []; arr1 = []; arrTerminal = []
        for i in range(len(self.Sequence)):
            if self.Sequence[i].state1[-1] == 1:
                arrTerminal.append(i)
        for i in range(99): 
            idx = int(i * len(arrTerminal)/99)
            arr0.append(arrTerminal[idx])
            arr1.append(arrTerminal[idx+1])
        
        #Mark all lines between index arr[i] - arr[i+1]
        Seqpd["mark"] = 0
        for i in range(99):
            for j in range(arr0[i]+1, arr1[i]+1):
                Seqpd.at[j, "mark"] = 1
        
        # Filter data frame
        Seq100pd =  Seqpd[Seqpd["mark"] == 1]
        Seq100pd = Seq100pd.drop(columns = ["mark"])

        # WRITE TO FILE:
        Seq100pd.to_csv(path, sep='|', encoding='utf-8', index = False)
      