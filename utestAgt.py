import Agt

class clsTest:
    def __init__(self):
        self.c = 0

    def test_EQ(self, a, b):
        self.c +=1
        if str(a) == str(b):
            print("Test " + str(self.c) + " passed")
        else:
            print("Test " + str(self.c) + " failed. Expected:" + str(b) + "Output was:" + str(a))

Agt = Agt.clsAgent(["high", "low"])
T = clsTest()

T.test_EQ(len(Agt.Sequence),0) 
for i in range(5):
    Agt.perceiveState([i,10-i,0],-i%2)
T.test_EQ(len(Agt.Sequence),10) 

T.test_EQ(Agt.batchsize,64) 
Agt.setModelTrainingParameter(batchsize=4)
T.test_EQ(Agt.batchsize,4) 

T.test_EQ(Agt.SequenceSample,[])
Agt.perceiveState([2,2,1],-1, tabular=False)
Agt.perceiveState([2,2,1],-1, tabular=False)
print(Agt.SequenceSamplePD)
testpd= Agt._ReturnPDFromSequence(Agt.SequenceSample, SplitState=True, SplitActions=True)
print(testpd)
testX = Agt._ReturnColsByKeywords(testpd,["0feat","blaction"])
print(testX)