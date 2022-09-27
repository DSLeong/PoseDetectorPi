#Initialise Modules
from Calibrate import Calibrate as Calibrate
from GenerateTags import GenerateTags as GenerateTags
from PoseDetector import PoseDetector as PoseDetector

#GUI Components
running = True

#Program Start
while running:
	#Get User Input + Error Testing
	while True:
		print("\n=================================================")
		print("|           Pose Detector using ArUco           |")
		print("|              Created by Group 45              |")
		print("|   https://github.com/DSLeong/PoseDetectorPi   |")
		print("=================================================")
		print("|                 Command  List                 |")
		print("|                                               |")
		print("|                 1 : Calibrate                 |")
		print("|               2 : Generate Tags               |")
		print("|         3 : Detect Pose (Eye to Hand)         |")
		print("|         4 : Follow Pose (Eye in Hand)         |")
		print("|               0 : Close Program               |")
		print("|                                               |")
		print("=================================================")

		try:
			command = int(input("Command? "))
		except ValueError:
			input("Please input Numeric Values.")
		else:
			if command < 0 or command > 4:
				input("Please input from Command List.")
			else:
				break
		

	#Switch for Modules
	if command == 0: #Close Program
		print("EXIT")
		running = False

	elif command == 1: #Calibration
		print("CALIBRATION")

		while True:
			try:
				userInput = int(input("Create Images (0:False 1:True)? "))
			except ValueError:
				input("Please input Numeric Values.")
			else:
				if userInput < 0 or userInput > 1:
					input("Please input from Command List.")
				else:
					if userInput == 1:
						Calibrate.camCapture()
					break

		Calibrate.Calibration()
	
	elif command == 2: #Generate Tags
		print("GENERATE TAGS")
		GenerateTags()

	elif command == 3: #Eye to Hand
		print("EYE TO HAND")
		PoseDetector.poseDetector(PoseDetector, None, None, None)
		input("Press Enter to continue")

	elif command == 4: #Eye in Hand
		print("EYE IN HAND")

		while True:
			try:
				print("Set Values:")
				inputX = int(input("x: "))
				inputY = int(input("y: "))
				inputZ = int(input("z: "))
			except ValueError:
				input("Please input Numeric Values.")
			else:
				break

		PoseDetector.poseDetector(PoseDetector, inputX, inputY, inputZ)
		input("Press Enter to continue")

	#ERROR CASE
	else:
		input("ERROR")


print("EXITED VIA COMMAND")
