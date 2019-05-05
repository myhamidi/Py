import myTracer;tr = myTracer.glTracer

import tkinter as tk

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
        self.limit_cols = cols
        self.limit_rows = rows
        self.step = 0

    def __getitem__(self,pos):
        tr.call("clsEnvironment.__getitem__")
        i,j = pos
        return self.EnvStates[i][j]

    def visualize_show(self,tim):
        tr.call("clsEnvironment.visualize_show")
        self.Grid.show(tim,self.step)

    def visualize_update(self):
        tr.call("clsEnvironment.visualize_update")
        self.Grid.update(self.currentposition)
    
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

class clsGrid:
    def __init__(self,rows,cols):
        tr.call("clsGrid.init")
        self.limit_cols = cols
        self.limit_rows = rows
        self.Frame = 0
        self.TextHeight = 50
        # <tkinter>
        self.master = tk.Tk()
        self.w = tk.Canvas(self.master, width=cols*50, height=self.TextHeight+rows*50)
        self.w.pack()
        self.element = [[self.w.create_rectangle(50*i, self.TextHeight+50*j, 50*i+50, self.TextHeight+50+50*j, fill="white") for i in range(cols)] for j in range(rows)]
        self.txt = [[self.w.create_text((25+50*i, self.TextHeight+25+50*j), text=str(i)+str(j)) for i in range(cols)] for j in range(rows)]
        self.txt_header = self.w.create_text((cols*50/2, self.TextHeight/2), text="Steps: " + str(self.Frame))
        self.w.itemconfig(self.element[0][0],fill="#3395E4")
        self.position = (0,0)

    def show(self,tim, steps):
        tr.call("clsGrid.show")
        self.Frame = steps
        if not tim == 99:
            self.master.after(tim, self.w.quit)
        tk.mainloop()

    def res(self):
        tr.call("clsGrid.res")
        self.element = [[self.w.create_rectangle(50*i, self.TextHeight+50*j, 50*i+50, self.TextHeight+50+50*j, fill="white") for i in range(self.limit_cols)] for j in range(self.limit_rows)]
        self.txt = [[self.w.create_text((25+50*i, self.TextHeight+25+50*j), text=str(j)+str(i)) for i in range(self.limit_cols)] for j in range(self.limit_rows)]
       

    def update(self,currentposition):
        tr.call("clsGrid.update")
        x,y = currentposition
        self.res()
        self.w.itemconfig(self.element[x][y],fill="#3395E4")
        self.w.itemconfig(self.txt_header,text="Steps: " + str(self.Frame))
