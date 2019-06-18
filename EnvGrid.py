import myTracer;tr = myTracer.glTracer
import tkinter as tk
import random
import os
import time

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
        self.Grid = clsGrid(rows,cols)
        self.currentposition = (0,0)
        self.start = (0,0)
        self.limit_cols = cols
        self.limit_rows = rows
        self.step = 0
        self.run = 0
        self.TKinterInit = False
        self.actions = ["up","down","left","right"]
        if rows == 1:
            self.actions = ["left","right"]
        if cols == 1:
            self.actions = ["up","down"]

    def __getitem__(self,pos):
        tr.call("clsEnvironment.__getitem__")
        i,j = pos
        return self.EnvStates[i][j]

    def SetRestartPosition(self,StartPosition):
        r,c = StartPosition
        if r >= 0 and r < self.limit_rows and c >= 0 and c < self.limit_cols:
            self.start = StartPosition
            self.currentposition = StartPosition
        else:
            print("error - SetStart")
    
    def SetRandomStart(self):
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
        if self.IsStateTerminal() == True:
            self.run += 1
            return str(self.currentposition) + "terminal1"
        return str(self.currentposition)

    def IsStateTerminal(self):
        tr.call("clsEnv.IsStateTerminal")
        row, col = self.currentposition
        if self.EnvStates[row][col].terminal==True:
            return True
        return False

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

    def Next(self,action):
        self.move(action)

    def Reset(self):
        self.step = 0
        self.run = self.run+1
        self.currentposition = self.start

    def render(self,tim,typ):
        if typ == "InConsole":
            self.render_Console(tim)
        if typ == "InTKinter":
            self.MonitorUpdate(tim)

    def render_Console(self,tim):
        GridString = "+-------+"
        emptyField = "| "
        egoField = "|o"
        tField = "|X"
        os.system('cls')
        for i in range(self.limit_rows):
            GridString += "\n"
            for j in range(self.limit_cols):
                if (i,j) == self.currentposition:
                    GridString += egoField
                elif self.EnvStates[i][j].terminal==True:
                    GridString += tField
                else:
                    GridString += emptyField
            GridString += "|" 
        GridString += "\n+-------+"
        GridString += "\n"
        GridString += "Position:" + str(self.currentposition)
        print(GridString)
        time.sleep(tim)
        os.system('cls')
    
    def MonitorUpdate(self,tim):
        tr.call("clsEnvironment.MonitorUpdate")
        if self.TKinterInit == False:
            self.Grid.show(int(tim*1000),0,0)
            self.TKinterInit = True
        terminal = False
        if "terminal" in str(self.RetState()):terminal = True
        self.Grid.update(self.currentposition,self.step,self.run,terminal)
        self.Grid.show(int(tim*1000),0,0)

class clsGrid:
    def __init__(self,rows,cols):
        tr.call("clsGrid.init")
        self.limit_cols = cols
        self.limit_rows = rows
        self.EnvSteps = 0
        self.EnvRuns = 0
        self.TextHeight = 50
        # <tkinter>
        self.master = tk.Tk()
        self.w = tk.Canvas(self.master, width=cols*50, height=self.TextHeight+rows*50)
        self.w.pack()
        self.element = [[self.w.create_rectangle(50*i, self.TextHeight+50*j, 50*i+50, self.TextHeight+50+50*j, fill="white") for i in range(cols)] for j in range(rows)]
        self.txt_elements = [[self.w.create_text((25+50*i, self.TextHeight+25+50*j), text=str(i)+str(j)) for i in range(cols)] for j in range(rows)]
        self.txt_header = self.w.create_text((cols*50/2, self.TextHeight/2), text="Run: " + str(self.EnvRuns) + ". Step: " + str(self.EnvSteps))
        self.w.itemconfig(self.element[0][0],fill="#3395E4")
        self.position = (0,0)

    def show(self,tim,steps,run):
        tr.call("clsGrid.show")
        self.EnvSteps = steps
        self.EnvRuns = run
        if not tim == 99:
            self.master.after(tim, self.w.quit)
        tk.mainloop()

    def res(self):
        tr.call("clsGrid.res")
        self.element = [[self.w.create_rectangle(50*i, self.TextHeight+50*j, 50*i+50, self.TextHeight+50+50*j, fill="white") for i in range(self.limit_cols)] for j in range(self.limit_rows)]
        self.txt_elements = [[self.w.create_text((25+50*i, self.TextHeight+25+50*j), text=str(j)+str(i)) for i in range(self.limit_cols)] for j in range(self.limit_rows)]
       

    def update(self,currentposition,step,run,terminal):
        tr.call("clsGrid.update")
        x,y = currentposition
        self.res()
        self.w.itemconfig(self.element[x][y],fill="#3395E4")
        if terminal == True: self.w.itemconfig(self.element[x][y],fill="#119111")
        self.w.itemconfig(self.txt_header,text="Run: " + str(run) + ". Step: " + str(step))
