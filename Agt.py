import pathlib
import pandas as pd
import random

class typState:
    def __init__(self, stateStr = "", features = [] , reward = 0.0, Q = [], value= 0.0 , visited = 0):
        self.stateStr = stateStr
        self.features = features
        self.reward = reward
        self.Q = Q
        self.value = value 
        self.visited = visited

class typStep:
    def __init__(self, stateStr = "", statefeatures = [] , reward = 0.0, totalreward = 0.0, Q = [], actionInt = -1, action = "", rg = "r"):
        self.stateStr = stateStr
        self.statefeat = statefeatures
        self.reward = reward
        self.totalreward = totalreward
        self.actionInt = actionInt
        self.action = action
        self.rg = rg

class clsAgent:
#Public:
    def __init__(self, actionlist, featurelist = []):
        self.States = []         #Typ: typState. Remembers all (unique) states visited.
        self.Sequence = []
        self.SequenceRewards = []   #Typ: (s,r,a,actionType). Remembers state (idx), reward and action
        self.SequenceFeatures = []   #Typ: (s,r,a,actionType). Remembers state (idx), reward and action
        self.SequenceRewardsTest = []   #Typ: (s,r,a,actionType). Remembers state (idx), reward and action
        self.lastSeqStep = ()
        self.lastStep = typStep()
        self.actions = actionlist
        self.statefeatures = featurelist
        self.LastAction = ""
        self.LastActionType = "" #g,r (greedy, random)
        self.LastActionInt = -1
        self.Q = []                 #QTable, Type: Table of RewStates rows x action cols
        # self.FeatureStates= []      #Typ: List of state representation by Features.List of Lists [[],[],...]. Matchin index of self.States
        self.QList = []          #Typ: List of QList represenation by features. Len = rows x cols from Q table.Lists [[],[],...]
        self.FeatureQ = []          #Typ: single col /List of Q valuse for QList

        self.alpha = .2
        self.gamma = 1
        self.rand = list(range(1000))
        random.shuffle(self.rand)
        self.randIdx = 0

    def perceiveState(self, state, reward):
        self._UpdateStates(state, reward)
        self._SequenceAppend(state, reward)
        self.lastSeqStep = self.SequenceRewards[-1]
        self._UpdateQOfLastSequenceStep(self.alpha, self.gamma)

        self.lastStep = self.Sequence[-1]

    def getState(self, state, reward):
        self._UpdateStates(state, 0)
        self._SequenceTestAppend(state, reward)
        self.lastSeqStep = self.SequenceRewardsTest[-1]

    def nextAction(self,epsilon):
        rand = self.pvNextRandInt()
        if rand < epsilon: # Random
            self.LastActionType = "r"
            self.LastAction = random.choice(self.actions)
            self.LastActionInt =self.actions.index(self.LastAction)
        else: # Greedy
            self.LastActionType = "g"
            s1,_,_,_ = self.lastSeqStep
            statefeatures = [state.features for state in self.States]
            s = statefeatures.index(self.Sequence[-1].statefeat)
            assert s == s1, "Oh"
            #     stop = 0    
            # self.LastActionInt = self.Q[s].index(max(self.Q[s]))
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

    def ImportQTable(self,FeatStates,Qpd):
        #Check StateFeatures
        assert len(self.actions) == len(Qpd[0]), "Q Table Cols != Number of actions. Numer of actions is: " + str(len(self.actions))
        assert self.States == [], "self.States not empty"
        assert self.Q == [], "Q Table not empty"

        for i in range(len(FeatStates)):
            for j in range(len(FeatStates[i])):
                self.States.append(typState(features = FeatStates[i]))
                self.Q.append([0]*len(self.actions))
                # self.pvAppendNewState(typState("",FeatStates[i],0,0,0),FeatStates[i])
        
        for i in range(len(Qpd)):
            for j in range(len(Qpd[i])):
                self.Q[i][j] = Qpd[i][j]
                #MOHI

    def ImportQList(self,Qlist):
        assert self.QList == [], "Q List not empty"
        for i in range(len(Qlist)):
            self.QList.append([])
            for j in range(len(Qlist[i])):
               self.QList[i].append(Qlist[i][j])

    def Importcsv(self, path):
        return pd.read_csv(path,skiprows = 0,
                      na_values = "?", comment='\t',
                      sep="|",skipinitialspace=True,error_bad_lines=False)

    def resetSequenceRewards(self):
        self.SequenceRewards = []

    def resetSequenceRewardsTest(self):
        self.SequenceRewardsTest = []

    def reset(self):
        self.States = [] 
        self.Q = [] 
        self.QList = []

    def setLearningParameter(self,alpha, gamma):
        self.alpha = alpha
        self.gamma = gamma

