class typGridState:
    def __init__(self,x,y,t,r):
        self.features = [float(x), float(y), int(t)]
        self.reward = float(r)
    
class clsEnvironment:
    def __init__(self, rows, cols, reward):
        self.cols = cols
        self.rows = rows
        self.EnvStates = [[typGridState(i,j,0,reward) for j in range(self.cols)] for i in range(self.rows)]
        self.currentstate = self.EnvStates[0][0].features
        self.start = self.EnvStates[0][0].features
        self.step = 0
        self.run = 0
        self.features = ["x","y","terminal"]
        self.actions = ["up","down","left","right"]
        if rows == 1:
            self.actions = ["left","right"]
        if cols == 1:
            self.actions = ["up","down"]

    def __getitem__(self, state):
        return self.EnvStates[int(state[0])][int(state[1])]

    def SetStartPosition(self, state):
        assert 0 <= state[0] and state[0] < self.rows
        assert 0 <= state[1] and state[1] < self.cols
        self.start = state + [self.__getitem__(state).features[-1]]
        self.currentstate = state + [self.__getitem__(state).features[-1]]

    def SetTerminalState(self, state, reward):
        self.EnvStates[state[0]][state[1]].features[-1] = 1
        self.EnvStates[state[0]][state[1]].reward = reward

    def SetReward(self, state, reward):
        self.EnvStates[state[0]][state[1]].reward = reward

    def Reward(self,state =[]):
        if state == []:
            state = self.currentstate[:-1]
        return self.__getitem__(state).reward

    def State(self):
        return self.currentstate

    def GridStateAsList(self):
        arr = []
        for i in range(self.rows):
            arrRow = []
            for j in range(self.cols):
                a = 0
                if self.currentstate[:-1] == [i,j]: a = 1
                arrRow.append(a)
            arr.append(arrRow)
        return arr

    def Step(self,action):
        if self.currentstate[-1] == 1: 
            self.Reset()
        else:
            self.step = self.step +1
            self.move(action)

    def move(self,direction):
        r=self.currentstate[0]
        c=self.currentstate[1]
        if direction == "left" and 0 < c:
            self.currentstate = self.__getitem__([r,c-1]).features
        elif direction == "right"and c < self.cols-1:
            self.currentstate =self.__getitem__([r,c+1]).features
        elif direction == "up" and 0 < r:
            self.currentstate = self.__getitem__([r-1,c]).features
        elif direction == "down" and r < self.rows-1:
            self.currentstate = self.__getitem__([r+1,c]).features
        elif direction == "":
            self.currentstate = self.currentstate

    def Reset(self):
        self.step = 0
        self.run = self.run+1
        self.currentstate = self.start