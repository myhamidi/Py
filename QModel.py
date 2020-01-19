import NN
import numpy as np

# ==============================================================================
# -- API -----------------------------------------------------------------------
# ============================================================================== 

class clsQModel():
    def __init__(self, actionlist, featurelist):
        self.features = featurelist
        self.actions = actionlist
        self.batch = 0
        
    def SetUp(self, Typ = "QSAI", nHidden = 1, Nrns = 64, Act = 'relu', alpha = 0.1, gamma = 1, batch = 100):
        self.QModelType = Typ
        self.QModelArch = [nHidden, Nrns, Act]
        self.alpha = alpha
        self.gamma = gamma
        self.batch = batch
        self.QModel = NN.clsNN(\
            NumInput = len(self.features)-1+len(self.actions),\
            NumLayers = nHidden,\
            NumOutputs = 1,\
            NeuronsHidden = Nrns,\
            ActHidden=Act,\
            FreezeModel=[],\
            Type="STD")
    def Train(self, FromSequence, Bellman_Iterations=1, StopAt=[1.0e-03,0]):
        return self.xTrain(FromSequence, Bellman_Iterations, StopAt=StopAt)

    def TrainToReward(self, FromSequence, StopAt=[1.0e-03,0]):
        return self.xTrainQToReward(FromSequence, StopAt=StopAt)

    def Predict(self, X, rund = None):
        return self.xQModelPredict(X, rund)

    def ExportWeights(self, path, prefix):
        return self.xQModelExportWeights(path, prefix)

    def ImportWeights(self, path):
        return self.xQModelImportWeights(path)

# ==============================================================================
# -- Train ---------------------------------------------------------------------
# ==============================================================================   

    def xTrainQToReward(self, FromSequence, StopAt=[1.0e-03,0]):
        SequenceSample = FromSequence.ReturnSample(self.batch)
        Xs, _, As, Rs, _ = SequenceSample.AsList()
        X_01 = self._RetXActAs01(Xs,As)
        R = Rs
        if FromSequence.Nterminal > 0:
            SequenceTerminal = FromSequence.ReturnSample(idxs=FromSequence.ReturnIdx(1))
            _, Xt, _, _, Rt = SequenceTerminal.AsList(multi=4)
            At = [j for _ in range(SequenceTerminal.len) for j in range(len(self.actions))]
            X_01 = self._RetXActAs01(Xs+Xt,As+At)
            R = Rs+Rt
        # Fit
        NN.ModelFit(self.QModel[0], np.array(X_01), np.array(R), Epochs=100, StopAt=StopAt)

    def xTrain(self, FromSequence, BellmanIterations, StopAt=[1.0e-03,0]):
        # Terminal States
        if FromSequence.Nterminal > 0:
            SequenceTerminal = FromSequence.ReturnSample(idxs=FromSequence.ReturnIdx(1))
            _, Xt, _, _, Rt = SequenceTerminal.AsList(multi=4)
            At = [j for _ in range(SequenceTerminal.len) for j in range(len(self.actions))]

        for k in range(BellmanIterations):
            # Non Terminal States
            SequenceSample = FromSequence.ReturnSample(self.batch)
            X0s, X1s, As, Rs, _ = SequenceSample.AsList()
            # Q under current policy
            Qpolicy_X0 = self.Predict(X0s)
            Qpolicy_X1 = self.Predict(X1s)
            QpAcn_X0 = [Qpolicy_X0[i][As[i]] for i in range(len(Qpolicy_X0))]
            QpMax_X1 = [max(Qpolicy_X1[i]) for i in range(len(Qpolicy_X1))]
            # taget Q
            QtAcn_X0 = [QpAcn_X0[i] + self.alpha*(Rs[i] + QpMax_X1[i] - QpAcn_X0[i]) for i in range(len(QpAcn_X0))]
            if FromSequence.Nterminal > 0:
                X0s = X0s+Xt
                As = As + At
                QtAcn_X0 = QtAcn_X0+Rt
            # Generate X As Combination of State and Action
            XA = self._RetXActAs01(X0s,As) # MOHI
            print("Iteration"+str(k))
            # Fit
            NN.ModelFit(self.QModel[0], np.array(XA), np.array(QtAcn_X0), Epochs=100, StopAt=StopAt)
        return

    def _RetXActAs01(self, X, ActIdx):
        retX = []
        for i in range(len(X)):
            retX.append(X[i] + [0]*len(self.actions))
            retX[i][ActIdx[i]+len(X[0])] = 1
        return retX

# ==============================================================================
# -- Predict -------------------------------------------------------------------
# ==============================================================================   

    def xQModelPredict(self, Xraw, rund = None):
        Xx = []; Ax = []; Q = []; la = len(self.actions)
        # Extend X to X+Actions 
        for state in Xraw:
            Q.append([0]*4)
            for j in range(len(self.actions)):
                if str(type(Xraw[0][-1])) == "<class 'int'>":
                    Xx.append(state[:-1])
                else:
                    Xx.append(state)
                Ax.append(j)
        X = self._RetXActAs01(Xx,Ax)
        # Predict
        Q01np = NN.ModelPredict(self.QModel[0],X)
        # Reduce Output to State
        Q01 = [float(Q01np[i][0]) for i in range(len(Q01np))]
        for i in range(len(Q01)):
            if rund == None:
                Q[i//la][i%la] = Q01[i]
            else:
                Q[i//la][i%la] = round(Q01[i], rund)
        return Q      

# ==============================================================================
# -- Import Export--------------------------------------------------------------
# ==============================================================================   

    def xQModelExportWeights(self, path, prefix):
        if self.QModelType == "QSAI":
            NN.ExportModelWeights(self.QModel[0], path, prefix + "_")

    def xQModelImportWeights(self,path):
        if self.QModelType == "QSAI":
            NN.ImportModelWeights(self.QModel[0], path)
