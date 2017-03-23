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
from Door import Door

# Run Tests in file
###################################
def main():
    ###################################
    # Initialize
    global T_UNIT
    T_UNIT = testUnit("Door") 
    T_UNIT.start()
    ###################################
    #Tests
    for test in get_tests():
        T_UNIT.eval_test_case(test,None )
    
    ###################################
    # Display
    T_UNIT.finish()

# Get Tests in file
###################################
def get_tests():
    tests=[]
    tests.append(test_init_VALID)
    tests.append(test_init_INVALID_DOOR)
    tests.append(test_init_INVALID_HOME)
    tests.append(test_init_INVALID_TYPE)
    tests.append(test_runVirtual)
    tests.append(test_runHardware)
    tests.append(test_run_BACK)
    tests.append(test_run_FRONT)
    tests.append(test_pollMessage_NONE)
    tests.append(test_pollMessage_PW_LCKD)
    tests.append(test_pollMessage_PW_ULCKD)
    tests.append(test_pollMessage_PW_FALSE)
    tests.append(test_pollMessage_PIC_TRUE)
    tests.append(test_pollMessage_PIC_FALSE)
    tests.append(test_pollMessage_ORD_LCKD)
    tests.append(test_pollMessage_ORD_ULCKD)
    tests.append(test_pollKeypad_NONE)
    tests.append(test_pollKeypad_ENTER)
    tests.append(test_pollKeypad_INACTIVE)
    tests.append(test_pollKeypad_DELETE)
    tests.append(test_pollKeypad_KEY)
    tests.append(test_requestPassword_TRUE)
    tests.append(test_requestPassword_FALSE)
    tests.append(test_requestPicture_TRUE)
    tests.append(test_requestPicture_FALSE)
    tests.append(test_printLCD)
    tests.append(test_appendLCD_FULL)
    tests.append(test_appendLCD_EMPTY)
    tests.append(test_backspaceLCD_FULL)
    tests.append(test_backspaceLCD_EMPTY)
    tests.append(test_clearLCD)
    return tests

#======================================================================
# Tests
#----------------------------------------------------------------------
def test_init_VALID(T_UNIT):
    try: 
        DOOR = Door(44,11,"Front")
    except:
        return T_UNIT.FAIL  
    if DOOR.HOME_ID == 44  and DOOR.DOOR_ID == 11: # and Door.DOOR_TYPE = "Front"
        return T_UNIT.PASS
    return T_UNIT.FAIL

def test_init_INVALID_DOOR(T_UNIT):
    try: 
        DOOR = Door(44,257,"Front")
    except:
        return T_UNIT.PASS
    return T_UNIT.FAIL
    
def test_init_INVALID_HOME(T_UNIT):
    try: 
        DOOR = Door(257,11,"Front")
    except:
        return T_UNIT.PASS
    return T_UNIT.FAIL
    
def test_init_INVALID_TYPE(T_UNIT):
    try: 
        DOOR = Door(257,11,"Wrong")
    except:
        return T_UNIT.PASS
    return T_UNIT.FAIL
    
    
#======================================================================
def test_runVirtual(T_UNIT):
    try:
        DOOR = Door(44,11,"Front")
        DOOR_THR = threading.Thread(target=DOOR.runVirtual, args=())
        DOOR_THR.daemon = True
        DOOR_THR.start()
        time.sleep(1)
        if DOOR.DOOR_IO != None: # and Door.DOOR_TYPE = "Front"
            return T_UNIT.PASS
        DOOR_THR.stop()
    except:
        return T_UNIT.FAIL
    return T_UNIT.UNRESOLVED

def test_runHardware(T_UNIT):
    try:
        DOOR = Door(44,11,"Front")
        DOOR_THR = threading.Thread(target=DOOR.runHardware, args=())
        DOOR_THR.daemon = True
        DOOR_THR.start()
        time.sleep(1)
        if DOOR.DOOR_IO != None: # and Door.DOOR_TYPE = "Front"
            return T_UNIT.PASS
        DOOR_THR.stop()
    except:
        return T_UNIT.FAIL
    
#======================================================================
def test_run_FRONT(T_UNIT):
    return T_UNIT.UNRESOLVED
def test_run_BACK(T_UNIT):
    return T_UNIT.UNRESOLVED

    
#======================================================================
def test_pollMessage_NONE(T_UNIT):
    return T_UNIT.UNRESOLVED
def test_pollMessage_PW_LCKD(T_UNIT):
    return T_UNIT.UNRESOLVED
def test_pollMessage_PW_ULCKD(T_UNIT):
    return T_UNIT.UNRESOLVED
def test_pollMessage_PW_FALSE(T_UNIT):
    return T_UNIT.UNRESOLVED

#======================================================================
def test_pollMessage_PIC_TRUE(T_UNIT):
    return T_UNIT.UNRESOLVED    
def test_pollMessage_PIC_FALSE(T_UNIT):
    return T_UNIT.UNRESOLVED
    
#======================================================================
def test_pollMessage_ORD_LCKD(T_UNIT):
    return T_UNIT.UNRESOLVED
def test_pollMessage_ORD_ULCKD(T_UNIT):
    return T_UNIT.UNRESOLVED

#======================================================================
def test_pollDoor_LCKED_CLSD(T_UNIT):
    return T_UNIT.UNRESOLVED    
def test_pollDoor_ULCKED_CLSD(T_UNIT):
    return T_UNIT.UNRESOLVED
def test_pollDoor_LCKED_OPEN(T_UNIT):
    return T_UNIT.UNRESOLVED
def test_pollDoor_ULCKED_OPEN(T_UNIT):
    return T_UNIT.UNRESOLVED
    
#======================================================================
def test_pollKeypad_NONE(T_UNIT):
    return T_UNIT.UNRESOLVED
def test_pollKeypad_ENTER(T_UNIT):
    return T_UNIT.UNRESOLVED
def test_pollKeypad_INACTIVE(T_UNIT):
    return T_UNIT.UNRESOLVED
def test_pollKeypad_DELETE(T_UNIT):
    return T_UNIT.UNRESOLVED
def test_pollKeypad_KEY(T_UNIT):
    return T_UNIT.UNRESOLVED
    
#======================================================================
def test_requestPassword_TRUE(T_UNIT):
    return T_UNIT.UNRESOLVED
def test_requestPassword_FALSE(T_UNIT):
    return T_UNIT.UNRESOLVED
    
#======================================================================
def test_requestPicture_TRUE(T_UNIT):
    return T_UNIT.UNRESOLVED
def test_requestPicture_FALSE(T_UNIT):
    return T_UNIT.UNRESOLVED
    
#======================================================================
def test_printLCD(T_UNIT):
    return T_UNIT.UNRESOLVED
def test_appendLCD_FULL(T_UNIT):
    return T_UNIT.UNRESOLVED
def test_appendLCD_EMPTY(T_UNIT):
    return T_UNIT.UNRESOLVED
def test_backspaceLCD_FULL(T_UNIT):
    return T_UNIT.UNRESOLVED
def test_backspaceLCD_EMPTY(T_UNIT):
    return T_UNIT.UNRESOLVED
def test_clearLCD(T_UNIT):
    return T_UNIT.UNRESOLVED
  
#======================================================================

if len(sys.argv) > 1 and sys.argv[1] == "-s": main()