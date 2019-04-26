import RL

def test_typGridState():
    testState = RL.typGridState(1,2,3,True)
    if not testState.x == 1:
        return -1
    if not testState.y == 2:
        return -2
    if not testState.reward == 3:
        return -3
    if not testState.terminal == True:
        return -4
    return 0

def test_typRewState():
    testState = RL.typRewState("-",1,2,-1)
    if not testState.state == "-":
        return -1
    if not testState.reward == 1:
        return -2
    if not testState.value == 2:
        return -3
    if not testState.visited == -1:
        return -4
    return 0

def test_clsEnvironment():
    rows = 4; cols = 4
    testGrid = RL.clsEnvironment(rows,cols,-2)
    for i in range(rows):
        for j in range(cols):
            if not testGrid[i,j].x == i:
                return -1
            if not testGrid[i,j].y == j:
                return -2
            if not testGrid[i,j].reward == -2:
                return -3
            if not testGrid[i,j].terminal == False:
                return -4
    return 0

def test_clsEnvironment_vizualize(tim):
    rows = 4; cols = 4
    testGridviz = RL.clsEnvironment(rows,cols,-2)
    testGridviz.visualize(1000)
    testGridviz.move("down")
    testGridviz.visualize(1000)
    return 0

print(test_typGridState())
print(test_typRewState())
print(test_clsEnvironment())
print(test_clsEnvironment_vizualize(99))

# grid = RL.Grid()

# grid.rect()

# grid.start()

# grid.move("up")

# grid.start()