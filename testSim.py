import CCSim
StartSpeed = 80

testSim = CCSim.clsCCSim(StartSpeed,StartSpeed/3)

testSim.setAccBehaviour([(0.1,1)],[(0.1,-1)])

testSim.RunSim()
