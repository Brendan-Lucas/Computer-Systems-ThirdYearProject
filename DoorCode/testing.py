#============================================================================================
# testing.py
#--------------------------------------------------------------------------------------------
# Patrick Perron
# 01/03/17
#--------------------------------------------------------------------------------------------
#
# Testing framework to test virtual door
# *Note: TIMEOUT not implemented due to differences in LINUX and WINDOWS OS for triggering
#        timeouts via signals. However, Timeouts not necessary for scope of project
#
#============================================================================================
# Imports
import time
import signal
import sys
import os

#============================================================================================
# Class Declaration
#--------------------------------------------------------------------------------------------
class testUnit():
#============================================================================================
    # Initializing Code
    #---------------------------------------------------------------
    def __init__(self, test):
        self.name = test
        # Constants
        self.PASS       =  0
        self.FAIL       =  1
        self.UNRESOLVED = -1
        self.TIMEOUT    =  60 # Default Timeout
        # Test Results
        self.pass_count = 0
        self.fail_count = 0
        self.unrs_count = 0
        self.test_count = 0

    #===============================================================
    # start()
    #---------------------------------------------------------------
    # Start the specified test suite
    #---------------------------------------------------------------
    def start(self):
        print("Start Test: "+self.name)
        # Reset Stats
        self.pass_count = 0
        self.fail_count = 0
        self.unrs_count = 0
        self.test_count = 0
        
    #===============================================================
    # eval_test_case()
    #---------------------------------------------------------------
    # Evaluate a specic test function and increment stats
    #---------------------------------------------------------------
    def eval_test_case(self, test, timeout):
        # Suppress output for test
        sys.stdout = os.devnull; sys.stderr = os.devnull
        # run test function
        rc = test(self)
        # Allow output again
        sys.stdout = sys.__stdout__; sys.stderr = sys.__stderr__
        self.test_count += 1
        if   rc == 1:
            print("["+str(self.test_count).ljust(3)+" - FAIL]: "+str(test)) 
            self.fail_count += 1
        elif rc == 0: 
            print("["+str(self.test_count).ljust(3)+" - PASS]: "+str(test))
            self.pass_count += 1
        else:
            print("["+str(self.test_count).ljust(3)+" - UNRESOLVED]: "+str(test)) 
            self.unrs_count         += 1
        return 

    #===============================================================
    # finish()
    #---------------------------------------------------------------
    # Display results from test case
    #---------------------------------------------------------------
    def finish(self):
        print("End Test: "+str(self.name)+"\n"+
              "PASS:("+str(self.pass_count)+"/"+str(self.test_count)+") | "+
              "FAIL:("+str(self.fail_count)+"/"+str(self.test_count)+") | "+
              "UNRESOLVED :("+str(self.unrs_count)+"/"+str(self.test_count)+")")

#============================================================================================
