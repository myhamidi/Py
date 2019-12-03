import random

class typGridState:
    def __init__(self,x,y,r,t):
        self.x=x
        self.y=y
        self.reward=r
        self.terminal=t
        self.q = []             # used for verification only
    
class clsEnvironment:
    def __init__(self,rows,cols,reward, parameters = []):
        self.cols = cols
        self.rows = rows
        self.ireward = reward
        if not parameters == []:
            assert len(parameters)==3, "Error! Length of Parameters!"
            self.rows = parameters[0]
            self.cols = parameters[1]
            self.ireward = parameters[2]
        self.EnvStates = [[typGridState(i,j,self.ireward,False) for j in range(self.cols)] for i in range(self.rows)]
        self.currentposition = (0,0)
        self.start = (0,0)

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
        assert r >= 0 and r < self.rows and c >= 0 and c < self.cols, "StartPosition out of Range"
        self.start = StartPosition
        self.currentposition = StartPosition
    
    def SetRandomStart(self):
        r = random.randint(0,self.rows-1)
        c = random.randint(0, self.cols-1)
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
        for i in range(self.rows):
            arrRow = []
            for j in range(self.cols):
                a = 0
                if self.currentposition == [i+1,j+1]: a = 1
                arrRow.append(a)
            arr.append(arrRow)
        return arr

    def IsCurrentStateTerminal(self):
        row, col = self.currentposition
        if self.EnvStates[row][col].terminal==True:
            return True
        return False

    def Next(self,action):
        # if action == "":
        #     self.move(random.choice(self.actions))
        #     return
        if self.IsCurrentStateTerminal(): 
            self.Reset()
        else:
            self.move(action)

    def move(self,direction):
        self.step = self.step +1
        r,c = self.currentposition
        if direction == "left" and 0 < c:
            self.currentposition = (r,c-1)
        elif direction == "right"and c < self.cols-1:
            self.currentposition =(r,c+1)
        elif direction == "up" and 0 < r:
            self.currentposition = (r-1,c)
        elif direction == "down" and r < self.rows-1:
            self.currentposition = (r+1,c)
        elif direction == "":
            self.currentposition = (r,c)

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
        assert len(tStates)==1,str(tStates)

        self._setqValuesToEnvStates(tStates)
        gtStates = []
        for i in range(len(self.EnvStates)):
            for j in range(len(self.EnvStates[i])):
                t = 1 if self.EnvStates[i][j].terminal else 0
                gtStates.append([[self.EnvStates[i][j].x, self.EnvStates[i][j].y, t] \
                    , self.EnvStates[i][j].q])
        return gtStates
    
    def _setqValuesToEnvStates(self,terminals):
        for i in range(self.rows):
            for j in range(self.cols):
                reward = self.EnvStates[i][j].reward
                dx = terminals[0][0]-i
                dy = terminals[0][1]-j
                q = float((abs(dx)+abs(dy))*reward)
                #ego bottomright
                if dx <= 0 and dy <= 0:
                    qup = q ; qleft = q; qdown = q+2*reward;qright = q+2*reward
                #ego bottomleft
                if dx > 0 and dy < 0:
                    qup = q ; qright = q; qdown = q+2*reward; qleft = q+2*reward
                #ego topright
                if dx < 0 and dy > 0:
                    qdown = q ; qleft = q; qup = q+2*reward; qright = q+2*reward
                #ego topleft
                if dx >= 0 and dy >= 0:
                    qdown = q ; qright = q; qup = q+2*reward; qleft = q+2*reward
                #if ego on edge
                if i == 0: qup = q+reward
                if j == 0: qleft = q+reward
                if i == self.cols-1: qdown = q+reward
                if j == self.rows-1: qright = q+reward
                if i == terminals[0][0] and j == terminals[0][1]:
                    self.EnvStates[i][j].q = [0.0,0.0,0.0,0.0]
                else:
                    self.EnvStates[i][j].q = [qup,qdown,qleft,qright]
        return