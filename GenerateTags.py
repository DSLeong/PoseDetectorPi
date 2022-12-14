import argparse
import cv2
import numpy as np
import os
import sys
import tkinter as tk
from   tkinter import filedialog
from utils import ARUCO_DICT


class GenerateTags:
    def __init__(self, TagSettings):
        #Find/Create Directory
        while True:
            try:
                print("\n=================================================")
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
                        while True:
                            print("\n=================================================")
                            print("Please choose the directory where the ArUCo tag will be saved")
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
               
        #ID of ArUco Tag
        while True:
            try:
                print("\n=================================================")
                iden = int(input("Please enter the ID of ArUCo tag to generate: "))
            except ValueError:
                input("Please input Numeric Values.")
            else:
                if iden < 0 or iden > int(TagSettings["range"]) - 1:
                    input("Please input value within range of 0 to " + str(int(TagSettings["range"]) - 1))
                else:
                    break
        
        #Size of Tag (pixel) or just have sets of values or standard value
        while True:
            try:
                print("\n=================================================")
                size = int(input("Please enter the size of ArUCo tag to generate (pixel): "))
            except ValueError:
                input("Please input Numeric Values.")
            else:
                if size <= 0:
                    print("Error: Please enter a positive number")
                else:
                    break

        # Check to see if the dictionary is supported
        arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[TagSettings["tagType"]])

        print("\n=================================================")
        print("Generating ArUCo tag of type '{}' with ID '{}'".format(TagSettings["tagType"], iden))
        tag_size = size
        tag = np.zeros((tag_size, tag_size, 1), dtype="uint8")
        cv2.aruco.drawMarker(arucoDict, iden, tag_size, tag, 1)

        # Save the tag generated
        tag_name = f'{dirpath}/{TagSettings["tagType"]}_id_{iden}.png'
        cv2.imwrite(tag_name, tag)
        cv2.imshow("ArUCo Tag", tag)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
