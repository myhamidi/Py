import unittest;import myTracer
import RL
import Agt
import Car
import random

class testCars(unittest.TestCase):
    def test_Init(self):
        testCars = [Car.typCar(0,20,0),Car.typCar(100,20,0),]
        self.assertEqual(testCars[0].Retxva(), (0,20,0))
        self.assertEqual(testCars[1].Retxva(), (100,20,0))
        # for c in range(testCars):
        #     a=1
        # testCar.gas()
        # testCar.gas()
        # self.assertEqual(testCar.RetCar(), (0.2,0.3,2))
        # testCar.roll()
        # testCar.roll()
        # self.assertEqual(testCar.RetCar(), (0.4,0.7,2))
        # testCar.brake()
        # self.assertEqual(testCar.RetCar(), (0.5,0.8,1))
        # testCar.brake()
        # self.assertEqual(testCar.RetCar(), (0.6,0.8,0))
        # testCar.brake()
        # self.assertEqual(testCar.RetCar(), (0.7,0.8,0))

class testCar(unittest.TestCase):
    def test_Basics(self):
        tCar = Car.typCar(0,20,0)
        tCar.SetA([(0.2,-4)])
        self.assertEqual(tCar.Retxva(), (0,20,0))
        tCar.Next()
        self.assertEqual(tCar.Retxva(), (2,20,0))
        tCar.Next()
        self.assertEqual(tCar.Retxva(), (3.98,19.6,-4))
    
    def test_Sets(self):
        tCar = Car.typCar(0,20,0)
        tCar.SetBrakings([0.1,0.4])
        tCar.SetAccelerations([0.2,0.3])
        tCar.SetA([(0.5,-4)])
                    # t = 0
        self.assertEqual(tCar.Retxva(), (0,20,0))
        tCar.Next() # t = 0.1
        self.assertEqual(tCar.Retxva(), (2,19.9,-1))
        tCar.Next() # t = 0.2
        self.assertEqual(tCar.Retxva(), (3.99,19.9,0))
        tCar.Next() # t = 0.3
        self.assertEqual(tCar.Retxva(), (5.99, 20.0, 1))
        tCar.Next() # t = 0.4
        self.assertEqual(tCar.Retxva(), (7.99, 20.0, 0))
        tCar.Next() # t = 0.5
        self.assertEqual(tCar.Retxva(), (9.97, 19.6, -4))

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
        testAgent.PerceiveState(testState.state,testState.reward)
        self.assertEqual(testAgent.RewStates[0].state,"ALF")
        self.assertEqual(testAgent.RewStates[0].reward,-1)

    def test_InitActions(self):
        testAgent = Agt.clsAgent(["up","down","left","right"])
        self.assertListEqual(sorted(testAgent.actions),["down","left","right","up",])
        self.assertIn(testAgent.RetNextAction(),["down","left","right","up",])

    def test_TerminalState(self):
        testAgent = Agt.clsAgent(["up","down","left","right"])
        self.assertEqual(testAgent.StateIsTerminal(),False)
        testAgent.PerceiveState("1",-1)
        testAgent.PerceiveState("2",-1)
        self.assertEqual(testAgent.StateIsTerminal(),False)
        testAgent.PerceiveState("3terminal",-1)
        self.assertEqual(testAgent.StateIsTerminal(),True)

class testEnv(unittest.TestCase):
    def test_SetTerminalState(self):
        testEnv = RL.clsEnvironment(3,5,-1)
        testEnv.setTerminalStates([(0,0),(2,3)])
        self.assertEqual(testEnv.EnvStates[0][0].terminal,True)
        self.assertEqual(testEnv.EnvStates[2][3].terminal,True)
        self.assertEqual(testEnv.EnvStates[0][0].reward,0)
        self.assertEqual(testEnv.EnvStates[2][3].reward,0)
        self.assertEqual(testEnv.EnvStates[1][4].terminal,False)
        testEnv.InitRun((2,3))
        self.assertEqual(testEnv.RetCurrentEnvState()[-8:],"terminal")

    def test_initRun(self):
        testEnv = RL.clsEnvironment(3,5,-1)
        testEnv.move("right")
        self.assertEqual(testEnv.step,1)
        testEnv.move("right")
        self.assertEqual(testEnv.step,2)
        testEnv.InitRun((2,3))
        self.assertEqual(testEnv.step,0)
        self.assertEqual(testEnv.run,1)

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
        self.assertEqual(testEnv.run,0)
    
    def test_clsGrid(self):
        testGrid = RL.clsGrid(5,10)
        self.assertEqual(len(testGrid.element),5)
        self.assertEqual(len(testGrid.element[0]),10)

if __name__ == '__main__':
    unittest.main()
