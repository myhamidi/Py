import sys
sys.path.append("../")

import unittest
import Agt
Agt = Agt.clsAgent(["high", "low"])

class testAgt(unittest.TestCase):
    def test_IsFirstStepOfEpoch(self):
        self.assertEqual(Agt._IsFirstStepOfEpoch(), True)
        self.assertEqual(Agt._RetRewardOfLastSequenceStep(),0)

        Agt.perceiveState([1,0],-1)
        self.assertEqual(Agt._IsFirstStepOfEpoch(), False)
        self.assertEqual(Agt._RetRewardOfLastSequenceStep(),-1)

        Agt.perceiveState([2,0],-1)
        self.assertEqual(Agt._IsFirstStepOfEpoch(), False)
        self.assertEqual(Agt._RetRewardOfLastSequenceStep(),-2)

        Agt.perceiveState([3,1],-1)
        self.assertEqual(Agt._IsFirstStepOfEpoch(), True)
        self.assertEqual(Agt._RetRewardOfLastSequenceStep(),0)
        self.assertEqual(Agt.SequenceRewards[-1],(2,-3,0,""))

        Agt.perceiveState([4,0],-1)
        self.assertEqual(Agt._IsFirstStepOfEpoch(), False)
        self.assertEqual(Agt._RetRewardOfLastSequenceStep(),-1)

        Agt.perceiveState([2,0],-1)
        self.assertEqual(Agt._IsFirstStepOfEpoch(), False)
        self.assertEqual(Agt._RetRewardOfLastSequenceStep(),-2)

    def test_SequenceRewards(self):
        self.assertEqual(Agt.SequenceRewards[-5],(0,-1,0,"")) # action 0 can also mean "no action"
        self.assertEqual(Agt.SequenceRewards[-4],(1,-2,0,""))
        self.assertEqual(Agt.SequenceRewards[-3],(2,-3,0,""))
        self.assertEqual(Agt.SequenceRewards[-2],(3,-1,0,""))
        self.assertEqual(Agt.SequenceRewards[-1],(1,-2,0,"")) # this state "1" has been seen before

if __name__ == '__main__':
    unittest.main()