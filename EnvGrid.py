import myTracer;tr = myTracer.glTracer
import random

class typGridState:
    def __init__(self,x,y,r,t):
        tr.call("typGridState.init")
        self.x=x
        self.y=y
        self.reward=r
        self.terminal=t
    
class clsEnvironment:
    def __init__(self,rows,cols,reward):
        tr.call("clsEnvironment.init")
        self.EnvStates = [[typGridState(i,j,reward,False) for j in range(cols)] for i in range(rows)]
        self.currentposition = (0,0)
        self.start = (0,0)
        self.limit_cols = cols
        self.limit_rows = rows
        self.step = 0
        self.run = 0
        self.actions = ["up","down","left","right"]
        if rows == 1:
            self.actions = ["left","right"]
        if cols == 1:
            self.actions = ["up","down"]

    def __getitem__(self,pos):
        tr.call("clsEnvironment.__getitem__")
        i,j = pos
        return self.EnvStates[i][j]

    def SetStartPosition(self,StartPosition):
        tr.call("clsEnv.SetStartPosition")
        r,c = StartPosition
        assert r >= 0 and r < self.limit_rows and c >= 0 and c < self.limit_cols, "StartPosition out of Range"
        self.start = StartPosition
        self.currentposition = StartPosition
    
    def SetRandomStart(self):
        tr.call("clsEnv.SetRandomStart")
        r = random.randint(0,self.limit_rows-1)
        c = random.randint(0, self.limit_cols-1)
        self.start = (r,c)
        self.currentposition = (r,c)

    def SetTerminalState(self,pos):
        tr.call("clsEnv.setTerminalState")
        row, col = pos
        self.EnvStates[row][col].terminal = True

    def SetRewardAtState(self,pos,Reward):
        tr.call("clsEnv.setRewardAtState")
        row, col = pos
        self.EnvStates[row][col].reward = Reward

    def RetReward(self):
        tr.call("clsEnv.RetReward")
        x,y = self.currentposition
        return self.EnvStates[x][y].reward

    def RetState(self):
        tr.call("clsEnv.RetState")
        if self.IsCurrentStateTerminal() == True:
            self.run += 1
            return str(self.currentposition) + "terminal1"
        return str(self.currentposition)

    def RetGridAsArray(self):
        tr.call("clsEnv.RetGridAsArray")
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
        tr.call("clsEnv.IsStateTerminal")
        row, col = self.currentposition
        if self.EnvStates[row][col].terminal==True:
            return True
        return False

    def Next(self,action):
        self.move(action)

    def move(self,direction):
        tr.call("clsEnvironment.move")
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
        tr.call("clsEnv.returnActionList")
        return self.actions

    def Reset(self):
        self.step = 0
        self.run = self.run+1
        self.currentposition = self.start