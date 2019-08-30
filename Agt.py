import pathlib
import pandas as pd
import random

class typRewState:
    def __init__(self,stateStr,statefeat,reward,value,visited):
        self.state = stateStr
        self.features = statefeat
        self.reward = reward
        self.value = value
        self.visited = visited

class clsAgent:
#Public:
    def __init__(self,actionlist):
        self.RewStates = []         #Typ: typRewState. Remembers all (unique) states visited.
        self.Sequence = []
        self.SequenceRewards = []   #Typ: (s,r,a,actionType). Remembers state (idx), reward and action
        self.SequenceFeatures = []   #Typ: (s,r,a,actionType). Remembers state (idx), reward and action
        self.SequenceRewardsTest = []   #Typ: (s,r,a,actionType). Remembers state (idx), reward and action
        self.lastSeqStep = ()
        self.actions = actionlist
        self.LastAction = ""
        self.LastActionType = "" #g,r (greedy, random)
        self.LastActionInt = 0
        self.Q = []                 #QTable, Type: Table of RewStates rows x action cols
        # self.FeatureStates= []      #Typ: List of state representation by Features.List of Lists [[],[],...]. Matchin index of self.RewStates
        self.QList = []          #Typ: List of QList represenation by features. Len = rows x cols from Q table.Lists [[],[],...]
        self.FeatureQ = []          #Typ: single col /List of Q valuse for QList

        self.alpha = .2
        self.gamma = 1
        self.rand = list(range(1000))
        random.shuffle(self.rand)
        self.randIdx = 0

    def perceiveState(self, state, reward):
        self._UpdateRewStates(state, reward)
        self._SequenceAppend(state, reward)
        self.lastSeqStep = self.SequenceRewards[-1]
        self._UpdateQOfLastSequenceStep(self.alpha, self.gamma)

    def getState(self, state, reward):
        self._UpdateRewStates(state, 0)
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
            s,_,_,_ = self.lastSeqStep      
            self.LastActionInt = self.Q[s].index(max(self.Q[s]))
            self.LastAction = self.actions[self.LastActionInt]     
        return self.LastAction

    def RoundQ(self, numdec):
        for i in range(len(self.Q)):
            for j in range(len(self.Q[i])):
                self.Q[i][j] = round(self.Q[i][j], numdec)
    
    def CreateQListFromQTable(self):
        assert len(self.RewStates) == len(self.Q), "Length of Agt states != Agt Q rows."
        self.QList = []
        for i in range(len(self.RewStates)):
            for j in range(len(self.Q[i])):
                arr = []
                for k in range(len(self.RewStates[i].features)):
                    arr.append((self.RewStates[i].features[k]))
                for k in range(len(self.actions)):
                    if k == j:
                        arr.append(1)
                    else:
                        arr.append(0)
                arr.append(self.Q[i][j])
                self.QList.append(arr)

    def ImportQTable(self,FeatStates,QTable):
        #Check StateFeatures
        assert len(self.actions) == len(QTable[0]), "Q Table Cols != Number of actions. Numer of actions is: " + str(len(self.actions))
        assert self.RewStates == [], "self.RewStates not empty"
        assert self.Q == [], "Q Table not empty"

        for i in range(len(FeatStates)):
            for j in range(len(FeatStates[i])):
                self.RewStates.append(typRewState("",FeatStates[i],0,0,0))
                self.Q.append([0]*len(self.actions))
                # self.pvAppendNewState(typRewState("",FeatStates[i],0,0,0),FeatStates[i])
        
        for i in range(len(QTable)):
            for j in range(len(QTable[i])):
                self.Q[i][j] = QTable[i][j]
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
        self.RewStates = [] 
        self.Q = [] 
        self.QList = []

    def setLearningParameter(self,alpha, gamma):
        self.alpha = alpha
        self.gamma = gamma

    def RetQTable(self):
        return self.Q

    def RetQList(self):
        return self.QList

    def RetFeatStates(self):
        arr = []
        for i in range(len(self.RewStates)):
            arr.append(self.RewStates[i].features)
        return arr

