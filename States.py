import pandas as pd
import numpy as np

# ==============================================================================
# -- API -----------------------------------------------------------------------
# ==============================================================================

class typState:
    def __init__(self, features = [] , reward = 0.0, Q = [], QUpdates = 0):
        self.features = features
        self.reward = [reward, [reward]]
        self.Q = Q
        self.QUpdates = QUpdates

class clsStatesTable():
    def __init__(self, CopyFrom = ""):
        self.items = []
        self.len = 0
        if not CopyFrom == "":
            assert str(type(CopyFrom)) == "<class 'States.clsStatesTable'>"
            for i in range(CopyFrom.len):
                f = [CopyFrom[i].features[j] for j in range(len(CopyFrom[i].features))]
                q = [CopyFrom[i].Q[j] for j in range(len(CopyFrom[i].Q))]
                self.items.append(typState(f, Q=q))
                self.items[-1].reward = CopyFrom[i].reward  #reference
                self.len +=1

    def __getitem__(self,idx):
        if str(type(idx)) == "<class 'int'>":
            try:
                return self.items[idx]
            except:
                return None
        if str(type(idx)) == "<class 'list'>":
            try:
                sIdx = [state.features for state in self.items].index(idx)
                return self.items[sIdx]
            except:
                return None

    def Update(self, state, reward=0, Q=[0]):
        return self.xUpdate(state, reward, Q)

    def Sort(self):
        return self.xSort()

    def AsList(self, SRQ = "S"):
        return self.xAsList(SRQ)

    def Export(self, path):
        return self.xExport(path)
    
    def Import(self, path):
        return self.xImport(path)

    def Reset(self):
        self.items = []
        self.len = 0
# ==============================================================================
# -- x -------------------------------------------------------------------------
# ==============================================================================

    def xUpdate(self, state, reward, Q):
        if np.array(state).ndim == 1:
            if state == [0]:
                return
            for i in range(len(self.items)):
                if state == self.items[i].features: 
                    if not reward in self.items[i].reward[1]:
                        self.items[i].reward[1].append(float(reward))
                        self.items[i].reward[0] = float(sum(self.items[i].reward[1])/len(self.items[i].reward[1]))
                    if not sum(Q) == 0:
                        self.items[i].Q = Q
                    return
            self.items.append(typState(features = state, reward=float(reward), Q =Q))
            self.len += 1
            return
        if np.array(state).ndim == 2:
            if reward == 0:
                reward = [0 for i in range(len(state))]
            if Q == [0]:
                Q = [[0] for i in range(len(state))]
            for i in range(len(state)):
                self.xUpdate(state[i], reward[i], Q[i])
            return

    def xSort(self):
        n = self.len
        for i in range(n):
            for j in range(0, n-i-1):
                if self.items[j].features > self.items[j+1].features:
                    self.items[j], self.items[j+1] = self.items[j+1], self.items[j]
        return
 
    def xAsList(self, SRQ):
        if SRQ == "S":
            return [self.items[i].features for i in range(self.len)]
        if SRQ == "Q":
            return [self.items[i].Q for i in range(self.len)]

# ==============================================================================
# -- Import --------------------------------------------------------------------
# ==============================================================================
    def xImport(self,dataset_path):
        QImport = pd.read_csv(dataset_path, skiprows = 0, na_values = "?", \
        comment='\t', sep="|", skipinitialspace=True, error_bad_lines=False)

        for col, _ in QImport.iterrows():
            features = QImport.at[col, "State"].replace("[","").replace("]","").split(",")
            Q = QImport.at[col, "Q"].replace("[","").replace("]","").split(",")
            QUpdates = QImport.at[col, "QUpdates"]
            for i in range(len(features)): features[i] = float(features[i]); features[-1] = int(features[-1])
            for i in range(len(Q)): Q[i] = float(Q[i])
            self.xUpdate(features, 0, Q)

# ==============================================================================
# -- Export --------------------------------------------------------------------
# ==============================================================================
    def xExport(self, path):
        Qpd = pd.DataFrame() 
        Qpd["State"] = [state.features for state in self.items] 
        Qpd["Q"] = [state.Q for state in self.items] 
        Qpd["QUpdates"] = [state.QUpdates for state in self.items] 
        Qpd.to_csv(path, sep='|', encoding='utf-8', index = False) 