#Initialise Modules
from Calibrate import Calibrate as Calibrate
from GenerateTags import GenerateTags as GenerateTags
from PoseDetector import PoseDetector as PoseDetector
import cv2

#GUI Components
running = True

class GUI:
	def __init__(self):
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
								cameraList = self.getCameras()
								Calibrate.camCapture(cameraList)
							break

				Calibrate.Calibration()
			
			elif command == 2: #Generate Tags
				print("GENERATE TAGS")
				tagSetting = self.setTag()
				GenerateTags(tagSetting)

			elif command == 3: #Eye to Hand
				print("EYE TO HAND")
				tagSetting = self.setTag()
				cameraList = self.getCameras()
				PoseDetector.poseDetector(PoseDetector, None, None, None, tagSetting, cameraList)
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

				tagSetting = self.setTag()
				PoseDetector.poseDetector(PoseDetector, inputX, inputY, inputZ, tagSetting, cameraList)
				input("Press Enter to continue")

			#ERROR CASE
			else:
				input("ERROR")


		print("EXITED VIA COMMAND")

	#=======================================================================================================================
	#=======================================================================================================================

	#Get Camera Data
	#https://stackoverflow.com/questions/8044539/listing-available-devices-in-python-opencv
	#https://stackoverflow.com/questions/11420748/setting-camera-parameters-in-opencv-python
	def getCameras():

        #List camera/s
		cameraList = []
		i = 0
		while i < 10:
			cap = cv2.VideoCapture(i)
			if cap.read()[0]:
				arr.append(i)
				cap.release()
			i += 1

		#Set Camera
		while True:
			try:
				print("List of avaliable camera/s index")
				i = 0
				for cam in cameraList:
					print("{}: Camera Index {}".format(i,cam))

				userInput = int(input("Select camera index: "))
			except ValueError:
				input("Please input Numeric Values.")
			else:
				if userInput < 0 or userInput > len(cameraList) - 1:
					input("Please input from Command List.")
				else:
					index = cameraList[userInput]

					cap = cv2.VideoCapture(0)
					ret, frame = cap.read()
					cv2.imshow("Camera index {}".format(index), frame) 
					cv2.waitKey(2000)
					cap.release()
					cv2.destroyAllWindows()
					break

        #Resolution of Camera
		while True:
			try:
				print("\nResolution Types")
				print("1: Standard 480p [640,480]")
				print("2: High 720p 	[1280,720]")
				print("3: Full HD 1080p [1920,1080])")

				userInput = int(input("Please enter the Resolution: "))
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
		CameraSettings["height"] = tagType
		CameraSettings["fps"] = tagType

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
				print("ArUco Tag List")
				print("0: DICT_4X4_50  | 1: DICT_4X4_100  | 2: DICT_4X4_250  | 3: DICT_4X4_1000")
				print("4: DICT_5X5_50  | 5: DICT_5X5_100  | 6: DICT_5X5_250  | 7: DICT_5X5_1000")
				print("8: DICT_6X6_50  | 9: DICT_6X6_100  | 10: DICT_6X6_250 | 11: DICT_6X6_1000")
				print("12: DICT_7X7_50 | 13: DICT_7X7_100 | 14: DICT_7X7_250 | 15: DICT_7X7_1000")
				print("16: DICT_ARUCO_ORIGINAL | 17: DICT_APRILTAG_16h5 | 18: DICT_APRILTAG_25h9")
				print("19: DICT_APRILTAG_36h10 | 20: DICT_APRILTAG_36h11\n")

				print("Formating                | DICT_ARUCO_ORIGINAL = 6X6_1024")
				print("DICT_5X5_100             | DICT_APRILTAG_16h5  = 4X4_30")
				print("5x5 - pixel (internal)   | DICT_APRILTAG_25h9  = 5X5_35")
				print("100 - Amount of id       | DICT_APRILTAG_36h10 = 6X6_2320")
				print("                         | DICT_APRILTAG_25h9  = 6X6_587")

				userInput = int(input("Please enter the type of ArUCo tag to generate: "))

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
