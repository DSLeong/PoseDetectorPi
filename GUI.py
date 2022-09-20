#Initialise Modules
from Calibrate import Calibrate as Calibrate
from GenerateTags import GenerateTags as GenerateTags
from detect import PoseDetector as PoseDetector

#GUI Components
running = True


#Program Start
while running:
	#Get User Input + Error Testing
	command = -1
	while command < 0 or command > 4:
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

		userInput = input("Command? ")

		if not userInput.isnumeric():
			print("Please input Numeric Value.")
		elif int(userInput) < 0 or int(userInput) > 4:
			input("Please input from Command List.")
		else:
			command = int(userInput)
		

	#Switch for Modules
	if command == 0: #Close Program
		print("EXIT")
		running = False

	elif command == 1: #Calibration
		print("CALIBRATION")

		command = -1
		while command < 0 or command > 1:
			userInput = input("Create Images (0:False 1:True)? ")

			if not userInput.isnumeric():
				print("Please input Numeric Value.")
			elif int(userInput) < 0 or int(userInput) > 1:
				input("Please input from Command List.")
			else:
				if int(userInput) == 1:
					command = int(userInput)
					Calibrate.camCapture(PanTiltEnable)

		Calibrate.Calibration()
	
	elif command == 2: #Generate Tags
		print("GENERATE TAGS")
		GenerateTags.GenerateTags()

	elif command == 3: #Eye to Hand
		print("EYE TO HAND")
		PoseDetector.poseDetector(PoseDetector, None, None, None)
		input("Press Enter to continue")

	elif command == 4: #Eye in Hand
		print("EYE IN HAND")
		inputX, inputY, inputZ = 0, 0, 0
		inputNum = False

        #Program to follow
		while not inputNum:
			try:
				print("Set Values:")
				inputX = int(input("x: "))
				inputY = int(input("y: "))
				inputZ = int(input("z: "))
			except ValueError:
				input("Please input Numeric Values.")
				continue
			else:
				inputNum = True

		PoseDetector.poseDetector(PoseDetector, inputX, inputY, inputZ)
		input("Press Enter to continue")

	else: #ERROR
		print("ERROR")


print("EXITED VIA COMMAND")
