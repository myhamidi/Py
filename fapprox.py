import numpy as np 

class clsApproximator:
    def __init__(self):
        self.x = np.array([])
        self.y = np.array([])

    def LinearRegression(self,a,b):
        assert len(a) == len(b), "input vectors a does not have same length as b"
        if type(a) is np.ndarray:
            x = a; y = b
        else:
            x = np.array(a); y = np.array(b)
        #ReShape:
        if len(x.shape) == 1:
            x = np.expand_dims(x,axis=0).T
        y = np.expand_dims(y,axis=0).T
        #Add Colum on "1" at index 0
        x = np.insert(x,0,1,axis=1)
        #Pseudoinverse
        x_pinv = np.linalg.pinv(x)
        #Getw
        w_x = np.dot(x_pinv,y)
        arr = []
        for i in range(len(w_x)):
            arr.append(w_x[i][0])
        return arr

    def NN(self,a,b,n_Neurons):
        assert len(a) == len(b), "input vectors a does not have same length as b"
        if type(a) is np.ndarray:
            x = a; y = b
        else:
            x = np.array(a); y = np.array(b)
        
        #ReShape:
        if len(x.shape) == 1:
            x = np.expand_dims(x,axis=0).T
        y = np.expand_dims(y,axis=0).T
        #Add Colum on "1" at index 0
        x = np.insert(x,0,1,axis=1)

        weights1 = np.random.rand(x.shape[1],n_Neurons) 
        weights2 = np.random.rand(n_Neurons,1) 
        # weights2 = np.ones((n_Neurons,1))

        # output1 = np.tanh(np.dot(x, weights1))
        # output2 = np.tanh(np.dot(output1, weights2))

        inner1 = np.dot(x, weights1)
        output1 = np.maximum(np.zeros(inner1.shape),inner1)
        inner2 = np.dot(output1, weights2)
        output2 = inner2

        #ReLu derivative
        dw2 = np.array(output2,copy = True)

        return output2