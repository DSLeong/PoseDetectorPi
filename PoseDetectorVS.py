import numpy as np
import cv2 as cv
import os
import argparse
import tkinter as tk
from   tkinter import filedialog

class Gui:

    display = {"home"}
    
    #def __init__(self):
        

    def home(self):
        self.state = "home"
        window = tk.Tk()
        for i in range(4):
            frame = tk.Frame(
                master=window,
                relief=tk.RAISED,
                borderwidth=1)
            frame.grid(row=1, column=i)
            label = tk.Label(master=frame, text=f"Row {1}\nColumn {i}")
            if i==0:
                label = tk.Label(master=frame, text="Home", )
            if i==1:
                label = tk.Label(master=frame, text="Generate Tags")
            if i==2:
                label = tk.Label(master=frame, text="Calibrate Camera")
            if i==3:
                label = tk.Label(master=frame, text="Detect Pose")
            label.pack()


        window.mainloop()

        


gui = Gui()
gui.home()
