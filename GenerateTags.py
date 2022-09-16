import cv2 as cv
import numpy as np
import argparse
from utils import ARUCO_DICT
import sys
import tkinter as tk
from   tkinter import filedialog

class GenerateTags:
    def __init__(self):
        ap = argparse.ArgumentParser()
        #ap.add_argument("-o", "--output", required=True, help="path to output folder to save ArUCo tag")
        #ap.add_argument("-i", "--id", type=int, required=True, help="ID of ArUCo tag to generate")
        ap.add_argument("-t", "--type", type=str, default="DICT_ARUCO_ORIGINAL", help="type of ArUCo tag to generate")
        ap.add_argument("-s", "--size", type=int, default=200, help="Size of the ArUCo tag")
        args = vars(ap.parse_args())

        print('Please choose the directory where the ArUCo tag will be saved')
        input('Press enter to continue')
        root = tk.Tk()
        root.withdraw()
        dirpath = filedialog.askdirectory()
        print(dirpath)

        good = False
        while good == False:
            iden = input('Please enter the ID of ArUCo tag to generate: ')
            
            if ARUCO_DICT.get(args["type"], None) == None:
	            print("ArUCo tag type '{args['type']}' is not supported")
                continue

            good = True

        # Check to see if the dictionary is supported
        

        arucoDict = cv.aruco.Dictionary_get(ARUCO_DICT[args["type"]])

        print("Generating ArUCo tag of type '{}' with ID '{}'".format(args["type"], args["id"]))
        tag_size = args["size"]
        tag = np.zeros((tag_size, tag_size, 1), dtype="uint8")
        cv.aruco.drawMarker(arucoDict, args["id"], tag_size, tag, 1)

        # Save the tag generated
        tag_name = '{args["output"]}/{args["type"]}_id_{args["id"]}.png'
        cv.imwrite(tag_name, tag)
        cv.imshow("ArUCo Tag", tag)
        cv.waitKey(0)
        cv.destroyAllWindows()
