import argparse
import cv2
import numpy as np
import os
import sys
import tkinter as tk
from   tkinter import filedialog
from utils import ARUCO_DICT


class GenerateTags:
    def __init__(self, tagSettings):

        # Check to see if the dictionary is supported
        arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[tagSettings["dict"]])

        tag_size = tagSettings["size"]
        iden = tagSettings["id"]
        tag = np.zeros((tag_size, tag_size, 1), dtype="uint8")
        cv2.aruco.drawMarker(arucoDict, iden, tag_size, tag, 1)

        # Save the tag generated
        tag_name = f'{tagSettings["dirpath"]}/{tagSettings["dict"]}_id_{tagSettings["id"]}.png'
        cv2.imwrite(tag_name, tag)
        cv2.imshow("ArUCo Tag", tag)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
