import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None

from tensorflow import keras
from tensorflow.keras import layers

class clsNN:
    def __init__(self, NumInput, NumLayers, NumOutputs = 1, NeuronsEachLayer = 8, ActFunction = 'relu'):
      self.model = keras.Sequential()
      self.modelLoss = 0
      
      # First  Layer:
      if NumLayers == 0:
        self.model.add(layers.Dense(1, input_shape=(NumInput,), activation='linear'))
      else:
        self.model.add(layers.Dense(NeuronsEachLayer, input_shape=(NumInput,), activation=ActFunction))
      # Further Layers:
      if NumLayers > 1:
        for _ in range(NumLayers-1):
          self.model.add(layers.Dense(NeuronsEachLayer, activation=ActFunction))    
      # Last Layer:
      if NumLayers > 0:
          self.model.add(layers.Dense(NumOutputs, activation='linear'))
        
      self.model.compile(optimizer='adam', loss='mean_squared_error')
      
    def fit_model(self,X,y,TrainEpochs):
      self.logg = self.model.fit(X, y, verbose=0, validation_split=0, epochs=TrainEpochs)
      self.modelLoss = self.logg.history['loss'][TrainEpochs-1]
      
    def RetWeights(self):
      weights = []
      for layer in self.model.layers:
        weights.append(layer.get_weights()) # list of numpy arrays
      return weights

    def return_modelLoss(self):
      return self.modelLoss
    
    def predict(self, x):
      return self.model.predict(x)
    
    def predictQmax(self,x,nactions):
      #add actionCols:
      out = []
      for i in range(nactions):
        for j in range(nactions):
          x["baction"+str(j)] = 0
          if i == j:
            x["baction"+str(j)] = 1
        npx = self.predict(np.expand_dims(x, axis=0)) #convert to numpy. Model.Predict needs expand dims in case of single sample
        out.append(npx[0][0])
      print(out, max(out))
      return max(out)    
    
    def SetWeights(self, weights):
      i = 0
      for layer in self.model.layers:
        #weights:
        layer.set_weights(weights[i])
        i = i+1
    
    # Make new Q Target
    def UpdateQ(self,seqX, seqT, seqA, seqR, nactions):
      X = pd.concat([seqX, seqA], axis=1, sort=False)
      Qold = self.predict(X)
      self.predictQmax(seqX.iloc[5406,:], nactions)
      Qnew = pd.DataFrame(columns=["Q"], index=range(len(X))); Qnew["Q"] = 0.01
      for i in range(len(X)-1):
        if seqT["terminal"][i] == 0:
          Qnew["Q"][i] = seqR["reward rel"][i] + Qold[i+1]
      return Qnew
    
    def CheckMaxDeltaPrediction(self, X, Target, MaxDelta):
      errPredictions = pd.DataFrame(columns=["index", "feat0", "PreditedTarget", "Target"])
      PredictedTarget = self.predict(X)
      for i in range(len(Target)):
        if abs(PredictedTarget[i]-Target["Q"][i]) > MaxDelta:
          errPredictions.loc[len(errPredictions)] = [i, X.iloc[i,0], PredictedTarget[i], Target["Q"][i]]
      return errPredictions