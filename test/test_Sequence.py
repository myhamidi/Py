import sys
sys.path.append("C:\\temp Daten\\Lernbereich\\Git\\myhamidi\\Py")
import Sequence as Seq

Sq = Seq.clsSequence()
# ==============================================================================
# -- Tests ---------------------------------------------------------------------
# ============================================================================== 

def test_AddStep1():
    Sq.AddStep([1,"hi",0.1,0], -1)
    assert Sq[-1].state0 == Sq.Steps[-1].state0

def test_AddStep2():
    Sq.Reset()
    assert len(Sq.Steps) == 0
    for i in range(5):
        Sq.AddStep([i,"hi",0.1,0], -1)
        assert len(Sq.Steps) == i+1
        assert Sq.Steps[-1].state0 == [i,"hi",0.1,0]
    for i in range(1,5):
        assert Sq.Steps[i-1].state1 == [i,"hi",0.1,0]
        assert Sq.Steps[i].reward == -1
        assert Sq.Steps[i].totalreward == -1 * (i+1)

def test_Reset():
    Sq.AddStep([2,"hi",0.1,1], -1)
    assert len(Sq.Steps) > 0
    assert Sq.len > 0
    assert Sq.Nterminal > 0
    Sq.Reset()
    assert len(Sq.Steps) == 0
    assert Sq.len == 0
    assert Sq.Nterminal == 0
    assert Sq[0] == None

def test_AddStep4():
    # Test First State is Terminal
    Sq.Reset()
    Sq.AddStep([1,2,1],-1)
    assert Sq.Steps[-1].state0 == [1,2,1]

def test_AddStep5():
    # Test Next State is Terminal
    Sq.AddStep([1,3,0],-1)
    Sq.AddStep([1,2,1],-1)
    assert Sq.Steps[-1].state1 == [1,2,1]

def test_AddStep6():
    # First State Terminal, then normal
    Sq.Reset()
    Sq.AddStep([1,3,1],-1)
    Sq.AddStep([1,2,0],-1)
    assert Sq.Steps[-2].state0 == [1,3,1],Sq.Steps[-2].state0
    assert Sq.Steps[-2].state1 == [1,2,0],Sq.Steps[-2].state1
    assert Sq.Steps[-1].state0 == [1,2,0],Sq.Steps[-1].state0

def test_AddStepN():
    # Nex State Terminal, then normal
    Sq.AddStep([1,5,0],-1)
    Sq.AddStep([1,3,1],-1)
    Sq.AddStep([1,2,0],-1)
    assert Sq.Steps[-2].state0 == [1,5,0],Sq.Steps[-2].state0
    assert Sq.Steps[-2].state1 == [1,3,1],Sq.Steps[-2].state1
    assert Sq.Steps[-1].state0 == [1,2,0],Sq.Steps[-1].state0


def test_AddStep8():
    # Test Second State is Terminal
    Sq.Reset()
    Sq.AddStep([1,1,0],-2)
    Sq.AddStep([1,2,1],-3)
    assert Sq.Steps[-1].state0 == [1,1,0]
    assert Sq.Steps[-1].state1 == [1,2,1]
    assert Sq.Steps[-1].reward == -2
    assert Sq.Steps[-1].totalreward == -3

def test_AddStep9():
    # Test Third State is Terminal
    Sq.Reset()
    Sq.AddStep([1,1,0],-2)
    Sq.AddStep([1,3,0],-2)
    Sq.AddStep([1,2,1],-3)
    assert Sq.Steps[-2].state0 == [1,1,0]
    assert Sq.Steps[-2].state1 == [1,3,0]
    assert Sq.Steps[-1].state0 == [1,3,0]
    assert Sq.Steps[-1].state1 == [1,2,1]
    assert Sq.Steps[-1].reward == -2
    assert Sq.Steps[-1].totalreward == -3

def test_AddStep10():
    # Test First and Second State is Terminal
    Sq.Reset()
    Sq.AddStep([1,1,1],-2)
    Sq.AddStep([1,2,1],-3)
    assert Sq.Steps[-1].state0 == [1,1,1]
    assert Sq.Steps[-1].state1 == [1,2,1]
    assert Sq.Steps[-1].reward == -2
    assert Sq.Steps[-1].totalreward == -3

def test_SetAction1():
    Sq.Reset()
    Sq.AddStep([1,1,1],-2)
    Sq.SetAction()
    assert Sq.Steps[-1].action == ""
    assert Sq.Steps[-1].actionInt == -1

def test_SetAction2():
    Sq.Reset()
    Sq.AddStep([1,1,1],-2)
    Sq.SetAction(Action="")
    assert Sq.Steps[-1].action == ""
    assert Sq.Steps[-1].actionInt == -1

def test_SetAction3():
    Sq.Reset()
    Sq.AddStep([1,1,1],-2)
    Sq.SetAction(-1,"",-1)
    assert Sq.Steps[-1].action == ""
    assert Sq.Steps[-1].actionInt == -1

def test_SetAction4():
    Sq.Reset()
    Sq.AddStep([1,1,1],-2)
    Sq.SetAction(-1,"Run",-1)
    assert Sq.Steps[-1].action == "Run"
    assert Sq.Steps[-1].actionInt == -1

