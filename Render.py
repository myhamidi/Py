# ==============================================================================
# -- API -----------------------------------------------------------------------
#
# Render.clsGrid(10,20,"")                                              | Initiate Render Grid
# Render.renderArray([[0,1,0],[0,0,0]], "Hello World",500)              | Display Grid with text for 500ms


import tkinter as tk

class clsGrid:
    def __init__(self,rows,cols, text):
        self.limit_cols = cols
        self.limit_rows = rows
        self.text = text
        self.TextHeight = 50; self.H = 50
        if cols > 20 or rows > 20: self.TextHeight = 20; self.H = 20
        if cols > 100 or rows > 100: self.H = 15
        self.master = tk.Tk()
        self.can = tk.Canvas(self.master, width=cols*self.H, height=self.TextHeight+rows*self.H)
        self.can.pack()
        self.element = [[self.can.create_rectangle(self.H*i, self.TextHeight+self.H*j, self.H*i+self.H, self.TextHeight+self.H+self.H*j, fill="white") for i in range(cols)] for j in range(rows)]
        self.txt_elements = [[self.can.create_text((self.H/2+self.H*i, self.TextHeight+self.H/2+self.H*j), text=str(j)+str(i)) for i in range(cols)] for j in range(rows)]
        self.txt_header = self.can.create_text((cols*self.H/2, self.TextHeight/2), text=self.text)
        self.TKinterInit = False

    def renderArray(self,twodarr,text,tim):
        #Text
        if not text == "":
            self.can.itemconfig(self.txt_header,text=text)
        #ColorFormat
        assert len(twodarr) == self.limit_rows,"Array size does not match to Grid Row size"
        for i in range(self.limit_rows):
            assert len(twodarr[i]) == self.limit_cols,"Array size does not match to Grid Col Size of Row " + str(i+1)
            for j in range(self.limit_cols):
                if twodarr[i][j] == 0:
                    self.SetColor((i,j),"#ffffff")
                if twodarr[i][j] == 1:
                    self.SetColor((i,j),"#3395E4")
                if twodarr[i][j] == 2:
                    self.SetColor((i,j),"#000000")
        #Render
        if self.TKinterInit == False:
            self.TKinterInit = True
            self.master.after(tim, self.can.quit)
            tk.mainloop()
        if self.TKinterInit == True:
            self.show(tim)
    
    def show(self,tim):
        self.can.update()
        self.master.after(tim)

    def SetColor(self,pos,color):
        x,y = pos
        self.can.itemconfig(self.element[x][y],fill=color)