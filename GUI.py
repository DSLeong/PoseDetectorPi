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
	while command < 0 or command > 3:
		print("=================================================")
		print("|           Pose Detector using ArUco           |")
		print("|              Created by Group 45              |")
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
			print("Please input from Command List.")
		else:
			command = int(userInput)
		

	#Switch for Modules
	if command == 0: #Close Program
		print("EXIT")
		running = False

	elif command == 1: #Calibration
		print("CALIBRATION")
		Calibrate.Calibration()
	
	elif command == 2: #Generate Tags
		print("GENERATE TAGS")
		GenerateTags.GenerateTags()

	elif command == 3: #Eye to Hand
		print("EYE TO HAND")
		PoseDetector.poseDetector()

	elif command == 4: #Eye in Hand
		print("EYE IN HAND")
		#Set Values
		PoseDetector.poseDetector()

	else: #ERROR
		print("ERROR")


print("EXITED VIA COMMAND")
