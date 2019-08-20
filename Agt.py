import myTracer;tr = myTracer.glTracer
import pathlib
import pandas as pd
import random

class typRewState:
    def __init__(self,stateStr,statefeat,reward,value,visited):
        tr.call("typRewState.init")
        self.state = stateStr
        self.features = statefeat
        self.reward = reward
        self.value = value
        self.visited = visited

class clsAgent:
#Public:
    def __init__(self,actionlist):
        tr.call("clsAgent.__init__")
        self.RewStates = []         #Typ: typRewState. Remembers all (unique) states visited.
        self.Sequence = []
        self.SequenceRewards = []   #Typ: (s,r,a,actionType). Remembers state (idx), reward and action
        self.SequenceFeatures = []   #Typ: (s,r,a,actionType). Remembers state (idx), reward and action
        self.SequenceRewardsTest = []   #Typ: (s,r,a,actionType). Remembers state (idx), reward and action
        self.TransitionMatrix = []  #Typ: List of Lists of tuples[[],[],...]
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

    def perceiveState(self,featState,strState,reward):
        tr.call("clsAgent.perceiveState")
        idx = self.pvRetIndex(strState,reward,featState)
        self.pvExtendSequence(idx, featState, reward)
        self.pvSequence_ResetRewardOnTerminal()
        self.pvExtendTransitionMatrix()
        self.pvUpdateQ(self.RewStates[idx].visited, self.alpha, self.gamma)

    def getState(self,featState,strState,reward):
        tr.call("clsAgent.takeState")
        idx = self.pvRetIndex(strState,0,featState)
        self.pvExtendSequenceTest(idx, featState, reward)
        self.pvSequenceTest_ResetRewardOnTerminal()

    def nextAction(self,epsilon):
        tr.call("clsAgent.nextAction")
        rand = self.pvNextRandInt()
        if rand < epsilon: #Random
            self.LastActionType = "r"
            self.LastAction = random.choice(self.actions)
            self.LastActionInt =self.actions.index(self.LastAction)
        else: #Greedy
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
                self.pvAppendNewState(typRewState("",FeatStates[i],0,0,0),FeatStates[i])
        
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
        tr.call("clsAgent.resetSequenceRewards")
        self.SequenceRewards = []

    def resetSequenceRewardsTest(self):
        tr.call("clsAgent.resetSequenceRewardsTest")
        self.SequenceRewardsTest = []

    def reset(self):
        self.RewStates = [] 
        self.Q = [] 
        self.QList = []

    def setLearningParameter(self,alpha, gamma):
        tr.call("clsAgent.setLearningParameter")
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

    def pvSequenceTest_ResetRewardOnTerminal(self):
        if len(self.SequenceRewardsTest) >1:
            s1,r1,_,_ = self.SequenceRewardsTest[-1]; s2,r2,_,_ = self.SequenceRewardsTest[-2]
            if "terminal" in str(self.RewStates[s2].state) and not "terminal" in str(self.RewStates[s1].state):
                s1,_,a,ty = self.SequenceRewardsTest[-1]; self.SequenceRewardsTest[-1] = (s1,r1-r2,a,ty)
    
    def pvSequence_ResetRewardOnTerminal(self):
        if len(self.SequenceRewards) >1:
            s1,r1,_,_ = self.SequenceRewards[-1]; s2,r2,_,_ = self.SequenceRewards[-2]
            if "terminal" in str(self.RewStates[s2].state) and not "terminal" in str(self.RewStates[s1].state):
                s1,_,a,ty = self.SequenceRewards[-1]; self.SequenceRewards[-1] = (s1,r1-r2,a,ty)

    def pvExtendSequence(self,idx, featState,reward):
        if len(self.SequenceRewards) == 0:r=0
        else: _,r,_,_ = self.SequenceRewards[-1]
        self.SequenceFeatures.append(featState)
        self.SequenceRewards.append((idx,round(r+reward,1),self.LastActionInt,self.LastActionType))
        self.lastSeqStep = self.SequenceRewards[-1]

    def pvExtendSequenceTest(self,idx,featState,reward):
        if len(self.SequenceRewardsTest) == 0:r=0
        else: _,r,_,_ = self.SequenceRewardsTest[-1]
        self.SequenceRewardsTest.append((idx, round(r+reward,1), self.LastActionInt, self.LastActionType))
        self.lastSeqStep = self.SequenceRewardsTest[-1]

    def pvAppendNewState(self,RewardState,featureState):
        tr.call("clsAgent.pvAppendNewState")
        self.RewStates.append(RewardState)
        # self.FeatureStates.append(featureState)
        self.TransitionMatrix.append([])
        self.pvAddQrow()

    def pvRetIndex(self,strState,reward,featureState):
        tr.call("clsAgent.pvRetIndex")
        for i in range(len(self.RewStates)):
            if featureState == self.RewStates[i].features:
                self.RewStates[i].visited +=1
                return i  
        self.pvAppendNewState(typRewState(strState,featureState,reward,0,0),featureState)
        i = len(self.RewStates) - 1
        self.RewStates[i].visited +=1
        return i 

    def pvExtendTransitionMatrix(self): #Type StateTransition: (1,3). From 1 to 3
        tr.call("clsAgent.pvExtendTransitionMatrix")
        if len (self.SequenceRewards)>1: #start from 2nd step
            FromIdx,_,_,_ = self.SequenceRewards[-2]
            ToIdx,_,_,_ = self.SequenceRewards[-1]
            if not (self.LastAction,ToIdx) in self.TransitionMatrix[FromIdx]:
                self.TransitionMatrix[FromIdx].append((self.LastAction,ToIdx))
                self.TransitionMatrix[FromIdx].sort()

    def pvAddQrow(self):
        tr.call("clsAgent.pvAddQrow")
        self.Q.append([])
        for  _ in range(len(self.actions)):
            self.Q[-1].append(0)
    
    def pvUpdateQ(self, visited, alpha, gamma):
        tr.call("clsAgent.pvUpdateQ")
        alpha = max(1/visited,self.alpha)
        if len(self.SequenceRewards)<3: 
            return
        s1,r1,a,ty = self.SequenceRewards[-1]
        s,r2,_,_ = self.SequenceRewards[-2]
        r = r1-r2
        if not "terminal" in str(self.RewStates[s].state):
            self.Q[s][a] = self.Q[s][a] + alpha*(r +gamma*max(self.Q[s1]) - self.Q[s][a])

    # def pvExtendFeatureStates(self):
    #     if len (self.SequenceRewards)>1: #start from 2nd step
    #         FromIdx,_,_,_ = self.SequenceRewards[-2]
    #         ToIdx,_,_,_ = self.SequenceRewards[-1]
    #         if not (self.LastAction,ToIdx) in self.TransitionMatrix[FromIdx]:
    #             self.TransitionMatrix[FromIdx].append((self.LastAction,ToIdx))
    #             self.TransitionMatrix[FromIdx].sort()

    def printTransitions(self,textfile,xwr):
        tr.call("clsAgent.printTransitions")
        f = open(textfile,xwr)
        f.write("Transitions\n")
        f.write("state|visited|q1|q2\n")    
        for i in range(len(self.TransitionMatrix)):
            tmpstr = self.RewStates[i].state + "|" + str(self.RewStates[i].visited) + "|" 
            for j in range(len(self.TransitionMatrix[i])):
                a,toState = self.TransitionMatrix[i][j]
                aIdx = self.actions.index(a)
                tmpstr += a + self.RewStates[toState].state + "Q:" + str(round(self.Q[i][aIdx],4)) + "|"
            f.write(tmpstr + "\n")

    def printSequence100(self,textfile,xwr):
        tr.call("clsAgent.printSequence100")
        f = open(textfile,xwr)
        f.write("Sequences 100\n")
        f.write("stateIndex|stateFeatures|state|reward|actionIndex|greed\n")
        #Create evenly distributed indices 0 to 99 of all terminal states-> arr
        arr = []; arrTerminal = []
        for i in range(len(self.SequenceRewards)):
            s,_,_,_ = self.SequenceRewards[i]
            if "terminal" in str(self.RewStates[s].state):
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
        tr.call("clsAgent.printSequenceTest")
        f = open(textfile,xwr)
        
        f.write("stateIndex|state|reward|actionIndex|greed\n")
        for i in range(len(self.SequenceRewardsTest)):
            s,r,a,ty = self.SequenceRewardsTest[i]
            va = self.RewStates[s].state
            f.write(str(s) + "|" + str(va) + "|" + str(r) + "|" + str(a) + "|" + str(ty) + "\n")  

    def printQTable(self,textfile,xwr):  
        tr.call("clsAgent.printQ")
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
        tr.call("clsAgent.printQ")
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