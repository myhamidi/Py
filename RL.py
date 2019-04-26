import tkinter as tk

class typGridState:
    def __init__(self,x,y,r,t):
        self.x=x
        self.y=y
        self.reward=r
        self.terminal=t

class typRewState:
    def __init__(self,stateStr,reward,value,visited):
        self.state = stateStr
        self.reward = reward
        self.value = value
        self.visited = visited
    
class clsEnvironment:
    def __init__(self,rows,cols,reward):
        self.EnvStates = [[typGridState(i,j,reward,False) for j in range(rows)] for i in range(cols)]
        self.Grid = clsGrid(rows,cols)

    def __del__(self):
            
      
    def __getitem__(self,pos):
        i,j = pos
        return self.EnvStates[i][j]

    def visualize(self,tim):
        self.Grid.start(tim)
    
    def move(self,direction):
        self.Grid.move(direction)

class clsGrid:
    def __init__(self,rows,cols):
        self.master = tk.Tk()
        self.w = tk.Canvas(self.master, width=rows*50, height=cols*50)
        self.w.pack()
        self.ele = [[self.w.create_rectangle(50*i, 50*j, 50*i+50, 50+50*j, fill="white") for i in range(4)] for j in range(4)]
        self.txt = [[self.w.create_text((25+50*i, 25+50*j), text=str(i)+str(j)) for i in range(4)] for j in range(4)]
        self.w.itemconfig(self.ele[0][0],fill="#3395E4")
        self.position = (0,0)

    def start(self,tim):
        if not tim == 99:
            self.master.after(tim, self.w.quit)
        tk.mainloop()

    def res(self):
        self.ele = [[self.w.create_rectangle(50*i, 50*j, 50*i+50, 50+50*j, fill="white") for i in range(4)] for j in range(4)]
        self.txt = [[self.w.create_text((25+50*i, 25+50*j), text=str(i)+str(j)) for i in range(4)] for j in range(4)]
       

    def move(self,direction):
        self.res()
        x,y = self.position
        if direction == "up":
            self.position = (x-1,y)
            self.w.itemconfig(self.ele[x-1][y],fill="#3395E4")
        elif direction == "down":
            self.position = (x+1,y)
            self.w.itemconfig(self.ele[x+1][y],fill="#3395E4")
        elif direction == "left":
            self.position = (x,y-1)
            self.w.itemconfig(self.ele[x][y-1],fill="#3395E4")
        elif direction == "right":
            self.position = (x,y+1)
            self.w.itemconfig(self.ele[x][y+1],fill="#3395E4")
