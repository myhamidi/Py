import numpy as np 

class clsApproximator:
    def LinearRegression(self,a,b):
        assert len(a) == len(b), "input vectors x does not have same length as y"
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