#Private:
    def pvNextRandInt(self):
        # Get Next Random Number from list
        self.randIdx +=1
        if self.randIdx == 1000: 
            self.randIdx = 0
        return self.rand[self.randIdx]/1000

    def _SequenceAppend(self,featState,reward):
        idx = [state.features for state in self.States].index(featState)
        r = self._RetRewardOfLastSequenceStep()
        self.SequenceRewards.append((idx,round(r + reward,1),self.LastActionInt,self.LastActionType))
        
        if len(self.Sequence) == 0:
            r = 0 
        else:
            r = self.Sequence[-1].totalreward
        self.Sequence.append(typStep(actionInt = self.LastActionInt, action = self.LastAction, \
            statefeatures = featState, reward = reward, totalreward = r + reward, rg = self.LastActionType))

    def _RetRewardOfLastSequenceStep(self):
        if self._LastSeqIsFirstStep(): 
            return 0
        else:
            _,r,_,_ = self.lastSeqStep
            return r
    
    def _LastSeqIsFirstStep(self):
        if len(self.Sequence) == 0:
            return True
        if len(self.Sequence) == 1:
            return False                # tbd
        if self.Sequence[-1].statefeat[-1] == 1:
            return True
        else:
            return False

    def _SequenceTestAppend(self, featState, reward):
        idx = [state.features for state in self.States].index(featState)
        r = self._RetRewardOfLastSequenceStep()
        self.SequenceRewardsTest.append((idx, round(r+reward,1), self.LastActionInt, self.LastActionType))

    def _UpdateStates(self,state, reward):
        for i in range(len(self.States)):
            if state == self.States[i].features:
                self.States[i].visited +=1
                return
        self.States.append(typState(features = state, reward = reward))
        # self.Q.append([0]*len(self.actions)) # to be obs
        self.States[-1].Q = [0]*len(self.actions)
        self.States[-1].visited +=1
    
    def _UpdateQOfLastSequenceStep(self, alpha, gamma):
        if len(self.SequenceRewards)<3: 
            return
        s1,r1,a,_ = self.SequenceRewards[-1]
        s,r2,_,_ = self.SequenceRewards[-2]
        r = r1-r2
        alpha = max(1/self.States[s1].visited,self.alpha)
        if self.States[s].features[-1] == 0: # non terminal
            # self.Q[s][a] = self.Q[s][a] + alpha*(r +gamma*max(self.Q[s1]) - self.Q[s][a])
            self.States[s].Q[a] = self.States[s].Q[a] + alpha*(r +gamma*max(self.States[s1].Q) - self.States[s].Q[a])
            # assert self.Q[s] == self.States[s].Q, str(self.States[s].features) + str(self.Q[s1]) + "|" + str(self.States[s].Q)      

    def printSequenceTest(self,textfile,xwr):
        f = open(textfile,xwr)
        
        f.write("stateIndex|state|reward|actionIndex|greed\n")
        for i in range(len(self.SequenceRewardsTest)):
            s,r,a,ty = self.SequenceRewardsTest[i]
            va = self.States[s].state
            f.write(str(s) + "|" + str(va) + "|" + str(r) + "|" + str(a) + "|" + str(ty) + "\n")  

    def ping(self):
        print("Agent here")

    def WriteQtoCSV(self, path, SplitCols = False):
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

    def WriteSeqtoCSV(self, path, SplitCols = False):
        # Create full size data frame
        Seqpd = pd.DataFrame()
        Seqpd["actionInt"] = [step.actionInt for step in self.Sequence]
        Seqpd["action"] = [step.action for step in self.Sequence]
        
        if SplitCols == True:
            for i in range(len(self.actions)):
                Seqpd["blaction"+str(i)] = 0
            for index, row in Seqpd.iterrows():
                for i in range(len(self.actions)):
                    if row["actionInt"] == i: 
                        Seqpd.at[index, "blaction"+str(i)] = 1
        
        Seqpd["state"] = [step.statefeat for step in self.Sequence]
        Seqpd["reward"] = [step.reward for step in self.Sequence]
        Seqpd["rnd_grd"] = [step.rg for step in self.Sequence]

        #Create evenly distributed indices 0 to 99 of all terminal states-> arr
        arr = []; arrTerminal = []
        for i in range(len(self.Sequence)):
            if self.Sequence[i].statefeat[-1] == 1:
                arrTerminal.append(i)
        for i in range(100): arr.append(int(i * len(arrTerminal)/99))
        
        #Mark all lines between index arr[i] - arr[i+1]
        Seqpd["mark"] = 0
        for i in range(99):
            for j in range(arrTerminal[arr[i]], arrTerminal[arr[i]+1]):
                Seqpd.at[j, "mark"] = 1
        
        # Filter data frame
        Seq100pd =  Seqpd[Seqpd["mark"] == 1]
        Seq100pd = Seq100pd.drop(columns = ["mark"])

        # WRITE TO FILE:
        Seq100pd.to_csv(path, sep='|', encoding='utf-8', index = False)
      