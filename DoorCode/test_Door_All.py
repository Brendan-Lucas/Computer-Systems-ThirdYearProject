#===============================================================
# test_Door.py
#---------------------------------------------------------------
# Test class for DoorModule
#===============================================================
#imports
import time
import sys
import threading
from testing import testUnit
from Door    import Door
from test_VirtualDoorIO import get_tests as get_VirtualDoorTests
from test_Door          import get_tests as get_DoorTests
from test_ServerIO      import get_tests as get_ServerTests

# Run Tests in file
###################################
def main():
    ###################################
    # Initialize
    global T_UNIT
    T_UNIT = testUnit("Complete Door Module") 
    T_UNIT.start()
    
    ###################################
    # Tests
    for test in get_VirtualDoorTests():
        T_UNIT.eval_test_case(test, None )
    for test in get_ServerTests():
        T_UNIT.eval_test_case(test, None )
    for test in get_DoorTests():
        T_UNIT.eval_test_case(test, None )
    
    ###################################
    # Display
    T_UNIT.finish()
  
#======================================================================

if len(sys.argv) > 1 and sys.argv[1] == "-a": main()