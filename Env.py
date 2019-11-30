import EnvCarla
import EnvGrid

class clsEnv:
    def __init__(self,name, Envparameters):
        self.name = name
        if name == "Grid":
            self.Env = EnvGrid.clsEnvironment(0,0,0,Envparameters)
# ==============================================================================
# -- Init ---------------------------------------------------------------------
# ==============================================================================      
    
    def SetStart(self,Start):
        self.Env.SetStartPosition(self,StartPosition)

# ==============================================================================
# -- Return ---------------------------------------------------------------------
# ==============================================================================     
    def Info(self):
        retStr = "Env Name not found"
        if self.name == "Grid":
            retStr = "Rows: " + str(self.Env.limit_rows) +"\n"
            retStr += "Cols: " + str(self.Env.limit_cols) +"\n"
            retStr += "Initial Reward: " + str(self.Env.ireward)
        return retStr