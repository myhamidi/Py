import unittest;import myTracer
import RL
import Agt
import random


class testAgent(unittest.TestCase):
    def test_typRewStat(self):
        testState = Agt.typRewState("-",1,2,-1)
        self.assertEqual(testState.state, "-")
        self.assertEqual(testState.reward, 1)
        self.assertEqual(testState.value, 2)
        self.assertEqual(testState.visited, -1)
    
    def test_Init(self):
        testAgent = Agt.clsAgent([])
        self.assertEqual(len(testAgent.RewStates),0)
        self.assertEqual(len(testAgent.SequenceRewards),0)
        self.assertEqual(len(testAgent.TransitionMatrix),0)
    
    def test_PerceiveStates(self):
        testState = Agt.typRewState("ALF",-1,0,0)
        testAgent = Agt.clsAgent([])
        testAgent.PerceiveState(testState)
        self.assertEqual(testAgent.RewStates[0].state,"ALF")
        self.assertEqual(testAgent.RewStates[0].reward,-1)

    def test_InitActions(self):
        testAgent = Agt.clsAgent(["up","down","left","right"])
        self.assertListEqual(sorted(testAgent.actions),["down","left","right","up",])
        self.assertIn(testAgent.RetNextAction(),["down","left","right","up",])

class testEnv(unittest.TestCase):
    def test_SetTerminalState(self):
        testEnv = RL.clsEnvironment(2,5,-1)
        testEnv.setTerminalStates([(0,0),(0,1)])
        self.assertEqual(testEnv.EnvStates[0][0].terminal,True)
        self.assertEqual(testEnv.EnvStates[0][1].terminal,True)
        self.assertEqual(testEnv.EnvStates[1][4].terminal,False)

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

if __name__ == '__main__':
    unittest.main()