def test_SetAction5():
    Sq.Reset()
    Sq.AddStep([1,1,1],-2)
    Sq.SetAction(-1,"",1)
    assert Sq.Steps[-1].action == ""
    assert Sq.Steps[-1].actionInt == 1

# # -- Review ExportSeqtoCSV()------------------------------------------------------------
def test_ImportExport():
    Sq.Reset()
    for i in range(100):
        Sq.AddStep([i%10,100-i%10,0],-1)
        Sq.SetAction(-1,"run",i%4)
    tmpSteps0 = [step.state0 for step in Sq.Steps]
    tmpSteps1 = [step.state1 for step in Sq.Steps]
    tmpact = [step.action for step in Sq.Steps]
    tmpactInt = [step.actionInt for step in Sq.Steps]
    Sq.Export("csv/test/exports/testSeq100.csv")
    Sq.Reset()
    assert len(Sq.Steps) == 0
    Sq.Import("csv/test/exports/testSeq100.csv")
    assert tmpSteps0 == [step.state0 for step in Sq.Steps]
    assert tmpSteps1 == [step.state1 for step in Sq.Steps]
    assert tmpact == [step.action for step in Sq.Steps]
    assert tmpactInt == [step.actionInt for step in Sq.Steps]
    assert len(Sq.Steps) == Sq.len, Sq.len 

# # -- Test Return------------------------------------------------------------
def test_ReturnIdx():
    Sq.Import("csv/test/testSeq.csv")
    assert len(Sq.ReturnIdx(None)) == 2998
    assert len(Sq.ReturnIdx(0)) == 2998
    assert Sq.ReturnIdx(1) == [974, 1328, 1440, 2309, 2549]

def test_ReturnStates():
    Sq.Import("csv/test/testSeq.csv")
    assert len(Sq.ReturnStates(None)) == 100
    assert len(Sq.ReturnStates(0)) == 99
    assert Sq.ReturnStates(1) == [[9.0, 9.0, 1]]


# -- Steps Sorting ---------------------------------------------------------------------
def test_SortRemoveDuplicates():
    Sq.Reset()
    Sq.Import("csv/test/testSeq.csv")
    Sq.RemoveDuplicates()
    Sq.Sort()
    c = 0
    for i in range(10):
        for j in range(10):
            if i == 9 and j == 9:
                assert Sq.Steps[c-1].state1 == [float(i), float(j), 1]
                break
            for k in range(4):
                assert Sq.Steps[c].state0 == [float(i), float(j), 0],c
                assert Sq.Steps[c].actionInt == k, str(c) + " " + str(k)
                c +=1
    Sq.Export("csv/test/exports/testSeqSorted.csv")

def test_ReturnSample():
    Sq.Reset()
    Sq.Import("csv/test/testSeq.csv")
    Sq.RemoveDuplicates()
    Sq.Sort()
    SqSample = Sq.ReturnSample(20)
    assert str(type(SqSample)) == "<class 'Sequence.clsSequence'>"
    assert SqSample.len == 20

    SqSample2 = Sq.ReturnSample(idxs=[12,40])
    assert SqSample2.len == 2
    
    SqSample3 = Sq.ReturnSample(idxs=Sq.ReturnIdx(1)) 
    assert SqSample3.len == 2
    assert SqSample3.Nterminal == 2

def test_AsList():
    Sq.Reset()
    Sq.Import("csv/test/testSeq.csv")
    Sq.Sort()
    Sq.RemoveDuplicates()
    S0, S1, AI, R, TR = Sq.AsList()
    a = 1 # review
    assert len(S0) == 396
    assert len(S1) == 396
    assert len(AI) == 396
    assert len(R) == 396
    assert len(TR) == 396

    S0, S1, AI, R, TR = Sq.AsList(multi=10)
    assert len(S0) == 3960
    for i in range(10):
        assert S0[i] == S0[0]
    assert len(S1) == 3960
    assert len(AI) == 3960
    assert len(R) == 3960
    assert len(TR) == 3960


test_AddStep1();print("test_AddStep1()")
test_AddStep2();print("test_AddStep2()")
test_Reset();print("test_Reset()")
test_AddStep4();print("test_AddStep4()")
test_AddStep5();print("test_AddStep5()")
test_AddStep6();print("test_AddStep6()")
test_AddStepN();print("test_AddStepN()")
test_AddStep8();print("test_AddStep8()")
test_AddStep9();print("test_AddStep9()")
test_AddStep10();print("test_AddStep10()")
test_SetAction1();print("test_SetAction1()")
test_SetAction2();print("test_SetAction2()")
test_SetAction3();print("test_SetAction3()")
test_SetAction4();print("test_SetAction4()")
test_SetAction5();print("test_SetAction5()")
test_ImportExport();print("test_ImportExport()")
test_ReturnIdx();print("test_ReturnIdx()")
test_ReturnStates();print("test_ReturnStates()")
test_SortRemoveDuplicates();print("test_SortRemoveDuplicates()")
test_ReturnSample();print("test_ReturnSample()")
test_AsList();print("test_AsList()")
