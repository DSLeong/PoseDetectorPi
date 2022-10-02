#Initialise Modules
from Calibrate import Calibrate as Calibrate
from GenerateTags import GenerateTags as GenerateTags
from PoseDetector import PoseDetector as PoseDetector
import cv2


#Get Camera Data
def getCameras():
	print("\n=================================================")
	print("Obtaining Camera/s - Please wait")

	#List camera/s
	cameraList = []
	i = 0
	while i < 10:
		cap = cv2.VideoCapture(i)
		if cap.read()[0]:
			cameraList.append(i)
			cap.release()
		i += 1

	#Set Camera
	while True:
		try:
			print("\n=================================================")
			print("List of avaliable camera/s index")
			i = 0
			for cam in cameraList:
				print("{}: Camera Index {}".format(i,cam))
				i += 1
			userInput = int(input("\nSelect camera index: "))
		except ValueError:
			input("Please input Numeric Values.")
		else:
			if userInput < 0 or userInput > len(cameraList) - 1:
				input("Please input from Command List.")
			else:
				index = cameraList[userInput]
				cap = cv2.VideoCapture(index)
				print("Creating Camera Preview")
				while True:
					ret, frame = cap.read()
					cv2.imshow("Camera index {} - Press q to close".format(index), frame) 
					key = cv2.waitKey(1) & 0xFF 
					if key == ord("q"): break

				cap.release()
				cv2.destroyAllWindows()

				input("Please Enter to continue")
				break

    #Resolution of Camera
	while True:
		try:
			print("\n=================================================")
			print("Resolution Types")
			print("1: Standard 480p [ 640, 480]")
			print("2: High 720p     [1280, 720]")
			print("3: Full HD 1080p [1920,1080])")

			userInput = int(input("\nPlease enter the Resolution number: "))
		except ValueError:
			input("Please input Numeric Values.")
		else:
			if userInput < 1 or userInput > 3:
				input("Please input from Command List.")
			else:
				if userInput == 1: width = 640; height = 480
				if userInput == 2: width = 1280; height = 720
				if userInput == 3: width = 1920; height = 1080
				break

	#Camera's FPS
	while True:
		try:
			print("\n=================================================")
			fps = int(input("Please enter the Frames Per Second (FPS): "))
		except ValueError:
			input("Please input Numeric Values.")
		else:
			if fps <= 0:
				input("Error: Please enter a positive number")
			else:
				break
	CameraSettings = {}
	CameraSettings["index"] = index
	CameraSettings["width"] = width
	CameraSettings["height"] = height
	CameraSettings["fps"] = fps
	
	return CameraSettings

#=======================================================================================================================
#=======================================================================================================================

