import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None

from tensorflow import keras
from tensorflow.keras import Model
from tensorflow.keras import layers
from tensorflow.keras import activations
from tensorflow.keras import metrics

# ==============================================================================
# -- API -----------------------------------------------------------------------
# ============================================================================== 

class clsNN:
    def __init__(self, NumInput, NumLayers, NumOutputs, \
            NeuronsHidden = 64, \
            ActHidden = 'relu', \
            ActOut = 'linear', \
            learning_rate = 0.001, \
            FreezeModel = [], \
            Type = "STD"\
    ):
        self.mInfo = [NumInput, NumLayers, NumOutputs, NeuronsHidden,\
                    ActHidden, ActOut, learning_rate, FreezeModel, Type]
        mI = self.mInfo
        if Type == "STD":
            self.model = _RetModel(mI[0], mI[1], mI[2], mI[3], mI[4], mI[5], mI[6], mI[7])
        if Type == "SL":
            self.model = _RetModelSharedLayer(mI[0], mI[1], mI[2], mI[3], mI[4], mI[5], mI[6], mI[7])
        if Type == "SL2":
            self.model = _RetModelSharedLayer2(mI[0], mI[1], mI[2], mI[3], mI[4], mI[5], mI[6], mI[7])        
        if Type == "SI":
            self.model = _RetModelSharedInput(mI[0], mI[1], mI[2], mI[3], mI[4], mI[5], mI[6])
        if Type not in ["STD","SL","SI", "SL2"]:
            assert False

    def __getitem__(self,idx):
        try:
            return self.model[idx]
        except:
            return None

# ==============================================================================
# -- Functions -----------------------------------------------------------------
# ==============================================================================

def _RetModel(NumInput, NumLayers, NumOutputs, NeuronsHidden, \
          ActHidden, ActOut, learning_rate, FreezeModel):
    model = []
    yIn = layers.Input(shape=(NumInput,))
    yHidden = [layers.Dense(NeuronsHidden,activation=ActHidden) for i in range(NumLayers)]
    yOut = layers.Dense(NumOutputs, activation=ActOut)

    if NumLayers == 0:  
        Nodes = [yIn]
    if NumLayers > 0: 
        Nodes = [yHidden[0](yIn)] 
    if NumLayers > 1: 
        for i in range(NumLayers-1):
            Nodes = [yHidden[i+1](Nodes[-1])]
    LastNode = yOut(Nodes[-1])
    model.append(Model(inputs=yIn, outputs=LastNode))
    adam = keras.optimizers.Adam(learning_rate=learning_rate) 
    model[0].compile(optimizer=adam, loss='mean_squared_error')
    return model

def _RetModelSharedLayer(NumInput, NumLayers, NumOutputs, NeuronsHidden, \
          ActHidden, ActOut, learning_rate, FreezeModel):
    model = []
    # Layers. Hidden Layers are shared
    yIn = layers.Input(shape=(NumInput,))
    yHidden = [layers.Dense(NeuronsHidden,activation=ActHidden) for i in range(NumLayers)]
    yOut = [layers.Dense(1, activation=ActOut) for i in range(NumOutputs)]

    # Nodes
    if NumLayers == 0:  Nodes = [yIn]
    if NumLayers > 0: Nodes = [yHidden[0](yIn)] 
    for i in range(0,NumLayers-1):
        Nodes.append(yHidden[i+1](Nodes[-1]))

    # OutputNode and Model:
    for i in range(NumOutputs):
        for j in range(NumLayers): yHidden[j].trainable = True
        if i in FreezeModel: 
            for j in range(NumLayers): yHidden[j].trainable = False
        LastNode = yOut[i](Nodes[-1])
        model.append(Model(inputs=yIn, outputs=LastNode))
        adam = keras.optimizers.Adam(learning_rate=learning_rate) 
        model[i].compile(optimizer=adam, loss='mean_squared_error')
    return model 

