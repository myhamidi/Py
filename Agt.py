import pathlib
import pandas as pd
import numpy as np
import random

import NN

class typState:
    def __init__(self, features = [] , reward = 0.0, Q = [], Qapx = [], value= 0.0 , visited = 0):
        self.features = features
        self.reward = reward
        self.Q = Q
        self.Qapx = Qapx
        self.value = value 
        self.visited = visited

class typStep:
    def __init__(self, state0 = [0], state1 = [0] , reward = 0.0, totalreward = 0.0, actionInt = -1, action = "", rg = "r"):
        self.state0 = state0
        self.state1 = state1
        self.reward = reward
        self.totalreward = totalreward
        self.actionInt = actionInt
        self.action = action
        self.rg = rg
        self.sampled = 0

class clsAgent:
#Public:
    def __init__(self, actionlist, featurelist = []):
        self.States = []         #Typ: typState. Remembers all (unique) states visited.
        self.Sequence = []
        self.TerminalRewards = []       # idx, reward
        self.actions = actionlist
        self.actionsConstrains = actionlist
        self.featurelist = featurelist
        self.LastAction = ""
        self.LastActionType = "" #g,r (greedy, random)
        self.LastActionInt = -1
        self.Nterminal = 0

        self.alpha = .2
        self.gamma = 1
        self.rand = list(range(1000))
        random.shuffle(self.rand)
        self.randIdx = 0

        self.batchsize = 0
        self.SequenceSampleLIST = []
        self.SequenceSampleLISTXA = []
        self.SequenceSampleLISTX = []
        self.SequenceSampleTYP = []
        self.SequenceSamplePD = pd.DataFrame()
        # self.Model 
        self.QSeqPD = pd.DataFrame()
        self.QSeqNP = np.array([])
        self.logg = ""

