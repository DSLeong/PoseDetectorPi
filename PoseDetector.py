import cv2
import math
import numpy as np

# Required to Run Simulation
import time
import simulation as simulate # Simulation Code
import sim # Simulation Software -- CoppeliaSim Directory

from PanTilt import PanTilt as PanTilt
from utils import ARUCO_DICT


class PoseDetector:

    #Check if Rotation Matrix
    def isRotationMatrix(R):
        Rt = np.transpose(R)
        shouldBeIdentity = np.dot(Rt, R)
        I = np.identity(3, dtype=R.dtype)
        n = np.linalg.norm(I - shouldBeIdentity)
        return n < 1e-6
    
    #=======================================================================================================================
	#=======================================================================================================================

    #Convert Rotation 3x3 Matrix to euler Angles 
    def rotationMatrixToEulerAngles(self, R):
        assert (self.isRotationMatrix(R))
        
        sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])
        
        singular = sy < 1e-6
        
        if not singular:
            x = math.atan2(R[2,1], R[2,2])
            y = math.atan2(-R[2,0], sy)
            z = math.atan2(R[1,0], R[0,0])
        else:
            x = math.atan2(-R[1,2], R[1,1])
            y = math.atan2(-R[2,0], sy)
            z = 0
        
        return np.array([x, y, z]) #returns pitch, roll and yaw (units?)


    #=======================================================================================================================
	#=======================================================================================================================

    #Display Pose
    def Display(self,x,y,z,ex,ey,ez):
        print("===========================")
        print("|    Translation  (mm)    |")
        print("===========================")
        print("|                          ")
        print("|  X (Red)  : {:4.0f}".format(x))
        print("|  Y (Green): {:4.0f}".format(y))
        print("|  Z (Blue) : {:4.0f}".format(z))
        print("|                          ")
        print("===========================")
        print("| Rotation (euler/degree) |")
        print("===========================")
        print("|                          ")
        print("| EulX: {:4.0f}".format(ex))
        print("| EulY: {:4.0f}".format(ey))
        print("| EulZ: {:4.0f}".format(ez))
        print("|                          ")
        print("===========================")
        print("|Press 'q' on cap  to stop|")
        print("===========================")
        print(" ")

    #=======================================================================================================================
	#=======================================================================================================================


    #Estimate Pose Values
    def poseDetector(self, inputX, inputY, inputZ, tagSetting, cameraSetting):
        #Set Tag Type
        aruco_dict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT[tagSetting["tagType"]])

        #Get Marker Size
        while True:
            try:
                print("\n=================================================")
                marker_size = float(input("Please enter the full length of the marker being used (mm): "))
            except ValueError:
                input("Please input Numeric Values.")
            else:
                if marker_size <= 0:
                    print('Error: Please enter a positive number')
                else:
                    break

        #Simulation Initiation
        while True:
            try:
                print("\n=================================================")
                print("\nIf you want to run simulation make sure it is running before you place your answer !!!")
                simulation = int(input("Run with Simulation: (0:No | 1:Yes)?: ")) # To Check if run Simulation
            except ValueError:
                input("Please input Numeric Values.")
            else:
                if simulation == 1:
                    joint_handle = []
                    clientID = 0
                    clientID, joint_handle = simulate.simulation_init()
                    print("---------------Simulation Initiated ----------------")
                    break
                elif simulation == 0:
                    break
                

        #Load Camera Calibration
        camera_matrix = np.load("calibration_matrix.npy")
        camera_distortion = np.load("distortion_coefficients.npy")

        #Eye in hand?
        follow = True
        flip = False
        PanTilt.reset()

        #Detect
        if inputX == None and inputY == None and inputZ == None:
            follow = False
        else:
            #Flip Camera
            while True:
                try:
                    print("\n=================================================")
                    userInput = int(input("Flip Camera? (0: No | 1: Yes)? "))
                except ValueError:
                    input("Please input Numeric Values.")
                else:
                    if userInput < 0 or userInput > 1:
                        input("Please input from Command List.")
                    else:
                        if userInput == 1: flip = True
                        break
            
        #Camera Setting
        cap = cv2.VideoCapture(cameraSetting["index"])
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, cameraSetting["width"])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cameraSetting["height"])
        cap.set(cv2.CAP_PROP_FPS, cameraSetting["fps"])

        while True:
            #
            ret, frame = cap.read()

            #Flip Vertically and Horizontally
            if flip: frame = cv2.flip(frame,-1)

            #
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            #
            corners, ids, rejected = cv2.aruco.detectMarkers(gray_frame, aruco_dict, camera_matrix, camera_distortion)

            #If Marker detected
            if len(corners) > 0: 
                #
                cv2.aruco.drawDetectedMarkers(frame, corners)
            
                #estimatePoseSingleMarkers
                #rvec_list_all = Rotation Vector of Marker/s from Camera
                #tvec_list_all = Translation Vector of Marker/s from Camera
                #
                rvec_list_all, tvec_list_all, _objPoints = cv2.aruco.estimatePoseSingleMarkers(corners, marker_size, camera_matrix, camera_distortion)
            
                #Obtain First Marker
                rvec = rvec_list_all[0][0]
                tvec = tvec_list_all[0][0]
                    
                #Draw Axes on Marker
                cv2.drawFrameAxes(frame, camera_matrix, camera_distortion, rvec, tvec, 50)
                
                #Calculate actual 'rvec' and 'tvec'
                rvec_flipped = rvec * -1
                tvec_flipped = tvec * -1
                rotation_matrix, jacobian = cv2.Rodrigues(rvec_flipped)
                realworld_tvec = np.dot(rotation_matrix, tvec_flipped)
                
                #Translation (mm)
                x = realworld_tvec[0]
                y = realworld_tvec[1]
                z = realworld_tvec[2]

                #Euler Angles (degree)
                eulerX, eulerY, eulerZ = self.rotationMatrixToEulerAngles(self, rotation_matrix)

                #If Eye in Hand
                if follow:
                    PanTilt.EyeInHand(x, y, z, math.degrees(eulerX), math.degrees(eulerY), math.degrees(eulerZ), inputX, inputY, inputZ)
                    
                #Display on Command Prompt
                self.Display(self,x, y, z, math.degrees(eulerX), math.degrees(eulerY), math.degrees(eulerZ))

                #Display on output
                tvec_str = "x=%4.0f y=%4.0f z=%4.0f eulerZ=%4.0f"%(x, y, z, math.degrees(eulerZ))
                cv2.putText(frame, tvec_str, (20, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2, cv2.LINE_AA)

                #Main Simulation Call     
                if simulation == 1:
                    simulate.simulation_run(x/1000,y/1000,z/1000,math.radians(eulerX),math.radians(eulerY),math.radians(eulerZ),joint_handle, clientID)
                
            #
            cv2.imshow("Pose Estimation - Press 'q' to stop", frame) 

            #Check for exit
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'): break
            
        #
        cap.release()
        cv2.destroyAllWindows()