def _RetModelSharedInput(NumInput, NumLayers, NumOutputs, NeuronsHidden, \
          ActHidden, ActOut, learning_rate):
    model = []
    # Layers. Input Layer is shared
    yIn = layers.Input(shape=(NumInput,))
    yHidden = [[layers.Dense(NeuronsHidden,activation=ActHidden) for i in range(NumLayers)] \
              for i in range(NumOutputs)]
    yOut = [layers.Dense(1, activation=ActOut) for i in range(NumOutputs)]

    # Nodes
    if NumLayers == 0:  
        Nodes = [yIn]

    # OutputNode and Model:
    for i in range(NumOutputs):
        if NumLayers > 0: 
            Nodes = [yHidden[i][0](yIn)] 
        if NumLayers > 1:
            for j in range(0,NumLayers-1):
                Nodes.append(yHidden[i][j+1](Nodes[-1]))
        LastNode = yOut[i](Nodes[-1])
        model.append(Model(inputs=yIn, outputs=LastNode))
        adam = keras.optimizers.Adam(learning_rate=learning_rate) 
        model[i].compile(optimizer=adam, loss='mean_squared_error')
    return model 

def _RetModelSharedLayer2(NumInput, NumLayers, NumOutputs, NeuronsHidden, \
          ActHidden, ActOut, learning_rate, FreezeModel):
    model = []
    # Layers. Hidden Layers are shared
    yIn = layers.Input(shape=(NumInput,))
    yHidden = [layers.Dense(NeuronsHidden/2, activation=ActHidden) for i in range(NumLayers)]
    yHidden2 = [[layers.Dense(NeuronsHidden/2, activation=ActHidden) for i in range(NumLayers)] \
            for i in range(NumOutputs)]
    yOut = [layers.Dense(1, activation=ActOut) for i in range(NumOutputs)]

    # Nodes
    if NumLayers == 0:  
        Nodes = [yIn]

    # OutputNode and Model:
    for i in range(NumOutputs):
        for j in range(NumLayers):
            yHidden[j].trainable = True
            if i in FreezeModel: 
                yHidden[j].trainable = False
        if NumLayers == 1: 
            Node1 = yHidden[0](yIn)
            Node2 = yHidden2[i][0](yIn)
            Nodes = [keras.layers.concatenate([Node1, Node2])]
        if NumLayers == 2: 
            Node1 = yHidden[1](yHidden[0](yIn))
            Node2 = yHidden2[i][1](yHidden2[i][0](yIn))
            Nodes = [keras.layers.concatenate([Node1, Node2])]
        if NumLayers == 3: 
            Node1 = yHidden[2](yHidden[1](yHidden[0](yIn)))
            Node2 = yHidden2[i][2](yHidden2[i][1](yHidden2[i][0](yIn)))
            Nodes = [keras.layers.concatenate([Node1, Node2])]
        LastNode = yOut[i](Nodes[-1])
        model.append(Model(inputs=yIn, outputs=LastNode))
        adam = keras.optimizers.Adam(learning_rate=learning_rate) 
        model[i].compile(optimizer=adam, loss='mean_squared_error')
    return model

# ==============================================================================
# -- Global Functions ----------------------------------------------------------
# ==============================================================================

def ModelFit(model, X, Y, \
        StopAt = [0.1, 0.001], \
        Epochs = 10, \
        ReTry = 10**2, \
        PrintMode = True\
):
    lastLoss = 1000
    for i in range(ReTry):
        if PrintMode:
            model.fit(X, Y, verbose=0, validation_split=0, epochs=Epochs)
            Loss = model.evaluate(X,Y)
        else:
            Loss = model.fit(X, Y, verbose=0, validation_split=0, epochs=Epochs).history['loss'][-1]
        if Loss < StopAt[0]:
            break
        lastLoss = Loss
    return Loss

def ModelPredict(model, x, AsList = False):
    if type(x) == list:
        x = np.array(x)
    if AsList:
        return model.predict(x).tolist()
    else:
        return model.predict(x)

def ExportModelWeights(model, folder, name):
    # Generate the name of the file
    tmpStr = ""
    for layer in model.layers:
        try:
            _,a = layer.get_config()['batch_input_shape']
        except KeyError:
            a = layer.get_config()['activation'] + str(layer.get_config()['units'])
        tmpStr += str(a) + "-"
    # Save the Wegihts
    model.save_weights(folder + name + tmpStr[:-1] + ".h5")

def ImportModelWeights(model, path):
    model.load_weights(path)   
