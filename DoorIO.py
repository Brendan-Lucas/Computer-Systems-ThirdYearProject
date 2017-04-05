import RPi.GPIO as GPIO
import time
from picamera import PiCamera
from time import sleep

class HardwareDoorIO():
    def __init__(self, type):
        # Variable to indicate hardware type
        if type == "Front": self.HW = "GertBoard"
        else: self.HW = "PiFace"

    #===============================================================
    # setLocked()
    #---------------------------------------------------------------
    # Set door to locked state.
    # return: True(successful), False(unsuccessful)
    #---------------------------------------------------------------
    def setLocked(self):
        # Only run if actual state is different than passed state
        if self.isLocked() is False:
            if(self.HW == "GertBoard"):
                GPIO.setmode(GPIO.BOARD)
                pin_number=7
                GPIO.setup(pin_number, GPIO.OUT)
                frequency_hertz= 50
                pwm= GPIO.PWM(pin_number, frequency_hertz)

                right_position=2.5
                middle_position = 5

                positionList= [middle_position, right_position, middle_position]
                ms_per_cycle= 700/frequency_hertz

                for position in positionList:
                    duty_cycle_percentage = position * 100 /ms_per_cycle
                    pwm.start(duty_cycle_percentage)
                    time.sleep(0.5)

                pwm.stop()
                GPIO.cleanup()

            
                
        # Check if operation was successful
        if self.isLocked() is True:
            return True
        return False

    #===============================================================
    # setUnocked()
    #---------------------------------------------------------------
    # Set door to unlocked state.
    # return: True(successful), False(unsuccessful)
    #---------------------------------------------------------------
    def setUnlocked(self):
        # Only run if actual state is different than passed state
        if self.isLocked() is True:
             if(self.HW == "GertBoard"):
                GPIO.setmode(GPIO.BOARD)
                pin_number=7
                GPIO.setup(pin_number, GPIO.OUT)
                frequency_hertz= 50
                pwm= GPIO.PWM(pin_number, frequency_hertz)

                right_position=2.5
                middle_poristion = 7.5

                positionList= [middle_poristion, right_position]
                ms_per_cycle= 700/frequency_hertz

                for position in positionList:
                    duty_cycle_percentage = position * 100 /ms_per_cycle
                    pwm.start(duty_cycle_percentage)
                    time.sleep(0.5)

                pwm.stop()
                GPIO.cleanup()
            
                
        # Check if operation was successful
        if self.isLocked() is False: return True
        return False

    #===============================================================
    # isLocked()
    #---------------------------------------------------------------
    # Get the current state of the lock
    # return: True(Locked), False(Unlocked)
    #---------------------------------------------------------------
    def isLocked(self):     
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(12, GPIO.IN, GPIO.PUD_UP)
        if not GPIO.input(12):
            return True  # Door Locked
        else:
            return False # Door Unlocked
    

    #===============================================================
    # isOpen()
    #---------------------------------------------------------------
    # Get the current state of the door
    # return: True(Open), False(Closed)
    #---------------------------------------------------------------
    def isOpen(self): 
        return False
    


    #===============================================================
    # displayLCD()
    #---------------------------------------------------------------
    # Display message on LCD
    #---------------------------------------------------------------
    def displayLCD(self, message):
        return

    #===============================================================
    # playSound()
    #---------------------------------------------------------------
    # Play sound on keypad panel speaker
    #---------------------------------------------------------------
    def playSound(self, sound):
        return

    #===============================================================
    # takePicture()
    #---------------------------------------------------------------
    # Take picture with camera
    # return: byte[](Picture taken), False(Error Occurred)
    #---------------------------------------------------------------
    def takePicture(self): 
        try:
            camera = PiCamera()
            camera.start_preview()
            sleep(5)

            camera.capture('/home/pi/Desktop/image.jpg')
            camera.stop_preview()
        except IOError:
            pass

#===============================================================
