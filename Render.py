import tkinter as tk

class clsGrid:
    def __init__(self,rows,cols, text):
        self.limit_cols = cols
        self.limit_rows = rows
        self.text = text
        self.TextHeight = 50
        self.master = tk.Tk()
        self.can = tk.Canvas(self.master, width=cols*50, height=self.TextHeight+rows*50)
        self.can.pack()
        self.element = [[self.can.create_rectangle(50*i, self.TextHeight+50*j, 50*i+50, self.TextHeight+50+50*j, fill="white") for i in range(cols)] for j in range(rows)]
        self.txt_elements = [[self.can.create_text((25+50*i, self.TextHeight+25+50*j), text=str(i)+str(j)) for i in range(cols)] for j in range(rows)]
        self.txt_header = self.can.create_text((cols*50/2, self.TextHeight/2), text=self.text)
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