#Private:
    def pvNextRandInt(self):
        # Get Next Random Number from list
        self.randIdx +=1
        if self.randIdx == 1000: 
            self.randIdx = 0
        return self.rand[self.randIdx]/1000
    
    def pvSequence_ResetRewardOnTerminal(self):
        if len(self.SequenceRewards) >1:
            s1,r1,_,_ = self.SequenceRewards[-1]; s2,r2,_,_ = self.SequenceRewards[-2]
            if "terminal" in str(self.RewStates[s2].state) and not "terminal" in str(self.RewStates[s1].state):
                s1,_,a,ty = self.SequenceRewards[-1]; self.SequenceRewards[-1] = (s1,r1-r2,a,ty)

    def _SequenceAppend(self,featState,reward):
        idx = [state.features for state in self.RewStates].index(featState)
        r = self._RetRewardOfLastSequenceStep()
        self.SequenceRewards.append((idx,round(r + reward,1),self.LastActionInt,self.LastActionType))

    def _RetRewardOfLastSequenceStep(self):
        if self._IsFirstStepOfEpoch(): 
            return 0
        else:
            _,r,_,_ = self.lastSeqStep
            return r

    def _IsFirstStepOfEpoch(self):
        if len(self.SequenceRewards) == 0:
            return True
        else:
            s,_,_,_ = self.lastSeqStep
            if self.RewStates[s].features[-1] == 1:
                return True
            else:
                return False

    def _SequenceTestAppend(self, featState, reward):
        idx = [state.features for state in self.RewStates].index(featState)
        r = self._RetRewardOfLastSequenceStep()
        self.SequenceRewardsTest.append((idx, round(r+reward,1), self.LastActionInt, self.LastActionType))

    def _UpdateRewStates(self,state, reward):
        for i in range(len(self.RewStates)):
            if state == self.RewStates[i].features:
                self.RewStates[i].visited +=1
                return
        self.RewStates.append(typRewState("",state,reward,0,0))
        self.Q.append([0]*len(self.actions))
        i = len(self.RewStates) - 1
        self.RewStates[i].visited +=1
    
    def _UpdateQOfLastSequenceStep(self, alpha, gamma):
        if len(self.SequenceRewards)<3: 
            return
        s1,r1,a,_ = self.SequenceRewards[-1]
        s,r2,_,_ = self.SequenceRewards[-2]
        r = r1-r2
        alpha = max(1/self.RewStates[s1].visited,self.alpha)
        if self.RewStates[s].features[-1] == 0: # non terminal
            self.Q[s][a] = self.Q[s][a] + alpha*(r +gamma*max(self.Q[s1]) - self.Q[s][a])

    def printSequence100(self,textfile,xwr):
        f = open(textfile,xwr)
        f.write("Sequences 100\n")
        f.write("stateIndex|stateFeatures|state|reward|actionIndex|greed\n")
        #Create evenly distributed indices 0 to 99 of all terminal states-> arr
        arr = []; arrTerminal = []
        for i in range(len(self.SequenceRewards)):
            s,_,_,_ = self.SequenceRewards[i]
            if self.RewStates[s].features[-1] == 1:
                arrTerminal.append(i)
        for i in range(100):
            arr.append(int(i * len(arrTerminal)/99))
        #Take all sequence steps between arr[i] to arr[i]+1
        for i in range(99):
            for j in range(arrTerminal[arr[i]+1] - arrTerminal[arr[i]]):
                    s,r,a,ty = self.SequenceRewards[arrTerminal[arr[i]]+j+1]
                    feat = self.SequenceFeatures[arrTerminal[arr[i]]+j+1]
                    va = self.RewStates[s].state
                    f.write(str(s) + "|" + str(feat) + "|" + str(va) + "|" + str(r) + "|" + str(a) + "|" + str(ty) + "\n")         

    def printSequenceTest(self,textfile,xwr):
        f = open(textfile,xwr)
        
        f.write("stateIndex|state|reward|actionIndex|greed\n")
        for i in range(len(self.SequenceRewardsTest)):
            s,r,a,ty = self.SequenceRewardsTest[i]
            va = self.RewStates[s].state
            f.write(str(s) + "|" + str(va) + "|" + str(r) + "|" + str(a) + "|" + str(ty) + "\n")  

    def printQTable(self,textfile,xwr):  
        sep = " | "; nfeat = len(self.RewStates[0].features); nactions = len(self.actions)
        f = open(textfile,xwr)
        #Header
        for k in range(nfeat):
            f.write("feat "+str(k)+sep)    
        f.write("visited"+sep)
        for k in range(nactions):
            if k == nactions-1:
                f.write(self.actions[k])
            else:
                f.write(self.actions[k]+sep)
        f.write("\n") 
        #Data
        for i in range(len(self.RewStates)):
            assert len(self.Q[i]) == nactions, "actions != Q coloums at Q row: " + str(i)
            tmpstr = ""
            for j in range(nfeat):
                tmpstr += str(self.RewStates[i].features[j]) + sep    
            tmpstr += str(self.RewStates[i].visited) + sep 
            for j in range(nactions):
                if j == nactions-1:
                    tmpstr += str(self.Q[i][j])
                else:
                    tmpstr += str(self.Q[i][j]) + sep
            f.write(tmpstr + "\n")

    def printQList(self,textfile,xwr):
        sep = " | "; nfeat = len(self.RewStates[0].features); nactions = len(self.actions)
        f = open(textfile,xwr)
        #Header
        for k in range(nfeat):
            f.write("feat "+str(k)+sep)    
        for k in range(nactions):
            f.write(self.actions[k]+sep)
        f.write("Q\n") 
        for i in range(len(self.QList)):
            tmpstr = ""
            for j in range(len(self.QList[i])):
                if j == len(self.QList[i])-1:
                   tmpstr += str(self.QList[i][j])
                else: 
                    tmpstr += str(self.QList[i][j])+sep
            f.write(tmpstr + "\n")

    def ping(self):
        print("Agent here")