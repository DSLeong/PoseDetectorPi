import cv2
import math
import numpy as np
import os
from utils import ARUCO_DICT

from PanTilt import PanTilt as PanTilt
PanTiltEnable = True
try:
    import pantilthat
except ImportError:
    PanTiltEnable = False
    pass


class PoseDetector:

    #Check if Rotation Matrix
    def isRotationMatrix(R):
        Rt = np.transpose(R)
        shouldBeIdentity = np.dot(Rt, R)
        I = np.identity(3, dtype=R.dtype)
        n = np.linalg.norm(I - shouldBeIdentity)
        return n < 1e-6


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


    #Estimate Pose Values
    def poseDetector(self, inputX, inputY, inputZ):

        #if Calibration does not exist
        if not os.path.isfile("calibration_matrix.npy") or not os.path.isfile("distortion_coefficients.npy"):
            print("Calibration does not exist.")
            print("Please run Calibration first.")
            input("Press enter to continue")

        else:
            #Multiple different markers?
            good = False
            while good == False:
                try:
                    #https://docs.opencv.org/4.x/d9/d6a/group__aruco.html#gac84398a9ed9dd01306592dd616c2c975
                    print("ArUco tag List")
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

                    tagType = int(input("Please enter the type of ArUCo tag to detect: "))

                except ValueError:
                    input("Please input Numeric Values.")
                else:
                    if tagType < 0 or tagType > 20:
                        input("Please input from Command List.")
                    else:
                        if tagType == 0: tagType = "DICT_4X4_50"
                        elif tagType == 1: tagType = "DICT_4X4_100"
                        elif tagType == 2: tagType = "DICT_4X4_250"
                        elif tagType == 3: tagType = "DICT_4X4_1000"
                        elif tagType == 4: tagType = "DICT_5X5_50"
                        elif tagType == 5: tagType = "DICT_5X5_100"
                        elif tagType == 6: tagType = "DICT_5X5_250"
                        elif tagType == 7: tagType = "DICT_5X5_1000"
                        elif tagType == 8: tagType = "DICT_6X6_50"
                        elif tagType == 9: tagType = "DICT_6X6_100"
                        elif tagType == 10: tagType = "DICT_6X6_250"
                        elif tagType == 11: tagType = "DICT_6X6_1000"
                        elif tagType == 12: tagType = "DICT_7X7_50"
                        elif tagType == 13: tagType = "DICT_7X7_100"
                        elif tagType == 14: tagType = "DICT_7X7_250"
                        elif tagType == 15: tagType = "DICT_7X7_1000"
                        elif tagType == 16: tagType = "DICT_ARUCO_ORIGINAL"
                        elif tagType == 17: tagType = "DICT_APRILTAG_16h5"
                        elif tagType == 18: tagType = "DICT_APRILTAG_25h9"
                        elif tagType == 19: tagType = "DICT_APRILTAG_36h10"
                        elif tagType == 20: tagType = "DICT_APRILTAG_36h11"
                        good = True
            
            aruco_dict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT[tagType])

            #Get Marker Size
            while True:
                try:
                    marker_size = float(input("Please enter the size of the squares (mm):  "))
                except ValueError:
                    input("Please input Numeric Values.")
                else:
                    if marker_size <= 0:
                        print('Error: Please enter a positive number')
                    else:
                        break
            
            #Load Camera Calibration
            camera_matrix = np.load("calibration_matrix.npy")
            camera_distortion = np.load("distortion_coefficients.npy")

            #Eye in hand?
            follow = True
            if PanTiltEnable: PanTilt.reset()
            if inputX == None and inputY == None and inputZ == None:
                follow = False
            
            #Check for camera (Usually 0)
            cap = cv2.VideoCapture(0)

            while True:
                ret, frame = cap.read()
                if PanTiltEnable: frame = cv2.flip(frame,-1)

                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                corners, ids, rejected = cv2.aruco.detectMarkers(gray_frame, aruco_dict, camera_matrix, camera_distortion)

                #If Marker detected
                if len(corners) > 0: 
            
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
                        print("Follow")
                        if PanTiltEnable: PanTilt.EyeInHand(x, y, z, math.degrees(eulerX), math.degrees(eulerY), math.degrees(eulerZ),inputX,inputY,inputZ)
                    
                    #Display on Command Prompt
                    self.Display(self,x, y, z, math.degrees(eulerX), math.degrees(eulerY), math.degrees(eulerZ))

                    #Display on output
                    tvec_str = "x=%4.0f y=%4.0f z=%4.0f eulerZ=%4.0f"%(x, y, z, math.degrees(eulerZ))
                    cv2.putText(frame, tvec_str, (20, 460), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2, cv2.LINE_AA)
                
                cv2.imshow("Image Feed - Press 'q' to stop", frame) 

                #Check for exit
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'): break

            cap.release()
            cv2.destroyAllWindows()