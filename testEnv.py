import Env as Envr

#Test1
Env = Envr.clsEnv("Grid",[9,10,-1]) 
retStr = "Rows: 9"+"\n";retStr += "Cols: 10"+"\n";retStr +="Initial Reward: -1"
assert Env.Info() == retStr, "Test1 failed"

#Test2
Env.SetStart([2,3])
assert Env.RetState() == [2, 3, 0],"Test2 failed"

#Test3
Env.SetState([2,3],1)
assert Env.RetState() == [2, 3, 1],"Test3.1 failed"
Env.SetStart([2,3])
assert Env.RetState() == [2, 3, 1],"Test3.2 failed"
Env.SetState([2,3],0)
assert Env.RetState() == [2, 3, 0],"Test3.3 failed"

#Test4
Env.SetState([4,5],reward = -2)
assert Env.RetReward() == -1,"Test4.1 failed"
assert Env.RetReward([4,5]) == -2,"Test4.2 failed"

#Test5
assert Env.RetActions() == ["up","down","left","right"],"Test5 failed: " + str(Env.RetActions())

#Test6
assert Env.RetEnvFeatures() == ["x","y","terminal"], "Test6 failed :" + str(Env.RetStateFeatures())
# print(Env.Info())

#Test7
Env.SetState([2,3])
assert Env.RetState() == [2, 3, 0], "Test7 failed"
Env.Step("left")
assert Env.RetState() == [2, 2, 0], "Test7 failed"
Env.Step("up")
assert Env.RetState() == [1, 2, 0], "Test7 failed"
Env.Step("right")
assert Env.RetState() == [1, 3, 0], "Test7 failed"
Env.Step("down")
assert Env.RetState() == [2, 3, 0], "Test7 failed"

# Test
Env = Envr.clsEnv("Grid",[3,4,-1]) 
Env.SetStart([2,3])
assert Env.RetState() == [2, 3, 0],Env1.RetState()
assert Env.RetStateAsGrid() == [[0,0,0,0],[0,0,1,0],[0,0,0,0]],Env.RetStateAsGrid()