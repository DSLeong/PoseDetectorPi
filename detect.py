import numpy as np 
import cv2
import cv2.aruco as aruco
import math

from PanTilt import PanTilt as PanTilt

class PoseDetector:
    #Check if Rotation Matrix
    def isRotationMatrix(R):
        Rt = np.transpose(R)
        shouldBeIdentity = np.dot(Rt, R)
        I = np.identity(3, dtype=R.dtype)
        n = np.linalg.norm(I - shouldBeIdentity)
        return n < 1e-6

    #Convert Rotation 3x3 Matrix to Eular Angles 
    def rotationMatrixToEulerAngles(R):
        assert (isRotationMatrix(R))
        
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
        
        return np.array([x, y, z]) #returns pitch, roll and yaw


    def poseDetector():
        marker_size = 100

        #with open('Calibrate.npy', 'rb') as f: 
        #    camera_matrix = np.load(f)
        #    camera_distortion = np.load(f)
            
        camera_matrix = np.load(calibration_matrix.npy)
        camera_distortion = np.load(distortion_coefficients.npy)

        aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)

        cap = cv2.VideoCapture(0)

        #camera_width = 640
        #camera_height = 480 
        #camera_frame_rate = 40 

        #cap.set(2, camera_width)
        #cap.set(4, camera_height)
        #cap.set(5, camera_frame_rate)

        #check of 'in' or 'of'

        while True:
            ret, frame = cap.read()

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            corners, ids, rejected = aruco.detectMarkers(gray_frame, aruco_dict, camera_matrix, camera_distortion)

            if ids != None: 
            
                aruco.drawDetectedMarkers(frame, corners)
            
                rvec_list_all, tvec_list_all, _objPoints = aruco.estimatePoseSingleMarkers(corners, marker_size, camera_matrix, camera_distortion)
            
                rvec = rvec_list_all[0][0]
                tvec = tvec_list_all[0][0]
            
                aruco.drawAxis(frame, camera_matrix, camera_distortion, rvec, tvec, 100)
                
                rvec_flipped = rvec * -1
                tvec_flipped = tvec * -1
                rotation_matrix, jacobian = cv2.Rodrigues(rvec_flipped)
                realworld_tvec = np.dot(rotation_matrix, tvec_flipped)
                
                #Translation
                x = realworld_tvec[0]
                y = realworld_tvec[1]
                z = realworld_tvec[2]
                #pitch, roll, yaw 
                eularX, eularY, eularZ = rotationMatrixToEulerAngles(rotation_matrix)

                PanTilt.EyeInHand(x, y, z, eularX, eularY, eularZ)
                PanTilt.Display(x, y, z, eularX, eularY, eularZ)

                #tvec_str = "x=%4.0f y=%4.0f z=%4.0f yaw=%4.0f"%(realworld_tvec[0], realworld_tvec[1], realworld_tvec[2], math.degrees(yaw))
                #cv2.putText(frame, tvec_str, (20, 460), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2, cv2.LINE_AA)
                
            cv2.imshow('Output', frame) 

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'): break

        cap.release()
        cv2.destroyAllWindows()