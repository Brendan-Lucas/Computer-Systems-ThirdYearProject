#===============================================================
# test_VirtualDoorIO.py
#---------------------------------------------------------------
# Test class for Virtual DoorIO Module
#===============================================================
#imports
import time
import sys
from testing import testUnit
from DoorIO import VirtualDoorIO

###################################
def main():
    ###################################
    # Initialize
    T_UNIT = testUnit("Server IO") 
    T_UNIT.start()
    ###################################
    #Tests
    for test in get_tests():
        T_UNIT.eval_test_case(test,None)
    
    ###################################
    # Display
    T_UNIT.finish()

def get_tests():
    tests=[]
    tests.append(test_init)
    tests.append(test_sendPassword)
    tests.append(test_sendPicture)
    tests.append(test_sendState)
    tests.append(test_send1)
    tests.append(test_send2)
    tests.append(test_receive1)
    tests.append(test_receive2)
    return tests

###################################
# Tests
#======================================================================
# setLocked()
#----------------------------------------------------------------------
def test_init(T_UNIT):
    return T_UNIT.UNRESOLVED
def test_sendPassword(T_UNIT):
    return T_UNIT.UNRESOLVED
def test_sendPicture(T_UNIT):
    return T_UNIT.UNRESOLVED
def test_sendState(T_UNIT):
    return T_UNIT.UNRESOLVED
def test_send1(T_UNIT):
    return T_UNIT.UNRESOLVED
def test_send2(T_UNIT):
    return T_UNIT.UNRESOLVED
def test_receive1(T_UNIT):
    return T_UNIT.UNRESOLVED
def test_receive2(T_UNIT):
    return T_UNIT.UNRESOLVED

if len(sys.argv) > 1 and sys.argv[1] == "-s": main()