#####################################################################
# Public                                                            #
#####################################################################
    
    def perceiveState(self, state, reward, learn = True, tabular = True, DQN = False):
        self._SequenceAppend(state, reward)
        self._UpdateNumTerminal()

        if tabular == True:
            self._UpdateStates(state, reward)
            # self._UpdateQOfSequenceStepN(self.alpha, self.gamma,-2)
        if DQN == True and len(self.Sequence) > self.batchsize*5:
            self._NewSequenceSample()
            # self._UpdateQOfSample(self.alpha, self.gamma)
            self._UpdateDQN()
            # if self.Nterminal > 1:
            #     self._NewSequenceSample(tonly=True)
            #     self._UpdateDQN()

    def nextAction(self,epsilon = 0):
        if self.Sequence[-1].state0[-1] == 1:
            self.LastActionType = ""
            self.LastAction = ""
            self.LastActionInt = -1
            return self.actions[0] # Update Env before returning  ""

        rand = self._NextRandInt()
        if rand < epsilon: # Random (x-case epsilon == 1)
            self.LastActionType = "r"
            self.LastAction = random.choice(self.actionsConstrains)
            self.LastActionInt =self.actions.index(self.LastAction)
        else: # Greedy (x-case epsilon == 0)
            self.LastActionType = "g"
            statefeatures = [state.features for state in self.States]
            s = statefeatures.index(self.Sequence[-1].state0)
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

    def QapxToStates(self):
        for state in self.States:
            f0 = np.array([state.features[i] for i in range(len(self.featurelist)-1)])
            features = np.expand_dims(f0, axis= 0)
            qs = self._ReturnQs(features)[0]
            state.Qapx = [q[0] for q in qs]
        return

    def RoundQ(self, numdec):
        for state in self.States:
            for j in range(len(state.Q)):
                state.Q[j] = round(state.Q[j],numdec)
                state.Qapx[j] = round(state.Qapx[j],numdec)

    def EchoPrint(self,afterNSteps = 10, prefix = ""):
        if self.Nterminal%afterNSteps == 0:
            print(prefix + "step: " + str(self.Nterminal),end ='\r')

    def setLearningParameter(self,alpha, gamma):
        self.alpha = alpha
        self.gamma = gamma

    def setModelTrainingParameter(self, batchsize = 64, replaybuffer = 1e5):
        self.batchsize = batchsize
        self.buffer = replaybuffer

    def modelInit(self, NumInput, NumLayers, act = 'ReLu'):
        self.Model = NN.clsNN(NumInput, NumLayers,ActFunction=act)

    def modelPredictQ(self,state):
        return self.Model.predict(state)

    def modelFit(self,X,y,TrainEpochs):
        modelLoss = self.Model.fitt(X, y, TrainEpochs)
        return modelLoss

    def SetActionConstrains(self, reducedActionList = [], forbiddenActions = []):
        assert reducedActionList== [] and not forbiddenActions == [] or forbiddenActions == [] and not reducedActionList == [], \
        "Choose only one constraint configuration"
        self.actionsConstrains = []
        if not reducedActionList == []:
            self.actionsConstrains = reducedActionList
        if not forbiddenActions == []:
            for action in self.actions:
                self.actionsConstrains.append(action)
            for action in forbiddenActions:
                self.actionsConstrains.remove(action) 
        
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
        if len(self.Sequence) == 0: 
            self.Sequence.append(typStep(state0 = featState, reward = reward, totalreward = reward))
            return

        if self.Sequence[-1].state0[-1] == 0: 
            self.Sequence[-1].state1 = featState
            self.Sequence[-1].actionInt = self.LastActionInt
            self.Sequence[-1].action = self.LastAction
            self.Sequence[-1].rg = self.LastActionType

            self.Sequence.append(typStep(state0 = featState, reward = reward, totalreward = self.Sequence[-1].totalreward + reward))
        else: 
            self.Sequence.append(typStep(state0 = featState, reward = reward, totalreward = reward))
            self.TerminalRewards.append([self.Sequence[-2].state0[:-1],self.Sequence[-2].reward])

        # self.Sequence.append(typStep(state0 = state0, actionInt = self.LastActionInt, action = self.LastAction, \
        #     state1 = featState, reward = reward, totalreward = totalrew_ + reward, rg = self.LastActionType))

    def _UpdateStates(self,state, reward):
        for i in range(len(self.States)):
            if state == self.States[i].features:
                self.States[i].visited +=1
                return
        self.States.append(typState(features = state, reward = reward))
        self.States[-1].Q = [0]*len(self.actions)
        self.States[-1].visited +=1
    
    def _UpdateQOfSequenceStepN(self, alpha, gamma, NSeqIndex):
        if len(self.Sequence)< -1*NSeqIndex+1:
            return
        if self.Sequence[NSeqIndex].state0[-1] == 1: # empty step (from terminal to nowhere)
            return
        state0 = self.Sequence[NSeqIndex].state0; s0 = [state.features for state in self.States].index(state0)
        state1 = self.Sequence[NSeqIndex].state1; s1 = [state.features for state in self.States].index(state1)
        r = self.Sequence[NSeqIndex].reward
        a = self.Sequence[NSeqIndex].actionInt

        alpha = max(1/self.States[s0].visited,self.alpha)
        if self.States[s0].features[-1] == 0: # non terminal
            self.States[s0].Q[a] = self.States[s0].Q[a] + alpha*(r +gamma*max(self.States[s1].Q) - self.States[s0].Q[a])
    
    def _UpdateQOfSample(self, alpha, gamma):
        X = np.array(self.SequenceSampleLISTX) # state and actions
        R = np.array(self.SequenceSampleLIST)[:,4] # reward
        A = np.array(self.SequenceSampleLIST)[:,1] # action
        X_ = np.array(self.SequenceSampleLISTX_) # follow up state

        for i in range(len(X)):
            s0 = [state.features for state in self.States].index(X[i].tolist())
            s1 = [state.features for state in self.States].index(X_[i].tolist())
            a = A[i]
            r = R[i]
            alpha = max(1/self.States[s0].visited,self.alpha)
            if self.States[s0].features[-1] == 0: # non terminal
                self.States[s0].Q[a] = self.States[s0].Q[a] + alpha*(r +gamma*max(self.States[s1].Q) - self.States[s0].Q[a])
    
    def _UpdateDQN(self):
        X = np.array(self.SequenceSampleLISTXA) # state and actions
        r = np.array(self.SequenceSampleLIST)[:,4] # reward
        X_ = np.array(self.SequenceSampleLISTX_) # follow up state
        X_t = list([])
        for state in X_:
            if state[-1] == 1:
                X_t.append([0]*(len(self.featurelist)-1))  
            else: 
                X_t.append([state[i] for i in range(len(self.featurelist)-1)])

        qmax = np.array(self._ReturnQs(X_t)).max(axis = 1)[:,0]
        for i in range(len(X_)):
            if X_[i][-1] == 1:
                for terrews in self.TerminalRewards:
                    if terrews[0] == X_[i][:-1].tolist(): 
                        qmax[i] = terrews[1]

        if len(self.Sequence) < self.batchsize*3:  
            NewQTarget = r # init model with rewards
            ftg = 10 
        else:
            NewQTarget = r + qmax
            ftg = 1
        loss = self.modelFit(X,NewQTarget,ftg)
        return

    def _ReturnQs(self, states):
        stateCopy =[]
        for i in range(len(self.actions)):
            # arr.append(np.copy(states).tolist())  -> check perfomance
            stateCopy.append([[feature for feature in state] for state in states]) # hard copy
        act010 = []
        for i in range(len(self.actions)):
            act010.append([1 if i == j else 0 for j in range(len(self.actions))])

        for i in range(len(stateCopy)):
            for j in range(len(stateCopy[i])):
                stateCopy[i][j] += act010[i] 
        stateCopyT = [[stateCopy[j][i] for j in range(len(stateCopy))] for i in range(len(stateCopy[0]))]

        qarr = []
        for stateaction in stateCopyT:
                qnp = self.modelPredictQ(np.array(stateaction)).tolist()
                qarr.append(qnp)
        # ttt = [[qarr[j][i] for j in range(len(qarr))] for i in range(len(qarr[0]))]
        return qarr

    def _Return01ChainFromInt(self, n, nmax):
        tmp =[]
        for i in range(nmax):
            if i == n:
                tmp.append(1)
            else:
                tmp.append(0)
        return tmp

    def _UpdateNumTerminal(self):
        if len(self.Sequence) > 0:
            if self.Sequence[-1].state0[-1] == 1: 
                self.Nterminal +=1

    def _NewSequenceSample(self, tonly = False):
        self.NewSequenceSampleTYP() if tonly == False else self.NewSequenceTerminalSampleTYP()
        self._ParseSequenceStepsToList()
        self._ParseSequenceSampleToListXXA()

    def NewSequenceSampleTYP(self,buffer=100):
        self.SequenceSampleTYP = []
        idx = list(range(self.batchsize*3)); random.shuffle(idx)
        c = 0; i = 0
        while c < self.batchsize:
            if not self.Sequence[-1*idx[i]].state1 == [0]: #skip epmty steps (from terminal to nowhere)
                self.SequenceSampleTYP.append(self.Sequence[-1*idx[i]])
                self.Sequence[-1*idx[i]].sampled += 1
                c += 1
            i +=1
        return

    def NewSequenceTerminalSampleTYP(self):
        self.SequenceSampleTYP = []
        for step in self.Sequence:
            if step.state1[-1] == 1 and len(self.SequenceSampleTYP) < self.batchsize:
                self.SequenceSampleTYP.append(step)
                step.sampled += 1
        return
    
    def _ParseSequenceStepsToList(self):
        self.SequenceSampleLIST = []; sample = []
        sample.append([step.state0 for step in self.SequenceSampleTYP])
        sample.append([step.actionInt for step in self.SequenceSampleTYP])
        sample.append([step.action for step in self.SequenceSampleTYP])
        sample.append([step.state1 for step in self.SequenceSampleTYP])
        sample.append([step.reward for step in self.SequenceSampleTYP])
        sample.append([step.totalreward for step in self.SequenceSampleTYP])
        sample.append([step.rg for step in self.SequenceSampleTYP])
        self.SequenceSampleLIST = list(map(list, zip(*sample)))

    def _ParseSequenceSampleToListXXA(self):
        self.SequenceSampleLISTX = [] 
        for step in self.SequenceSampleTYP:
            self.SequenceSampleLISTX.append(step.state0)
        
        self.SequenceSampleLISTX_ = []
        for step in self.SequenceSampleTYP:
            self.SequenceSampleLISTX_.append(step.state1)
    
        self.SequenceSampleLISTXA = []; sampleXA = []
        for step in self.SequenceSampleTYP:
            tmp = []
            for i in range(len(self.featurelist)-1): # exclude terminal state
                tmp.append(step.state0[i])
            tmp += self._Return01ChainFromInt(step.actionInt, len(self.actions))
            sampleXA.append(list(tmp))
        self.SequenceSampleLISTXA = sampleXA   

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

    def ExportQtoCSV(self, path, SplitCols = False, colQapx = False):
        self.RoundQ(2)
        Qpd = pd.DataFrame()
        Qpd["State"] = [state.features for state in self.States]
        Qpd["Q"] = [state.Q for state in self.States]
        Qpd["Qapx"] = [state.Qapx for state in self.States]
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
        Seqpd["totrew"] = [step.totalreward for step in self.Sequence]
        Seqpd["rnd_grd"] = [step.rg for step in self.Sequence]
        Seqpd["sampled"] = [step.sampled for step in self.Sequence]

        #Create 100evenly distributed indices from 0 to n terminal states-> arr
        arr0 = []; arr1 = []; arrTerminal = []
        for i in range(len(self.Sequence)):
            if self.Sequence[i].state0[-1] == 1:
                arrTerminal.append(i)
        if len(arrTerminal) > nthEpoch:
            for i in range(nthEpoch): 
                idx = int(i * len(arrTerminal)/nthEpoch)
                arr0.append(arrTerminal[idx])
                arr1.append(arrTerminal[idx+1])

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

    def ExportWeights(self,path):
        wpd = pd.DataFrame()
        a = self.Model.RetWeights()
        for i in range(len(a)):
            wpd["Layer "+ str(i)] = [layer[0].tolist() for layer in a]
            wpd["bias "+ str(i)] = [layer[1].tolist() for layer in a]
        wpd.to_csv(path, sep='|', encoding='utf-8', index = False)
      