#============================================================================================
# test_Door_All.py
#--------------------------------------------------------------------------------------------
# Patrick Perron
#--------------------------------------------------------------------------------------------
#
# Testing Module for all Door Modules using testing.py
# Run all by passing -a option
#
#============================================================================================
# Imports
import time
import sys
import threading
from testing import testUnit
from Door    import Door
from test_VirtualDoorIO import get_tests as get_VirtualDoorTests
from test_Door          import get_tests as get_DoorTests
from test_ServerIO      import get_tests as get_ServerTests

#============================================================================================
# Run Local Tests
#--------------------------------------------------------------------------------------------
def main():
    # Initialize
    global T_UNIT
    T_UNIT = testUnit("Complete Door Module") 
    T_UNIT.start()
    
    # Test each module
    for test in get_VirtualDoorTests():
        T_UNIT.eval_test_case(test, None )
    for test in get_ServerTests():
        T_UNIT.eval_test_case(test, None )
    for test in get_DoorTests():
        T_UNIT.eval_test_case(test, None )
    
    # Display Results
    T_UNIT.finish()

#============================================================================================
# Run All
#--------------------------------------------------------------------------------------------
if len(sys.argv) > 1 and sys.argv[1] == "-a": main()
#============================================================================================
