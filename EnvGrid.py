import random

class typGridState:
    def __init__(self,x,y,r,t):
        self.x=x
        self.y=y
        self.reward=r
        self.terminal=t
        self.q = []             # used for verification only
    
class clsEnvironment:
    def __init__(self,rows,cols,reward):
        self.EnvStates = [[typGridState(i,j,reward,False) for j in range(cols)] for i in range(rows)]
        self.currentposition = (0,0)
        self.start = (0,0)
        self.limit_cols = cols
        self.limit_rows = rows
        self.step = 0
        self.run = 0
        self.features = ["x","y","terminal"]
        self.actions = ["up","down","left","right"]
        if rows == 1:
            self.actions = ["left","right"]
        if cols == 1:
            self.actions = ["up","down"]

    def __getitem__(self,pos):
        i,j = pos
        return self.EnvStates[i][j]

    def SetStartPosition(self,StartPosition):
        r,c = StartPosition
        assert r >= 0 and r < self.limit_rows and c >= 0 and c < self.limit_cols, "StartPosition out of Range"
        self.start = StartPosition
        self.currentposition = StartPosition
    
    def SetRandomStart(self):
        r = random.randint(0,self.limit_rows-1)
        c = random.randint(0, self.limit_cols-1)
        self.start = (r,c)
        self.currentposition = (r,c)

    def SetTerminalState(self,pos):
        row, col = pos
        self.EnvStates[row][col].terminal = True

    def SetRewardAtState(self,pos,Reward):
        row, col = pos
        self.EnvStates[row][col].reward = Reward

    def RetReward(self):
        x,y = self.currentposition
        return self.EnvStates[x][y].reward

    def RetState(self):
        if self.IsCurrentStateTerminal() == True:
            self.run += 1
            return str(self.currentposition) + "terminal1"
        return str(self.currentposition)

    def RetStateFeatures(self):
        t = 0
        if self.IsCurrentStateTerminal() == True:
            self.run += 1
            t = 1
        x,y = self.currentposition
        return [x,y,t]

    def RetGridAsArray(self):
        arr = []
        for i in range(self.limit_rows):
            arrRow = []
            for j in range(self.limit_cols):
                a = 0
                if self.currentposition == (i,j): a = 1
                arrRow.append(a)
            arr.append(arrRow)
        return arr

    def IsCurrentStateTerminal(self):
        row, col = self.currentposition
        if self.EnvStates[row][col].terminal==True:
            return True
        return False

    def Next(self,action):
        if action == "":
            self.move(random.choice(self.actions))
            return
        if self.IsCurrentStateTerminal(): 
            self.Reset()
        else:
            self.move(action)

    def move(self,direction):
        self.step = self.step +1
        r,c = self.currentposition
        if direction == "left" and c >0:
            self.currentposition = (r,c-1)
        elif direction == "right"and c < self.limit_cols-1:
            self.currentposition =(r,c+1)
        elif direction == "up" and r >0:
            self.currentposition = (r-1,c)
        elif direction == "down" and r < self.limit_rows-1:
            self.currentposition = (r+1,c)

    def ReturnActionList(self):
        return self.actions
    
    def ReturnFeatureList(self):
        return self.features

    def Reset(self):
        self.step = 0
        self.run = self.run+1
        self.currentposition = self.start
        

# ==============================================================================
# -- Verification --------------------------------------------------------------
# ==============================================================================

    def ReturnGroundTruthQTable(self):
        tStates = []
        for i in range(len(self.EnvStates)):
            for j in range(len(self.EnvStates[i])):
                if self.EnvStates[i][j].terminal == True:
                    tStates.append([self.EnvStates[i][j].x,self.EnvStates[i][j].y])
        assert len(tStates)==1 and str(tStates)== '[[0, 0]]',str(tStates)

        self._setqValuesToEnvStates()
        gtStates = []
        for i in range(len(self.EnvStates)):
            for j in range(len(self.EnvStates[i])):
                t = 1 if self.EnvStates[i][j].terminal else 0
                gtStates.append([[self.EnvStates[i][j].x, self.EnvStates[i][j].y, t] \
                    , self.EnvStates[i][j].q])
        return gtStates
    
    def _setqValuesToEnvStates(self):
        for i in range(self.limit_rows):
            for j in range(self.limit_cols):
                reward = self.EnvStates[i][j].reward
                q = float((i+j)*reward)
                qup = q if i > 0 else q+reward
                qdown = q+2*reward if i < self.limit_rows-1 else q+reward
                qleft = q if j > 0 else q+reward
                qright = q+2*reward if j < self.limit_cols-1 else q+reward
                if i == 0 and j == 0:
                    self.EnvStates[i][j].q = [0.0,0.0,0.0,0.0]
                else:
                    self.EnvStates[i][j].q = [qup,qdown,qleft,qright]
        return