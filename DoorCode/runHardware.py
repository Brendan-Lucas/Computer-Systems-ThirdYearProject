#============================================================================================
# runHardware.py
#--------------------------------------------------------------------------------------------
# Patrick Perron
# 25/02/17
#--------------------------------------------------------------------------------------------
#
# Initalize a door running on hardware
#
#============================================================================================
# Imports
import sys
from Door import Door
#============================================================================================
# Constants
MAX_ID = 256

#============================================================================================
def main():
	#--------------------------------------------------------------------------------------------
	# Check if Input is Valid
	if len(sys.argv) is not 4:
		print("Error: Must pass with Valid HomeID, DoorID, and Type"); exit(1)

	HomeID = sys.argv[1]
	DoorID = sys.argv[2]
	Type   = sys.argv[3] 

	# Check if HomeID is in valid range        
	if int(HomeID) < 0 or MAX_ID < int(HomeID):       
	    print("Error: Invalid Home ID Range"); exit(1)
	# Check if DoorID is in valid range
	if int(DoorID) < 0 or MAX_ID < int(DoorID):        
	    print("Error: Invalid Door ID Range"); exit(1)
	# Check if Door Type is valid
	if Type != "Front" and Type != "Back":        
	    print("Error: Invalid Door Type"); exit(1)

	#--------------------------------------------------------------------------------------------
	#Run Door
	print("Connecting to Door: HomeID("+HomeID+"), DoorID("+DoorID+")")
	door = Door(HomeID, DoorID, Type)
	door.runHardware()
	
#--------------------------------------------------------------------------------------------
main()
#============================================================================================


