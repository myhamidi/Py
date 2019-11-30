# ==============================================================================
# -- API -----------------------------------------------------------------------
#
# Env.clsEnv("Grid",[10,10,-1])         | Initiate Environment Grid
# Env.SetStart([2,3])                   | Set Ego Start Position to [2,3]
# Env.RetStatue()                       | Return Reward of current state
# Env.RetReward()                       | Return Reward of current state
# Env.RetReward([4,5])                  | Return Reward of state [4,5]
# Env.RetActions()                      | Return Actions that can be applied to the environement
# Env.RetStateFeatures()                | Return Features used for State Representation
# ==============================================================================

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
    
    def SetStart(self,start):
        self.Env.SetStartPosition(start)
        return

    def SetState(self,state,terminal=-1,reward=-0.999):
        if not terminal == -1:
            assert terminal == 0 or terminal == 1
            self.Env.EnvStates[state[0]][state[1]].terminal = terminal
        if not reward == -0.999:
            self.Env.EnvStates[state[0]][state[1]].reward = reward
    # def SetStateDefinition(self,state,reward,terminal):

# ==============================================================================
# -- Step ---------------------------------------------------------------------
# ==============================================================================    

    def Step(self,action):
        self.Env.Next(action)

# ==============================================================================
# -- Return ---------------------------------------------------------------------
# ==============================================================================     
    def Info(self):
        retStr = "Env Name not found"
        if self.name == "Grid":
            retStr = "Rows: " + str(self.Env.rows) +"\n"
            retStr += "Cols: " + str(self.Env.cols) +"\n"
            retStr += "Initial Reward: " + str(self.Env.ireward)
        return retStr
    
    def RetState(self):
        return self.Env.RetStateFeatures()
    
    def RetReward(self,state = []):
        if state == []:
            return self.Env.RetReward()
        else:
            return self.Env.EnvStates[state[0]][state[1]].reward

    def RetActions(self):
        return self.Env.ReturnActionList()

    def RetStateFeatures(self):
        return self.Env.features