#Set Tag type and range
def setTag():
	#Type of ArUco Tag (Maybe have standard one e.g. DICT_5X5_100 or select of list)
	good = False
	while good == False:
		try:
			#https://docs.opencv.org/4.x/d9/d6a/group__aruco.html#gac84398a9ed9dd01306592dd616c2c975
			print("\n=================================================")
			print("ArUco Tag List")
			print("0: DICT_4X4_50  | 1: DICT_4X4_100  | 2: DICT_4X4_250  | 3: DICT_4X4_1000")
			print("4: DICT_5X5_50  | 5: DICT_5X5_100  | 6: DICT_5X5_250  | 7: DICT_5X5_1000")
			print("8: DICT_6X6_50  | 9: DICT_6X6_100  | 10: DICT_6X6_250 | 11: DICT_6X6_1000")
			print("12: DICT_7X7_50 | 13: DICT_7X7_100 | 14: DICT_7X7_250 | 15: DICT_7X7_1000")
			print("16: DICT_ARUCO_ORIGINAL | 17: DICT_APRILTAG_16h5 | 18: DICT_APRILTAG_25h9")
			print("19: DICT_APRILTAG_36h10 | 20: DICT_APRILTAG_36h11\n")

			print("Formating               | DICT_ARUCO_ORIGINAL = 6X6_1024")
			print("DICT_5X5_100            | DICT_APRILTAG_16h5  = 4X4_30")
			print("5x5 - pixel (internal)  | DICT_APRILTAG_25h9  = 5X5_35")
			print("100 - Amount of id      | DICT_APRILTAG_36h10 = 6X6_2320")
			print("                        | DICT_APRILTAG_25h9  = 6X6_587")

			userInput = int(input("\nPlease enter the number for ArUCo tag: "))

		except ValueError:
			input("Please input Numeric Values.")
		else:
			if userInput < 0 or userInput > 20:
				input("Please input from Command List.")
			else:
				if userInput == 0: tagType = "DICT_4X4_50"; range = 50
				elif userInput == 1: tagType = "DICT_4X4_100"; range = 100
				elif userInput == 2: tagType = "DICT_4X4_250"; range = 250
				elif userInput == 3: tagType = "DICT_4X4_1000"; range = 100
				elif userInput == 4: tagType = "DICT_5X5_50"; range = 50
				elif userInput == 5: tagType = "DICT_5X5_100"; range = 100
				elif userInput == 6: tagType = "DICT_5X5_250"; range = 250
				elif userInput == 7: tagType = "DICT_5X5_1000"; range = 1000
				elif userInput == 8: tagType = "DICT_6X6_50"; range = 50
				elif userInput == 9: tagType = "DICT_6X6_100"; range = 100
				elif userInput == 10: tagType = "DICT_6X6_250"; range = 250
				elif userInput == 11: tagType = "DICT_6X6_1000"; range = 100
				elif userInput == 12: tagType = "DICT_7X7_50"; range = 50
				elif userInput == 13: tagType = "DICT_7X7_100"; range = 100
				elif userInput == 14: tagType = "DICT_7X7_250"; range = 250
				elif userInput == 15: tagType = "DICT_7X7_1000"; range = 1000
				elif userInput == 16: tagType = "DICT_ARUCO_ORIGINAL"; range = 1024
				elif userInput == 17: tagType = "DICT_APRILTAG_16h5"; range = 30
				elif userInput == 18: tagType = "DICT_APRILTAG_25h9"; range = 35
				elif userInput == 19: tagType = "DICT_APRILTAG_36h10"; range = 2320
				elif userInput == 20: tagType = "DICT_APRILTAG_36h11"; range = 587
				good = True
	
	TagSettings = {}
	TagSettings["tagType"] = tagType
	TagSettings["range"] = range

	return TagSettings

#=======================================================================================================================
#=======================================================================================================================

#GUI Components
running = True
cameraSetting = {}

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
		print("|         1 : Camera Select + Calibrate         |")
		print("|               2 : Generate Tags               |")
		print("|         3 : Detect Pose (Eye to Hand)         |")
		print("|         4 : Follow Pose (Eye in Hand)         |")
		print("|               0 : Close Program               |")
		print("|                                               |")
		print("=================================================")

		try:
			command = int(input("\nCommand? "))
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

	elif command == 1: #Camera Select + Calibration
		print("CALIBRATION")

		#Obtain Camera/s
		cameraSetting = getCameras()

		while True:
			try:
				print("\n=================================================")
				userInput = int(input("Create Images (0:False | 1:True)? "))
			except ValueError:
				input("Please input Numeric Values.")
			else:
				if userInput < 0 or userInput > 1:
					input("Please input from Command List.")
				else:
					if userInput == 1:
						Calibrate.camCapture(cameraSetting)
					break

		Calibrate.Calibration()
			
	elif command == 2: #Generate Tags
		print("GENERATE TAGS")
		tagSetting = setTag()
		GenerateTags(tagSetting)

	elif command == 3: #Eye to Hand
		print("EYE TO HAND")
		tagSetting = setTag()
		PoseDetector.poseDetector(PoseDetector, None, None, None, tagSetting, cameraSetting)
		input("Press Enter to continue")

	elif command == 4: #Eye in Hand
		print("EYE IN HAND")

		while True:
			try:
				print("\n=================================================")
				print("Set Values:")
				inputX = int(input("X: "))
				inputY = int(input("Y: "))
				inputZ = int(input("Z: "))
			except ValueError:
				input("Please input Numeric Values.")
			else:
				break

		tagSetting = setTag()
		PoseDetector.poseDetector(PoseDetector, inputX, inputY, inputZ, tagSetting, cameraSetting)
		input("Press Enter to continue")

	#ERROR CASE
	else:
		input("ERROR")


print("EXITED VIA COMMAND")