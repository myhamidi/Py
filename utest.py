import unittest;import myTracer
import RL
import random

class testInits(unittest.TestCase):
    def test_typGridState(self):
        testState = RL.typGridState(1,2,3,True)
        self.assertEqual(testState.x, 1)
        self.assertEqual(testState.y, 2)
        self.assertEqual(testState.reward, 3)
        self.assertEqual(testState.terminal, True)

    def test_clsEnvironment(self):
        testEnv = RL.clsEnvironment(2,5,-2)
        self.assertEqual(len(testEnv.EnvStates),2)
        self.assertEqual(testEnv.limit_rows,2)
        self.assertEqual(testEnv.limit_cols,5)
        self.assertEqual(len(testEnv.EnvStates[0]),5)
        self.assertEqual(testEnv.currentposition,(0,0))
        self.assertEqual(testEnv.step,0)
    
    def test_clsGrid(self):
        testGrid = RL.clsGrid(5,10)
        self.assertEqual(len(testGrid.element),5)
        self.assertEqual(len(testGrid.element[0]),10)
    
    def test_typRewStat(self):
        testState = RL.typRewState("-",1,2,-1)
        self.assertEqual(testState.state, "-")
        self.assertEqual(testState.reward, 1)
        self.assertEqual(testState.value, 2)
        self.assertEqual(testState.visited, -1)

if __name__ == '__main__':
    unittest.main()
