import sys
sys.path.append("C:\\temp Daten\\Lernbereich\\Git\\myhamidi\\Py")

import Constraints

def test_AddRet():
    C = Constraints.clsConstraints(["up", "down", "left", "right"])
    C.Add([0.0, None, None], Allowed=["down", "left", "right"])
    C.Add([9.0, None, None], Forbidden=["down"])
    assert C.RetActionList([1.0, 2.0, 0]) == ["up", "down", "left", "right"]
    assert C.RetActionList([0.0, 2.0, 0]) == ["down", "left", "right"]
    assert C.RetActionList([9.0, 2.0, 0]) == ["up", "left", "right"]

    C.Add([None, 0.0, None], Allowed=["up", "down", "right"])
    C.Add([None, 9.0, None], Forbidden=["right"])
    assert C.RetActionList([2.0, 0.0, 0]) == ["up", "down", "right"]
    assert C.RetActionList([3.0, 9.0, 0]) == ["up", "down", "left"]

    assert C.RetActionList([0.0, 0.0, 0]) == ["down", "right"]
    assert C.RetActionList([9.0, 9.0, 0]) == ["up", "left"]

def test_ImportExport():
    C = Constraints.clsConstraints(["up", "down", "left", "right"])
    # Import
    C.Import("csv/test/testCTable.csv")
    assert C.RetActionList([2.0, 0.0, 0]) == ["up", "down", "right"]
    assert C.RetActionList([3.0, 9.0, 0]) == ["up", "down", "left"]
    assert C.RetActionList([0.0, 0.0, 0]) == ["down", "right"]
    assert C.RetActionList([9.0, 9.0, 0]) == ["up", "left"]
    # Export
    C.Export("csv/test/exports/testCTableCopy.csv")
    C2 = Constraints.clsConstraints(["up", "down", "left", "right"])
    C2.Import("csv/test/exports/testCTableCopy.csv")
    for i in range(C.len):
        assert C[i].featuresFrom == C2[i].featuresFrom
        assert C[i].featuresTo == C2[i].featuresTo
        assert C[i].ConstrainedActions == C2[i].ConstrainedActions

test_AddRet()
test_ImportExport()