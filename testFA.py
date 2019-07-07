import csv
import fapprox as FA
import numpy

def writeData(vector, textfile,xwr): 
    f = open(textfile,xwr)
    f.write("x\n")
    for i in range(len(vector)):
        f.write(str(vector[i]) + "\n")

def readData(textfile):
    return numpy.loadtxt(open(textfile, "rb"), delimiter="|", skiprows=1)

x = readData("Features-x.csv")
y = readData("Feature-Q.csv")

Apx = FA.clsApproximator()

w = Apx.LinearRegression(x,y)

print(w)

