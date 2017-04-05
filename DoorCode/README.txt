=====================================================
README

widget_*.py -  Widgets run as part of the virtual door panel
test_*      -  Test function modules for existing code
testing.py  -  Test framework for testing

To run a door on hardware:
  python runHardware.py $HomeID $DoorID $DoorType

To run a door virtually:
  python runVirtual_DEMO.py
  
  
Virtual Door Info:
  -Download all images and sounds
  -run on windows operating system with python3 installed

=====================================================
To run tests:

	If standalone module, run as: 
		> python test_*.py -s

	If running all tests at once, run as:
		> python  test_Door_All.py -a


Note: not all test cases are implemented. Though the
list of tests is exhaustive and covers nearly every case,
we did not have the time to finish writing the all However, 
all required functioanlity that these tests prove can be 
demonstrated with the virtual door GUI

=====================================================
