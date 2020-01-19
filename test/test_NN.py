import sys
sys.path.append("C:\\temp Daten\\Lernbereich\\Git\\myhamidi\\Py")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from tensorflow import keras
from tensorflow.keras import activations

import NN
# import NNS

x1 = np.linspace(-2,2,110)
x2 = np.linspace((-2,-2),(2,2),110)
def f20(x): 
    return x**2

def f21(x): 
    return x**2-3*x+4

def plot(X,Y, Ynn):
    plt.scatter(X,Y)
    plt.scatter(X,Ynn)
    plt.plot([np.min(X)-0.1,np.max(X)+0.1],[0,0],color='black', linewidth=2)
    plt.plot([0, 0],[-1,np.max(Y)+0.1],color='black', linewidth=2)
    plt.axis([np.min(X)-0.1, np.max(X)+0.1, np.min(Y)-0.1, np.max(Y)+0.1])
    plt.grid(True, which='both')
    plt.show()

# ==============================================================================
# -- Testing Functions ----------------------------------------------------------
# ==============================================================================

ModelTypes = ["STD","SL","SL2","SI"]
# Test Init - Number Layers 1
def test_ModelLayer():
    for typ in ModelTypes:
        for i in range(4):
            cl = i+1 if typ == "SL2" and i >0 else 0
            NNx = NN.clsNN(1,i,1,Type=typ)
            assert len(NNx.model) == 1                  # Only One Model (one Output)                  
            assert len(NNx.model[0].layers) == i + 2 + cl  # i+ Input and Output Layer

# Test Init - Number Models/Outputs 2
def test_ModelOut():
    for typ in ModelTypes:
        for i in range(1,4):
            NNx = NN.clsNN(1,1,i,Type=typ)
            if typ == "STD":
                assert len(NNx.model) == 1
            else:                                    
                assert len(NNx.model) == i


# Test ModelFit and Model Predict
def review_ModelFit():
    for typ in ModelTypes:
        NNx = NN.clsNN(1,1,1,Type=typ)
        NN.ModelFit(NNx.model[0],x1,f20(x1), Epochs=10, StopAt=[1.0e-3])
        Ynn = NN.ModelPredict(NNx.model[0],x1)
        plot(x1,f20(x1),Ynn)

# Test ModelFit and Model Predict
def review_ModelFitMultiOut():
    typ = "STD"
    NNx = NN.clsNN(1,1,2,Type=typ)
    Y = np.swapaxes([f20(x1), f21(x1)],0,1)
    NN.ModelFit(NNx.model[0],x1,Y, Epochs=10, StopAt=[1.0e-2])
    Ynn = np.swapaxes(NN.ModelPredict(NNx.model[0],x1),0,1)
    plot(x1,f20(x1),Ynn[0])
    plot(x1,f21(x1),Ynn[1])

    typs = ["SI", "SL", "SL2"]
    for typ in typs:
        NNx = NN.clsNN(1,1,2,Type=typ)
        NN.ModelFit(NNx.model[0],x1,f20(x1), Epochs=10, StopAt=[1.0e-2])
        NN.ModelFit(NNx.model[1],x1,f21(x1), Epochs=10, StopAt=[1.0e-2])
        Ynn = [NN.ModelPredict(NNx.model[0],x1), NN.ModelPredict(NNx.model[1],x1)]
        plot(x1,f20(x1),Ynn[0])
        plot(x1,f21(x1),Ynn[1])

# Test ModelFit and Model Predict with Freeze
def test_ModelFitandFreez1():
    typs = ["SL", "SL2"]
    for typ in typs:
        NNx = NN.clsNN(1,1,2, Type=typs[0], FreezeModel=[1])
        NN.ModelFit(NNx.model[0],x1,f20(x1), Epochs=10, ReTry=100, StopAt=[1.0e-2])
        oldw = list(NNx.model[0].layers[1].get_weights()[0][0])
        NN.ModelFit(NNx.model[1],x1,f21(x1), Epochs=10, ReTry=100, StopAt=[1.0e-2])
        assert list(NNx.model[0].layers[1].get_weights()[0][0]) == \
                list(NNx.model[1].layers[1].get_weights()[0][0]), "shared layer weights not identical"
        assert not list(NNx.model[0].layers[2].get_weights()[0][0]) == \
                list(NNx.model[1].layers[2].get_weights()[0][0]), "last /parallel layer weights identical"
        assert oldw == list(NNx.model[0].layers[1].get_weights()[0][0]), "frozen weights changed"

# Test Export Import Weights SL
def test_NN_ExportImportWeights():
    typ = "STD"
    NN1 = NN.clsNN(3,1,4,Type=typ)
    NN2 = NN.clsNN(3,1,4,Type=typ)
    # NN.ModelFit(NN1.model[0],x1,f20(x1), Epochs=10, ReTry=100, StopAt=[1.0e-2])
    NN.ExportModelWeights(NN1.model[0],"csv/test/exports/","TestNN_ImpExp" + typ + "_")
    for i in range(1,3):
        w1 = list(NN1.model[0].layers[i].get_weights()[0][0]) 
        w2 = list(NN2.model[0].layers[i].get_weights()[0][0])
        assert not w1 == w2
    NN.ImportModelWeights(NN2.model[0],"csv/test/exports/TestNN_ImpExp" + typ + "_3-relu64-linear4.h5")
    for i in range(1,3):
        w1 = list(NN1.model[0].layers[i].get_weights()[0][0]) 
        w2 = list(NN2.model[0].layers[i].get_weights()[0][0])
        assert w1 == w2, "layer " + str(i) + " weights not identical"

test_ModelLayer();print("test_ModelLayer()")
test_ModelOut();print("test_ModelOut()")
review_ModelFit();print("review_ModelFit()")
review_ModelFitMultiOut();print("review_ModelFitMultiOut()")
test_ModelFitandFreez1();print("test_ModelFitandFreez1()")
test_NN_ExportImportWeights();print("test_NN_ExportImportWeights()")