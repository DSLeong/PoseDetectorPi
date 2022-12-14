import argparse
import cv2
import numpy as np
import os
import re
import time
import tkinter as tk
from   tkinter import filedialog

class Calibrate:

    #Produce Images from Camera for Calibration
    def camCapture(cameraSetting):

        #Find/Create Directory
        while True:
            try:
                print("\n=================================================")
                userInput = int(input("Create Directory for Images (0:False 1:True)? "))
            except ValueError:
                input("Please input Numeric Values.")
            else:
                if userInput < 0 or userInput > 1:
                    input("Please input from Command List.")
                else:
                    if userInput == 1: #Create Directory
                        dirName = "Capture_" + str(cameraSetting["index"]) + "_" + str(cameraSetting["height"])
                        try:
                            os.mkdir(dirName)
                        except FileExistsError:
                            print("Directory '" , dirName ,  "' already exists")
                        else:
                            print("Directory '" , dirName ,  "' Created")

                        dirpath = os.path.join(os.getcwd(), dirName)
                        print(dirpath)
                        break

                    elif userInput == 0: #Find Directory
                        while True:
                            print("\n=================================================")
                            print("Please choose the folder where to save checkerboard images:")
                            input("Press enter to continue")
                            root = tk.Tk()
                            root.withdraw()
                            dirpath = filedialog.askdirectory()
                            print(dirpath)
                            if dirpath == "":
                                input("Please select folder")
                            else:
                                break
                        break
                        
                    else:
                        print("ERROR")

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
                    if userInput == 0: flip = False
                    else: flip = True
                    break


        print("Press 'q' on capture to stop")

        cap = cv2.VideoCapture(cameraSetting["index"])
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, cameraSetting["width"])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cameraSetting["height"])
        cap.set(cv2.CAP_PROP_FPS, cameraSetting["fps"])

        frameCount = 0
        capImageCount = 0

        timeStart = time.time()
        while True: 
            #reading camera frame
            ret, frame = cap.read()
            if flip: frame = cv2.flip(frame,-1)

            #Capture Image
            frameCount += 1

            if frameCount == 30:
                img = "cap_image_" + str(capImageCount) + ".jpg"
                cv2.imwrite(os.path.join(dirpath, img), frame)

                capImageCount += 1
                frameCount = 0
            
            #Display Video
            cv2.imshow("Image Feed - Press 'q' to stop", frame)
    
            key = cv2.waitKey(1) & 0xFF 
            if key == ord("q"): break

        cap.release()
        cv2.destroyAllWindows()

        elapseTime = time.time() - timeStart
        print("\n=================================================")
        print("Created " + str(capImageCount) + " image/s")
        print("Elapsed Time for Image Creation: " + str(elapseTime) + " seconds")

    #=======================================================================================================================
	#=======================================================================================================================

    #Calibration of Camera
    def Calibration():

        #Find Directory
        while True:
            print("\n=================================================")
            print("Please choose the folder where the checkerboard images are located:")
            input("Press enter to continue")
            root = tk.Tk()
            root.withdraw()
            dirpath = filedialog.askdirectory()
            print(dirpath)
            if dirpath == "":
                input("Please select folder")
            else:
                #Check for images (in .jpg format)
                images = [file for file in os.listdir(dirpath) if re.findall(r"\w+\.jpg", file)]
                if len(images) < 1:
                    input(str(dirpath) + " - has no images (.jpg), please select a new folder")
                else:
                    break
        
        #Width of Checkerboard
        while True:
            try:
                print("\n=================================================")
                width = int(input("Please enter the width of the checkerboard (no. of corners): "))
            except ValueError:
                input("Please input Numeric Value.")
            else:
                if width <= 0:
                    print('Error: Please enter a positive number')
                else:
                    break

        #Height of Checkerboard
        while True:
            try:
                print("\n=================================================")
                height = int(input("Please enter the height of the checkerboard (no. of corners): "))
            except ValueError:
                input("Please input Numeric Value.")
            else:
                if height <= 0:
                    print('Error: Please enter a positive number')
                else:
                    break
       
        #Checkerboard square length
        while True:
            try:
                print("\n=================================================")
                square_size = float(input("Please enter the size of the squares (mm): "))
            except ValueError:
                input("Please input Numeric Value.")
            else:
                if square_size <= 0:
                    print('Error: Please enter a positive number')
                else:
                    break


        # Apply camera calibration operation for images in the given directory path.

        # termination criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

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
            img = cv2.imread(os.path.join(dirpath, fname))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Find the chess board corners within image
            ret, corners = cv2.findChessboardCorners(gray, (width, height), None)

            # If found, add object points, image points (after refining them)
            if ret:
                usableImages += 1
                objpoints.append(objp)

                corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
                imgpoints.append(corners2)

                # Draw and display the corners
                img = cv2.drawChessboardCorners(img, (width, height), corners2, ret)

            #Display image with Calibration (May not need)
            cv2.imshow("Image Calibration",img)
            cv2.waitKey(1000)

        cv2.destroyAllWindows()
        

        #Calibration of Camera
        print("\nCalibrating Camera using Images - Please Wait")
        timeStart = time.time()
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
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

