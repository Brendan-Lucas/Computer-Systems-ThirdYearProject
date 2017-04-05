#============================================================================================
# test_ServerIO.py
#--------------------------------------------------------------------------------------------
# Patrick Perron
#--------------------------------------------------------------------------------------------
#
# Testing Module for ServerIO.py using testing.py
# Run standalone by passing -s option
#
#============================================================================================
# Imports
import time
import sys
from testing import testUnit
from ServerIO import ServerIO

#============================================================================================
# Run Local Tests
#--------------------------------------------------------------------------------------------
def main():
    # Initialize
    global T_UNIT
    T_UNIT = testUnit("ServerIO") 
    T_UNIT.start()
    # Run tests
    for test in get_tests():
        T_UNIT.eval_test_case( test, None )
    
    # Display Results
    T_UNIT.finish()

#============================================================================================
# get_tests()
#--------------------------------------------------------------------------------------------
# Return list of tests in suite
#--------------------------------------------------------------------------------------------
def get_tests():
    tests=[]
    tests.append(test_init)
    tests.append(test_sendPassword)
    tests.append(test_sendPicture)
    tests.append(test_sendState)
    tests.append(test_send)
    tests.append(test_receive)
    return tests


#============================================================================================
# Tests
#--------------------------------------------------------------------------------------------
def test_init(T_UNIT):
    IO = ServerIO(3,3)
    if IO != None and IO.SOCKET is not None:
        return T_UNIT.PASS  
    else:
        return T_UNIT.FAIL


#--------------------------------------------------------------------------------------------
# NOTE:
#
#  The following test cases can be seen working with the virtual door. Therefore, we did
#  did not write theses test cases as we did not have the time.
#   
#--------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------
def test_sendPassword(T_UNIT):    
    return T_UNIT.UNRESOLVED

#--------------------------------------------------------------------------------------------
def test_sendPicture(T_UNIT):
    return T_UNIT.UNRESOLVED

#--------------------------------------------------------------------------------------------
def test_sendState(T_UNIT):
    return T_UNIT.UNRESOLVED

#--------------------------------------------------------------------------------------------
def test_send(T_UNIT):
    return T_UNIT.UNRESOLVED

#--------------------------------------------------------------------------------------------
def test_receive(T_UNIT):
    return T_UNIT.UNRESOLVED

#============================================================================================
# Run Standalone
#--------------------------------------------------------------------------------------------
if len(sys.argv) > 1 and sys.argv[1] == "-s": main()
#============================================================================================
