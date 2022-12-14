import argparse
import cv2 as cv
import numpy as np
import os
import re
import time
import tkinter as tk
from   tkinter import filedialog

class Calibrate:

    #Produce Images from Camera for Calibration
    def camCapture(cameraSetting, flip, dirpath):

        index = cameraSetting["index"]
        width = cameraSetting["width"]
        height = cameraSetting["height"]
        fps = cameraSetting["fps"]
             


        print("Press 'q' on capture to stop")

        cap = cv.VideoCapture(index)
        cap.set(cv.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, height)
        cap.set(cv.CAP_PROP_FPS, fps)

        frameCount = 0
        capImageCount = 0

        timeStart = time.time()

        print(type(cameraSetting["index"]))
        print(type(cameraSetting["width"]))
        print(type(cameraSetting["height"]))
        print(type(cameraSetting["fps"]))
        print(type(flip))
        print(type(dirpath))

        while True: 
            #reading camera frame
            ret, frame = cap.read()
            if flip: frame = cv.flip(frame,-1)
            #Display Video
            cv.imshow("Image Feed - Press 'q' to stop", frame)

            #Capture Image
            frameCount += 1

            if frameCount == 30:
                img = "cap_image_" + str(capImageCount) + ".jpg"
                #cv.imwrite(os.path.join(dirpath, img), frame)

                capImageCount += 1
                frameCount = 0
            
            
    
            key = cv.waitKey(1) & 0xFF 
            if key == ord("q"): break

        cap.release()
        cv.destroyAllWindows()

        elapseTime = time.time() - timeStart
        print("\n=================================================")
        print("Created " + str(capImageCount) + " image/s")
        print("Elapsed Time for Image Creation: " + str(elapseTime) + " seconds")

    #=======================================================================================================================
	#=======================================================================================================================

    #Calibration of Camera
    def Calibration(dirpath, width, height, square_size):

        images = [file for file in os.listdir(dirpath) if re.findall(r"\w+\.jpg", file)]

        # Apply camera calibration operation for images in the given directory path.

        # termination criteria
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(8,6,0)
        objp = np.zeros((height*width, 3), np.float32)
        objp[:, :2] = np.mgrid[0:width, 0:height].T.reshape(-1, 2) * square_size

        # Arrays to store object points and image points from all the images.
        objpoints = []  # 3d point in real world space
        imgpoints = []  # 2d points in image plane.

        #Calibrate Images
        print("Rendering Calibration")
        usableImages = 0
        for fname in images:
            print(fname)

            #Retrieve and grayscale image
            img = cv.imread(os.path.join(dirpath, fname))
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

            # Find the chess board corners within image
            ret, corners = cv.findChessboardCorners(gray, (width, height), None)

            # If found, add object points, image points (after refining them)
            if ret:
                usableImages += 1
                objpoints.append(objp)

                corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
                imgpoints.append(corners2)

                # Draw and display the corners
                img = cv.drawChessboardCorners(img, (width, height), corners2, ret)

            #Display image with Calibration (May not need)
            cv.imshow("Image Calibration",img)
            cv.waitKey(1000)

        cv.destroyAllWindows()
        

        #Calibration of Camera
        print("\nCalibrating Camera using Images - Please Wait")
        timeStart = time.time()
        ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
        elapseTime = time.time() - timeStart
        
        print("\n=================================================")
        print("Elapsed Time for Calibration: " + str(elapseTime) + " seconds")
        print("Amount of Used Images: " + str(usableImages) + " out of " + str(len(images)))

        print("\nCalibration Matrix:")
        print(mtx)
        print("\nDistortion:")
        print(dist)

        np.save("calibration_matrix", mtx)
        np.save("distortion_coefficients", dist)

