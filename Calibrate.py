import numpy as np
import cv2 as cv
import os
import argparse
import tkinter as tk
from   tkinter import filedialog

class Calibrate:
    def Calibrate():

        print('Please choose the folder where the checkerboard images are located')
        input('Press enter to continue')
        root = tk.Tk()
        root.withdraw()
        dirpath = filedialog.askdirectory()
        print(dirpath)

        
        good = False
        while not good:
            width = input('Please enter the width of the checkerboard (mm): ')
            if not width.isnumeric():
                print('Error: Please enter a number')
            elif int(width) <= 0:
                print('Error: Please enter a positive number')
            else:
                width = int(width)
                good = True


        good = False
        while not good:
            height = input('Please enter the height of the checkerboard (mm): ')
            if not height.isnumeric():
                print('Error: Please enter a number')
            elif int(height) <= 0:
                print('Error: Please enter a positive number')
            else:
                height = int(height)
                good = True
       
        good = False
        while not good:
            square_size = input('Please enter the size of the squares (mm): ')
            if not square_size.isnumeric():
                print('Error: Please enter a number')
            elif int(square_size) <= 0:
                print('Error: Please enter a positive number')
            else:
                square_size = int(square_size)
                good = True
    
        # 2.4 cm == 0.024 m
        # square_size = 0.024

        good = False
        while not good:
            visualize = input('Visualise? True or False: ')
            if visual.lower() != "true" and visual.lower() != "false":
                print('Error: Please enter a true or false')
            else:
                good = True

        if visualize.lower() == "true":
            visualize = True
        else:
            visualize = False

        ret, mtx, dist, rvecs, tvecs = self.__calibrate(dirpath, square_size, visualize=visualize, width=width, height=height)

        print(mtx)
        print(dist)

        np.save("calibration_matrix", mtx)
        np.save("distortion_coefficients", dist)

    def __calibrate(dirpath, square_size, width, height, visualize=False):
        """ Apply camera calibration operation for images in the given directory path. """

        # termination criteria
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(8,6,0)
        objp = np.zeros((height*width, 3), np.float32)
        objp[:, :2] = np.mgrid[0:width, 0:height].T.reshape(-1, 2)

        objp = objp * square_size

        # Arrays to store object points and image points from all the images.
        objpoints = []  # 3d point in real world space
        imgpoints = []  # 2d points in image plane.

        images = os.listdir(dirpath)

        for fname in images:
            img = cv.imread(os.path.join(dirpath, fname))
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

            # Find the chess board corners
            ret, corners = cv.findChessboardCorners(gray, (width, height), None)

            # If found, add object points, image points (after refining them)
            if ret:
                objpoints.append(objp)

                corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
                imgpoints.append(corners2)

                # Draw and display the corners
                img = cv.drawChessboardCorners(img, (width, height), corners2, ret)

            if visualize:
                cv.imshow('img',img)
                cv.waitKey(0)


        ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

        return [ret, mtx, dist, rvecs, tvecs]
