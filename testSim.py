import CCSim
speed = 80

testSim = CCSim.clsCCSim(speed,speed/3)

testSim.setAccBehaviour([(0.1,1)],[(0.1,-1)])

testSim.RunSim()
