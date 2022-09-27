import argparse
import cv2
import numpy as np
import os
import sys
import tkinter as tk
from   tkinter import filedialog
from utils import ARUCO_DICT


class GenerateTags:
    def __init__(self):
        #Find/Create Directory (Maybe place within GUI?)
        while True:
            try:
                userInput = int(input("Create Directory for Tag (0:False 1:True)? "))
            except ValueError:
                input("Please input Numeric Values.")
            else:
                if userInput < 0 or userInput > 1:
                    input("Please input from Command List.")
                else:
                    if userInput == 1: #Create Directory
                        dirName = "Tags"
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
                        print("Please choose the directory where the ArUCo tag will be saved")
                        input("Press enter to continue")
                        root = tk.Tk()
                        root.withdraw()
                        dirpath = filedialog.askdirectory()
                        print(dirpath)
                        break
                    else:
                        print("ERROR")


        #Type of ArUco Tag (Maybe have standard one e.g. DICT_5X5_100 or select of list)
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

                tagType = int(input("Please enter the type of ArUCo tag to generate: "))

            except ValueError:
                input("Please input Numeric Values.")
            else:
                if tagType < 0 or tagType > 20:
                    input("Please input from Command List.")
                else:
                    if tagType == 0: tagType = "DICT_4X4_50"; range = 50;
                    elif tagType == 1: tagType = "DICT_4X4_100"; range = 100;
                    elif tagType == 2: tagType = "DICT_4X4_250"; range = 250;
                    elif tagType == 3: tagType = "DICT_4X4_1000"; range = 100;
                    elif tagType == 4: tagType = "DICT_5X5_50"; range = 50;
                    elif tagType == 5: tagType = "DICT_5X5_100"; range = 100;
                    elif tagType == 6: tagType = "DICT_5X5_250"; range = 250;
                    elif tagType == 7: tagType = "DICT_5X5_1000"; range = 1000;
                    elif tagType == 8: tagType = "DICT_6X6_50"; range = 50;
                    elif tagType == 9: tagType = "DICT_6X6_100"; range = 100;
                    elif tagType == 10: tagType = "DICT_6X6_250"; range = 250;
                    elif tagType == 11: tagType = "DICT_6X6_1000"; range = 100;
                    elif tagType == 12: tagType = "DICT_7X7_50"; range = 50;
                    elif tagType == 13: tagType = "DICT_7X7_100"; range = 100;
                    elif tagType == 14: tagType = "DICT_7X7_250"; range = 250;
                    elif tagType == 15: tagType = "DICT_7X7_1000"; range = 1000;
                    elif tagType == 16: tagType = "DICT_ARUCO_ORIGINAL"; range = 1024;
                    elif tagType == 17: tagType = "DICT_APRILTAG_16h5"; range = 30;
                    elif tagType == 18: tagType = "DICT_APRILTAG_25h9"; range = 35;
                    elif tagType == 19: tagType = "DICT_APRILTAG_36h10"; range = 2320;
                    elif tagType == 20: tagType = "DICT_APRILTAG_36h11"; range = 587;
                    good = True

               
        #ID of ArUco Tag (Need to check if exists within type)
        good = False
        print(range)
        while not good:
            try:
                iden = int(input("Please enter the ID of ArUCo tag to generate: "))
            except ValueError:
                input("Please input Numeric Values.")
            else:
                if iden < 0 or iden > range - 1:
                    input("Please input value within range of 0 to " + str(range - 1))
                else:
                    good = True
        
        #Size of Tag (pixel) or just have sets of values or standard value
        good = False
        while good == False:
            try:
                size = int(input("Please enter the size of ArUCo tag to generate (pixel): "))
            except ValueError:
                input("Please input Numeric Values.")
            else:
                if size <= 0:
                    print("Error: Please enter a positive number")
                else:
                    good = True

        # Check to see if the dictionary is supported
        arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[tagType])

        print("Generating ArUCo tag of type '{}' with ID '{}'".format(tagType, iden))
        tag_size = size
        tag = np.zeros((tag_size, tag_size, 1), dtype="uint8")
        cv2.aruco.drawMarker(arucoDict, iden, tag_size, tag, 1)

        # Save the tag generated
        tag_name = f'{dirpath}/{tagType}_id_{iden}.png'
        cv2.imwrite(tag_name, tag)
        cv2.imshow("ArUCo Tag", tag)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
