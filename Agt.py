import myTracer;tr = myTracer.glTracer

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
        self.actions = actionlist
        self.LastAction = ""
        self.LastActionType = "" #g,r (greedy, random)
        self.LastActionInt = 0
        self.Q = []                 #Type: Table of RewStates rows x action cols
        self.FeatureStates= []      #Typ: List of state representation by Features.List of Lists [[],[],...]. Matchin index of self.RewStates
        self.FeatureStatesAndActions = []          #Typ: List of FeatureStatesAndActions represenation by features. Len = rows x cols from Q table.Lists [[],[],...]
        self.FeatureQ = []          #Typ: single col /List of Q valuse for featureStatesAndActions

        self.alpha = .2
        self.gamma = 1
        self.rand = list(range(1000))
        random.shuffle(self.rand)
        self.randIdx = 0

    def perceiveState(self,featState,strState,reward):
        tr.call("clsAgent.perceiveState")
        idx = self.pvRetIndex(strState,reward,featState)
        alpha = max(1/self.RewStates[idx].visited,self.alpha)      # Learning rate adaptation
        self.pvExtendSequence(idx, featState,reward)
        self.pvExtendTransitionMatrix()
        self.pvUpdateQ(alpha,self.gamma)

    def pvExtendSequence(self,idx, featState,reward):
        if len(self.SequenceRewards) == 0:r=0
        else: _,r,_,_ = self.SequenceRewards[-1]
        self.SequenceFeatures.append(featState)
        self.SequenceRewards.append((idx,round(r+reward,1),self.LastActionInt,self.LastActionType))
    
    def MergeStateFeaturesAndQ(self):
        for i in range(len(self.FeatureStates)):
            for j in range(len(self.Q[i])):
                arr = []
                for k in range(len(self.FeatureStates[i])):
                    arr.append(self.FeatureStates[i][k])
                for k in range(len(self.actions)):
                    if k == j:
                        arr.append(1)
                    else:
                        arr.append(0)
                self.FeatureStatesAndActions.append(arr)
                self.FeatureQ.append(self.Q[i][j])

    def getState(self,strState,reward,featState):
        tr.call("clsAgent.takeState")
        idx = self.pvRetIndex(strState,0,featState)
        #standard Sequence
        if len(self.SequenceRewards) == 0:r=0
        else: _,r,_,_ = self.SequenceRewards[-1]
        self.SequenceRewards.append((idx,round(r+reward,1),self.LastActionInt,self.LastActionType))
        #test Sequence
        if len(self.SequenceRewardsTest) == 0:r=0
        else: _,r,_,_ = self.SequenceRewardsTest[-1]
        self.SequenceRewardsTest.append((idx,round(r+reward,1),self.LastActionInt,self.LastActionType))
        #Reset reward ->0 after terminal state
        if len(self.SequenceRewardsTest) >1:
            s1,_,_,_ = self.SequenceRewardsTest[-1]; s2,_,_,_ = self.SequenceRewardsTest[-2]
            if "terminal" in str(self.RewStates[s2].state) and not "terminal" in str(self.RewStates[s1].state):
                s1,_,a,ty = self.SequenceRewardsTest[-1]; self.SequenceRewardsTest[-1] = (s1,0,a,ty)

    def nextAction(self,epsilon):
        tr.call("clsAgent.nextAction")
        # Get Next Random Number from list
        self.randIdx +=1
        if self.randIdx == 1000: self.randIdx = 0
        rand = self.rand[self.randIdx]/1000

        if rand < epsilon:
            return self.retNextAction("random")
        else:
            return self.retNextAction("greedy")
    
    def retNextAction(self,policy):
        tr.call("clsAgent.retNextAction")
        if policy == "random":
            self.LastAction = random.choice(self.actions)
            self.LastActionInt =self.actions.index(self.LastAction)
            self.LastActionType = "r"
            return self.LastAction
        if policy == "greedy":
            s,_,_,_ = self.SequenceRewards[-1]        
            self.LastActionInt = self.Q[s].index(max(self.Q[s]))
            self.LastAction = self.actions[self.LastActionInt]
            self.LastActionType = "g"
            return self.LastAction
        #Return
        return ""
    
    def resetSequenceRewards(self):
        tr.call("clsAgent.resetSequenceRewards")
        self.SequenceRewards = []

    def resetSequenceRewardsTest(self):
        tr.call("clsAgent.resetSequenceRewardsTest")
        self.SequenceRewardsTest = []
    
    def setLearningParameter(self,alpha, gamma):
        tr.call("clsAgent.setLearningParameter")
        self.alpha = alpha
        self.gamma = gamma

