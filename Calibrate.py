import numpy as np
import cv2
import os
import argparse
import tkinter as tk
from   tkinter import filedialog

class Calibrate:
    def camCapture():
        capImageCount = 0
        frameCount = 0

        print("Please choose the folder where to save checkerboard images:")
        input("Press enter to continue")
        root = tk.Tk()
        root.withdraw()
        dirpath = filedialog.askdirectory()
        print(dirpath)

        print("Press 'q' on capture to stop")

        cv2.namedWindow("Image Feed")
        cap = cv2.VideoCapture(0)

        while True: 
            #reading camera frame
            ret, frame = cap.read()
    
            #Capture Image
            frameCount += 1

            if frameCount == 30:
                img = "cap_image_" + str(capImageCount) + ".jpg"
                cv2.imwrite(os.path.join(dirpath, img), frame)

                capImageCount += 1
                frameCount = 0
            
            #Display Video
            cv2.imshow("Image Feed", frame)
    
            key = cv2.waitKey(1) & 0xFF 
            if key == ord("q"): break

        print("Created " + capImageCount + " image/s")

        cap.release()
        cv2.destroyAllWindows()

    def Calibration():
        print("Please choose the folder where the checkerboard images are located:")
        input("Press enter to continue")
        root = tk.Tk()
        root.withdraw()
        dirpath = filedialog.askdirectory()
        print(dirpath)
        
        #Width of Checkerboard
        good = False
        while not good:
            width = input("Please enter the width of the checkerboard (no. of corners): ")
            if not width.isnumeric():
                print("Error: Please enter a number")
            elif int(width) <= 0:
                print("Error: Please enter a positive number")
            else:
                width = int(width)
                print ("Width = " + str(width))
                good = True

        #Height of Checkerboard
        good = False
        while not good:
            height = input("Please enter the height of the checkerboard (no. of corners): ")
            if not height.isnumeric():
                print("Error: Please enter a number")
            elif int(height) <= 0:
                print("Error: Please enter a positive number")
            else:
                height = int(height)
                print ("Height = " + str(height))
                good = True
       
        #Checkerboard square length
        good = False
        while not good:
            square_size = input("Please enter the size of the squares (mm): ")
            if not square_size.isnumeric():
                print("Error: Please enter a number")
            elif float(square_size) <= 0:
                print("Error: Please enter a positive number")
            else:
                square_size = float(square_size)/1000
                print ("Square Size (m) = " + str(square_size))
                good = True


        # Apply camera calibration operation for images in the given directory path.

        # termination criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(8,6,0)
        objp = np.zeros((height*width, 3), np.float32)
        objp[:, :2] = np.mgrid[0:width, 0:height].T.reshape(-1, 2) * square_size

        # Arrays to store object points and image points from all the images.
        objpoints = []  # 3d point in real world space
        imgpoints = []  # 2d points in image plane.

        images = os.listdir(dirpath)


        #Calibrate Images
        print("Rendering Calibration")
        for fname in images:
            print(fname + "\n")

            img = cv2.imread(os.path.join(dirpath, fname))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Find the chess board corners
            ret, corners = cv2.findChessboardCorners(gray, (width, height), None)

            # If found, add object points, image points (after refining them)
            if ret:
                objpoints.append(objp)

                corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
                imgpoints.append(corners2)

                # Draw and display the corners
                img = cv2.drawChessboardCorners(img, (width, height), corners2, ret)

            #Display image with Calibration
            cv2.imshow("Image Calibration",img)
            cv2.waitKey(1000)

        #Save Calibration
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

        print("Calibration Matrix:")
        print(mtx)
        print("\nDistortion:")
        print(dist)

        np.save("calibration_matrix", mtx)
        np.save("distortion_coefficients", dist)

