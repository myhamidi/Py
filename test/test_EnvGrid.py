import sys
sys.path.append("C:\\temp Daten\\Lernbereich\\Git\\myhamidi\\Py")

import EnvGrid

def test_Init():
    Env = EnvGrid.clsEnvironment(10,10,-1)
    assert Env.Reward([0,0]) == -1
    
    assert Env.Reward([0,0]) == -1
    Env.SetTerminalState([9,9],0)
    assert Env.Reward([9,9]) == 0

    assert Env.Reward([3,4]) == -1
    Env.SetReward([3,4],7)
    assert Env.Reward([3,4]) == 7

    assert Env.Reward() == -1
    assert Env.Reward([3,4]) == 7
    Env.SetStartPosition([3,4])
    assert Env.State() == [3,4,0], Env.State()
    assert Env.Reward() == 7

def test_move():
    Env = EnvGrid.clsEnvironment(3,3,-1)
    assert Env.State() == [0,0,0]
    assert Env.GridStateAsList() == [[1,0,0],[0,0,0],[0,0,0]]
    Env.Step("right")
    assert Env.State() == [0,1,0]
    assert Env.GridStateAsList() == [[0,1,0],[0,0,0],[0,0,0]]
    Env.Step("down")
    assert Env.State() == [1,1,0]
    assert Env.GridStateAsList() == [[0,0,0],[0,1,0],[0,0,0]]
    Env.Step("left")
    assert Env.State() == [1,0,0]
    assert Env.GridStateAsList() == [[0,0,0],[1,0,0],[0,0,0]]
    Env.Step("up")
    assert Env.State() == [0,0,0]
    assert Env.GridStateAsList() == [[1,0,0],[0,0,0],[0,0,0]]

def test_terminal():
    Env = EnvGrid.clsEnvironment(10,10,-1)
    Env.SetTerminalState([9,9],0)
    for i in range(8):
        Env.Step("down")
        Env.Step("right")
    Env.Step("down")
    assert Env.State() == [9,8,0]
    assert Env.Reward() == -1
    Env.Step("right")
    assert Env.State() == [9,9,1]
    assert Env.Reward() == 0
    Env.Step("")
    assert Env.State() == [0,0,0]

test_Init();print("test_Init()")
test_move();print("test_move()")
test_terminal();print("test_terminal()")