#Private:
    def pvAppendNewState(self,RewardState,featureState):
        tr.call("clsAgent.pvAppendNewState")
        self.RewStates.append(RewardState)
        self.FeatureStates.append(featureState)
        self.TransitionMatrix.append([])
        self.pvExtendQ()

    def pvRetIndex(self,strState,reward,featureState):
        tr.call("clsAgent.pvRetIndex")
        for i in range(len(self.RewStates)):
            if featureState == self.RewStates[i].features:
                self.RewStates[i].visited +=1
                return i
            # if strState == self.RewStates[i].state:
            #     self.RewStates[i].visited +=1
            #     return i    
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

    def pvExtendQ(self):
        tr.call("clsAgent.pvExtendQ")
        self.Q.append([])
        for  _ in range(len(self.actions)):
            self.Q[-1].append(0)
    
    def pvUpdateQ(self,alpha, gamma):
        tr.call("clsAgent.pvUpdateQ")
        if len(self.SequenceRewards)<3: 
            return
        s1,r1,a,ty = self.SequenceRewards[-1]
        s,r2,_,_ = self.SequenceRewards[-2]
        r = r1-r2
        if not "terminal" in str(self.RewStates[s].state):
            self.Q[s][a] = self.Q[s][a] + alpha*(r +gamma*max(self.Q[s1]) - self.Q[s][a])
        else:
            self.SequenceRewards[-1] = (s1,0,a,ty)

    def pvExtendFeatureStates(self):
        if len (self.SequenceRewards)>1: #start from 2nd step
            FromIdx,_,_,_ = self.SequenceRewards[-2]
            ToIdx,_,_,_ = self.SequenceRewards[-1]
            if not (self.LastAction,ToIdx) in self.TransitionMatrix[FromIdx]:
                self.TransitionMatrix[FromIdx].append((self.LastAction,ToIdx))
                self.TransitionMatrix[FromIdx].sort()

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

    def printQ(self,textfile,xwr):  
        tr.call("clsAgent.printQ")
        f = open(textfile,xwr)
        f.write("Q\n")
        f.write("state|visited|q1|q2\n")
        for i in range(len(self.TransitionMatrix)):
            tmpstr = self.RewStates[i].state.replace(",","|") + "|" + str(self.RewStates[i].visited) + " |" 
            for j in range(len(self.Q[i])):
                a = self.actions[j]
                tmpstr += a + "| Q:" + str(round(self.Q[i][j],4)) + "|"
            f.write(tmpstr + "\n")

    def printSequence100(self,textfile,xwr):
        tr.call("clsAgent.printSequence100")
        f = open(textfile,xwr)
        f.write("Sequences 100\n")
        f.write("stateIndex|stateFeatures|state|reward|actionIndex|greed\n")
        #Create evenly distributed indices
        arr = []; arrTerminal = []
        for i in range(len(self.SequenceRewards)):
            s,_,_,_ = self.SequenceRewards[i]
            if "terminal" in str(self.RewStates[s].state):
                arrTerminal.append(i)
        for i in range(100):
            arr.append(int(i * len(arrTerminal)/99))
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

    def printQwithFeatures(self,Featurefile,Qfile,xwr):
        self.MergeStateFeaturesAndQ()
        f = open(Featurefile,xwr)
        f.write("Features\n")
        for i in range(len(self.FeatureStatesAndActions)):
            for j in range(len(self.FeatureStatesAndActions[i])):
                f.write(str(self.FeatureStatesAndActions[i][j]))
                if not j == len(self.FeatureStatesAndActions[i])-1:
                    f.write("|")
            f.write("\n")
        
        fq = open(Qfile,xwr)
        fq.write("Features\n")
        for i in range(len(self.FeatureQ)):
            fq.write(str(round(self.FeatureQ[i],4)))
            fq.write("\n")