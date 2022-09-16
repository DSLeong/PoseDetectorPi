import cv2 as cv
import numpy as np
import cv2.aruco as aruco
import sys
import copy
import argparse
from utils import ARUCO_DICT, aruco_display
import Calibrate



class MarkerDetector:
    def __init__(self):
        self.marker = aruco.getPredefinedDictionary(aruco.DICT_5X5_100)

    def detect(self):
        #get a dictionary of what m,arkers are needed
        arucoDict = self.marker
        #set parameters (default)
        arucoParams = aruco.DetectorParameters_create()
        #start capturing video
        vid_capture = cv.VideoCapture(0)


        while (vid_capture.grab()):
            #ret is whether the connection is good, frame is the fram from the camera
            ret, inputImage = vid_capture.read()
            #exit if connection is bad
            if ret == False: 
                break
            (markerCorners, markerIDs, rejected) = cv.aruco.detectMarkers(inputImage, arucoDict, parameters=arucoParams)
            
            detected_markers = aruco_display(markerCorners, markerIDs, rejected, inputImage)
            
            aruco.drawDetectedMarkers(inputImage, markerCorners, markerIDs)

            cv.imshow("out", inputImage)
            #wait for 'q' key to exit
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        vid_capture.release()
        cv.destroyAllWindows()





def main():
    arucoDetect = MarkerDetector()
    while True:
        print('please choose a number')
        print('1 : Calibrate Camera')
        print('2 : detect markers')
        selection = input()

        #if selection == 1:
         #   Calibrate.Calibrate()
    arucoDetect.detect()

if __name__ == "__main__":
    main()

