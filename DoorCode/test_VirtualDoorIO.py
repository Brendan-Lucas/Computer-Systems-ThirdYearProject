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
    T_UNIT = testUnit("Virtual Door IO")
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
    tests.append(test_setLocked_TRUE)
    tests.append(test_setLocked_FALSE)
    tests.append(test_setUnlocked_TRUE)
    tests.append(test_setUnlocked_FALSE)
    tests.append(test_isLocked_TRUE)
    tests.append(test_isLocked_FALSE)
    tests.append(test_isOpen_TRUE)
    tests.append(test_isOpen_FALSE)
    tests.append(test_isKeyPressed_TRUE)
    tests.append(test_isKeyPressed_FALSE)
    tests.append(test_displayLCD_TEXT)
    tests.append(test_displayLCD_CLEAR)
    tests.append(test_playSound)
    return tests

###################################
# Tests
#======================================================================
# setLocked()
#----------------------------------------------------------------------
# Test setLocked() if door initally locked
def test_setLocked_TRUE(T_UNIT):
    IO = VirtualDoorIO()
    IO.LOCK_BUFFER = True
    if IO.setLocked() and IO.LOCK_BUFFER == True:
        return T_UNIT.PASS  
    return T_UNIT.FAIL

#----------------------------------------------------------------------
# Test setLocked() if door initally locked
def test_setLocked_FALSE(T_UNIT):
    IO = VirtualDoorIO()
    IO.LOCK_BUFFER = False
    if IO.setLocked() and IO.LOCK_BUFFER == True:
        return T_UNIT.PASS  
    return T_UNIT.FAIL

#======================================================================
# setUnlocked()
#----------------------------------------------------------------------
# Test setUnlocked() if door initally locked
def test_setUnlocked_TRUE(T_UNIT):
    IO = VirtualDoorIO()
    IO.LOCK_BUFFER = True
    if IO.setUnlocked() and IO.LOCK_BUFFER == False:
        return T_UNIT.PASS  
    return T_UNIT.FAIL

#----------------------------------------------------------------------
# Test setUnlocked() if door initally unlocked
def test_setUnlocked_FALSE(T_UNIT):
    IO = VirtualDoorIO()
    IO.LOCK_BUFFER = False
    if IO.setUnlocked() and IO.LOCK_BUFFER == False:
        return T_UNIT.PASS  
    return T_UNIT.FAIL

#======================================================================
# isLocked()
#----------------------------------------------------------------------
# Test isLocked() if door initally locked
def test_isLocked_TRUE(T_UNIT):
    IO = VirtualDoorIO()
    IO.LOCK_BUFFER = True
    if IO.isLocked() == True:
        return T_UNIT.PASS  
    return T_UNIT.FAIL

#----------------------------------------------------------------------
# Test isLocked() if door initally unlocked
def test_isLocked_FALSE(T_UNIT):
    IO = VirtualDoorIO()
    IO.LOCK_BUFFER = False
    if IO.isLocked() == False:
        return T_UNIT.PASS  
    return T_UNIT.FAIL

#======================================================================
# isOpen()
#----------------------------------------------------------------------
# Test isOpen() if door initally open
def test_isOpen_TRUE(T_UNIT):
    IO = VirtualDoorIO()
    IO.DOOR_BUFFER = True
    if IO.isOpen() == True:
        return T_UNIT.PASS  
    return T_UNIT.FAIL

#----------------------------------------------------------------------
# Test isOpen() if door initally closed
def test_isOpen_FALSE(T_UNIT):
    IO = VirtualDoorIO()
    IO.DOOR_BUFFER = False
    if IO.isOpen() == False:
        return T_UNIT.PASS  
    return T_UNIT.FAIL

#======================================================================
# isKeyPressed()
#----------------------------------------------------------------------
# Test isKeyPressed() if 1 key is pressed
def test_isKeyPressed_TRUE(T_UNIT):
    IO = VirtualDoorIO()
    IO.KEYPAD_BUFFER = '1'
    if IO.isKeyPressed() == '1':
        return T_UNIT.PASS  
    return T_UNIT.FAIL

#----------------------------------------------------------------------
# Test isKeyPressed() no key is pressed
def test_isKeyPressed_FALSE(T_UNIT):
    IO = VirtualDoorIO()
    if IO.isKeyPressed() == False:
        return T_UNIT.PASS  
    return T_UNIT.FAIL
    
#======================================================================
# displayLCD()
#----------------------------------------------------------------------
# Test displayLCD() if LCD has text
def test_displayLCD_TEXT(T_UNIT):
    IO = VirtualDoorIO()
    IO.displayLCD("HELLO WORLD!")
    if IO.LCD_BUFFER == 'HELLO WORLD!':
        return T_UNIT.PASS  
    return T_UNIT.FAIL
#----------------------------------------------------------------------
# Test displayLCD() if LCD is clear
def test_displayLCD_CLEAR(T_UNIT):
    IO = VirtualDoorIO()
    IO.displayLCD("")
    if IO.LCD_BUFFER == '':
        return T_UNIT.PASS  
    return T_UNIT.FAIL
#======================================================================
# playSuund()
#----------------------------------------------------------------------
# Test is sound is played
def test_playSound(T_UNIT):
    IO = VirtualDoorIO()
    IO.playSound("sounds/sound_blocked.wav")
    if IO.SOUND_BUFFER == 'sounds/sound_blocked.wav':
        return T_UNIT.PASS  
    return T_UNIT.FAIL
###################################

if len(sys.argv) > 1 and sys.argv[1] == "-s": main()
