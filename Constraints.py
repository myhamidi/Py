import pandas as pd
import numpy as np
import pandas as pd

class typConstraints:
    def __init__(self, featuresFrom = [] , featuresTo = [], ConstrainedActions = []):
        self.featuresFrom = featuresFrom
        self.featuresTo = featuresTo
        if featuresTo == []:
            self.featuresTo = featuresFrom
        self.ConstrainedActions = ConstrainedActions

# ==============================================================================
# -- API -----------------------------------------------------------------------
# ==============================================================================
class clsConstraints():
    def __init__(self, actionlist):
        self.items = []
        self.actions = actionlist
        self.len = 0

    def __getitem__(self,idx):
        if str(type(idx)) == "<class 'int'>":
            try:
                return self.items[idx]
            except:
                return None

    def Add(self, From, To = [], Allowed = [], Forbidden = []):
        return self.xAdd(From, To, Allowed, Forbidden)

    def RetActionList(self, state):
        return self.xRetActionList(state)

    def Import(self, path):
        return self.xImport(path)

    def Export(self, path):
        return self.xExport(path)
# ==============================================================================
# -- x -----------------------------------------------------------------------
# ==============================================================================

    def xAdd(self, From, To = [], Allowed = [], Forbidden = []):
        if Allowed == [] and not Forbidden == []:
            CA = [self.actions[i] for i in range(len(self.actions)) if self.actions[i] not in Forbidden]
            self.items.append(typConstraints(From, To, CA))
        if Forbidden == [] and not Allowed == []:
            self.items.append(typConstraints(From, To, Allowed))

    def xRetActionList(self, state):
        Cidxs = self._RetIdxsConstrainedState(state)
        if len(Cidxs)==0:
            return self.actions
        ret = self.items[Cidxs[0]].ConstrainedActions
        for idx in Cidxs:
            for action in ret:
                if not action in self.items[idx].ConstrainedActions:
                    ret.remove(action)
        return ret                                                      

    def _RetIdxsConstrainedState(self, state):
        ret = [i for i in range(len(self.items))]
        for i in range(len(self.items)):
            for j in range(len(self.items[i].featuresFrom)):
                if not self.items[i].featuresFrom[j] == None:
                    if self.items[i].featuresTo[j] < state[j] or \
                        state[j] < self.items[i].featuresFrom[j]:
                            ret.remove(i)
        return ret

    def xImport(self, path):
        Cpd = pd.read_csv(path, skiprows = 0, na_values = "?", \
        comment='\t', sep="|", skipinitialspace=True, error_bad_lines=False)

        for col, _ in Cpd.iterrows():
            SFm = Cpd.at[col, "StateFrom"].replace("[","").replace("]","").split(",")
            STo = Cpd.at[col, "StateTo"].replace("[","").replace("]","").split(",")
            Cst = Cpd.at[col, "Constraint"].replace("[","").replace("]","").split(",")

            for i in range(len(SFm)):
                if "None" in str(SFm[i]):
                    SFm[i] = None
                if not "None" in str(SFm[i]):
                    SFm[i] = float(SFm[i])
            for i in range(len(STo)):
                if "None" in str(STo[i]):
                    STo[i] = None
                if not "None" in str(STo[i]):
                    STo[i] = float(STo[i])
            for i in range(len(Cst)):
                Cst[i] = Cst[i].replace(" ","").replace("'","")
            self.xAdd(SFm, STo, Cst)

    def xExport(self, path):
        Cpd = pd.DataFrame() 
        Cpd["StateFrom"] = [item.featuresFrom for item in self.items] 
        Cpd["StateTo"] = [item.featuresTo for item in self.items] 
        Cpd["Constraint"] = [item.ConstrainedActions for item in self.items] 
        Cpd.to_csv(path, sep='|', encoding='utf-8', index = False) 