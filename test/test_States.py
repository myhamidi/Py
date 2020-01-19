import sys
sys.path.append("C:\\temp Daten\\Lernbereich\\Git\\myhamidi\\Py")

import States
import Sequence

def test_Init():
    St = States.clsStatesTable()
    assert St[0] == None
    assert St.len == 0

def test_InitCopy():
    St = States.clsStatesTable()
    St.Import("csv/test/testQ.csv")
    StCopy = States.clsStatesTable(CopyFrom=St)
    assert StCopy.len == 100
    for i in range(St.len):
        assert St[i].features == StCopy[i].features
        assert St[i].reward == StCopy[i].reward
        assert St[i].Q == StCopy[i].Q
    # Check that there's no reference link
    StCopy[0].Q[0] = 10.5
    assert StCopy[0].Q[0] == 10.5
    assert not St[0].Q[0] == 10.5

def test_Update():
    St = States.clsStatesTable()
    St.Reset()
    St.Update([0,1,0],3)
    assert St[0].features == [0,1,0]
    assert St.len == 1
    St.Update([0,2,0],1)
    St.Update([0,1,0],1)
    assert St.len == 2
    assert St[0].reward == [2.0, [3.0, 1.0]]

def test_MassUpdate():
    St = States.clsStatesTable()
    Sq = Sequence.clsSequence()
    Sq.Import("csv/test/testSeq.csv")
    for step in Sq.Steps:
        St.Update(step.state0)
        St.Update(step.state1)
    assert St.len == 100

def test_MassUpdate2():
    St = States.clsStatesTable()
    Sq = Sequence.clsSequence()
    Sq.Import("csv/test/testSeq.csv")
    X = [step.state0 for step in Sq.Steps]
    Q = [[-1,-2,-3] for step in Sq.Steps]
    St.Update(X,Q=Q)
    for i in range(St.len):
        St[i].Q = [-1,-2,-3]
    assert St.len == 99

def test_MassUpdate3():
    St = States.clsStatesTable()
    Sq = Sequence.clsSequence()
    Sq.Import("csv/test/testSeq.csv")
    X = [step.state0 for step in Sq.Steps]
    r = [-1.5 for step in Sq.Steps]
    St.Update(X,reward=r)
    for i in range(St.len):
        St[i].reward = -1.5
    assert St.len == 99

def test_Key():
    St = States.clsStatesTable()
    Sq = Sequence.clsSequence()
    Sq.Import("csv/test/testSeq.csv")
    for step in Sq.Steps:
        St.Update(step.state0)
        St.Update(step.state1)
    c=0
    for i in range(10):
        for j in range(10):
            t = 1 if i ==9 and j == 9 else 0
            stat = [float(i), float(j), t]
            assert St[stat].features == stat
            c +=1

def test_Sort():
    St = States.clsStatesTable()
    Sq = Sequence.clsSequence()
    Sq.Import("csv/test/testSeq.csv")
    for step in Sq.Steps:
        St.Update(step.state0)
        St.Update(step.state1)
    St.Sort()
    c=0
    for i in range(10):
        for j in range(10):
            if not (i ==9 and j == 9):
                assert St[c].features == [float(i), float(j), 0]
            else:
                assert St[c].features == [float(i), float(j), 1]
            c +=1

def test_AsList():
    St = States.clsStatesTable()
    St.Import("csv/test/testQ.csv")
    ls = St.AsList()
    c=0
    for i in range(10):
        for j in range(10):
            if not (i ==9 and j == 9):
                assert ls[c] == [float(i), float(j), 0]
            else:
                assert ls[c] == [float(i), float(j), 1]
            c +=1

def test_ImportExport():
    St1 = States.clsStatesTable()
    St2 = States.clsStatesTable()
    St1.Import("csv/test/testQ.csv")
    St1.Export("csv/test/exports/testQExport.csv")
    St2.Import("csv/test/exports/testQExport.csv")
    for i in range(St1.len):
        assert St1[i].features == St2[i].features
        assert St1[i].Q == St2[i].Q, i

def test_Reset():
    St = States.clsStatesTable()
    Sq = Sequence.clsSequence()
    Sq.Import("csv/test/testSeq.csv")
    for step in Sq.Steps:
        St.Update(step.state0)
        St.Update(step.state1)
    St.Reset()
    assert St[0] == None
    assert St.len == 0

test_Init();print("test_Init()")
test_InitCopy();print("test_InitCopy()")
test_Update();print("test_Update()")
test_MassUpdate();print("test_MassUpdate()")
test_MassUpdate2();print("test_MassUpdate2()")
test_MassUpdate3();print("test_MassUpdate3()")
test_Key();print("test_Key()")
test_Sort();print("test_Sort()")
test_AsList();print("test_AsList()")
test_ImportExport();print("test_ImportExport()")
test_Reset();print("test_Reset()")