from ast import Lambda
from turtle import left
import numpy as np
import cv2 as cv
import os
import argparse
from   tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from utils import ARUCO_DICT
from GenerateTags import GenerateTags
from Calibrate import Calibrate
from PoseDetector import PoseDetector

class Gui:

    displayHeight = 480
    displayWidth = 640

    defaultPadY = 25
    defaultPadX = 10

    welcomeMessage = "Hi! welcome to group fourexplore's pose detection system read below to get started."
    genTagsMessage = "Generate tags will create a file which you can use to print out a tag, using this tag in the next stages will enable you to estimate\nthe pose of the tag in 3D space!"
    calibrateMessage = "This tab allows for our program to get a better understand of where your tag is in space, calibrating the camera is a necessary\nphase before you can continue to Detect Pose."
    detectPoseMessage = "This tab will use the camera to tell you just where the tag is in 3D space."

    navbarOptions = {"home":"Home", "camera" : "Camera Settings", "generate" : "Generate Markers", "calibrate" : "Calibrate", "detect" : "Detect Pose"}

    txtBodyFormatting = 'TkDefaultFont 8'
    txtHeadingFormatting = 'TkDefaultFont 9 bold'

    resOptions = { "1: Standard 480p  [640, 480]" : [640 , 480], "2: High 720p  [1280, 720]" : [1280, 720], "3: Full HD 1080p [1920,1080])" : [1920,1080]}



    def __init__(self):
        self.state = self.navbarOptions["home"]
        self.window = Tk()
        self.window.geometry("640x480+0+0")
        self.camSettingsRun = False
        self.getCamList()
        self.mainDisplayFrame = tk.Frame()
        self.gui_navbar()
        self.draw_home()
        self.window.mainloop()
        
    
    def draw(self, tab):
        self.mainDisplayFrame.forget()
        self.mainDisplayFrame.destroy()
        


        if(tab == self.navbarOptions["home"]):
            self.state = self.navbarOptions["home"]
            self.draw_home()
        if(tab == self.navbarOptions["camera"]):
            self.state = self.navbarOptions["camera"]
            self.draw_camera()
        if(tab == self.navbarOptions["generate"]):
            self.state = self.navbarOptions["generate"]
            self.draw_generate()
        if (tab == self.navbarOptions["calibrate"]):
            self.state = self.navbarOptions["calibrate"]
            self.draw_calibrate()
        if (tab == self.navbarOptions["detect"]):
            self.state = self.navbarOptions["detect"]
            self.draw_detect()

    def gui_navbar(self):
        topFrame = Frame(
            master = self.window,
            bg = "white")
        topFrame.pack(
            side = "top",
            fill = tk.X)
        Button(topFrame, text=self.navbarOptions["home"], bg="gray85", fg="gray1", activebackground="gray99", activeforeground="gray50", command= lambda: self.draw(self.navbarOptions["home"]) ).pack(side="left", fill=tk.X, ipadx=30, ipady=30, expand=True)
        Button(topFrame, text=self.navbarOptions["camera"], bg="gray85", fg="gray1", activebackground="gray99", activeforeground="gray50", command= lambda: self.draw(self.navbarOptions["camera"]) ).pack(side="left", fill=tk.X, ipadx=30, ipady=30, expand=True)
        Button(topFrame, text=self.navbarOptions["generate"], bg="gray85", fg="gray1", activebackground="gray99", activeforeground="gray50", command= lambda: self.draw(self.navbarOptions["generate"]) ).pack(side="left", fill=tk.X, ipadx=30, ipady=30, expand=True)
        Button(topFrame, text=self.navbarOptions["calibrate"], bg="gray85", fg="gray1", activebackground="gray99", activeforeground="gray50", command= lambda: self.draw(self.navbarOptions["calibrate"]) ).pack(side="left", fill=tk.X, ipadx=30, ipady=30, expand=True)
        Button(topFrame, text=self.navbarOptions["detect"], bg="gray85", fg="gray1", activebackground="gray99", activeforeground="gray50", command= lambda: self.draw(self.navbarOptions["detect"]) ).pack(side="left", fill=tk.X, ipadx=30, ipady=30, expand=True)

    def draw_home(self):
        self.mainDisplayFrame = tk.Frame(
            master= self.window,
            width = self.displayWidth,
            height= self.displayHeight)
        self.mainDisplayFrame.pack(side="top")
        Label(master=self.mainDisplayFrame, text=self.welcomeMessage, pady=self.defaultPadY,font=self.txtBodyFormatting).pack(anchor=tk.W)
        Label(master=self.mainDisplayFrame, text=self.navbarOptions["generate"], font=self.txtHeadingFormatting).pack(anchor=tk.W)
        Label(master=self.mainDisplayFrame, text=self.genTagsMessage, pady=self.defaultPadY, font=self.txtBodyFormatting, justify="left").pack(anchor=tk.W)
        Label(master=self.mainDisplayFrame, text=self.navbarOptions["calibrate"], font=self.txtHeadingFormatting).pack(anchor=tk.W)
        Label(master=self.mainDisplayFrame, text=self.calibrateMessage, pady=self.defaultPadY, font=self.txtBodyFormatting, justify="left").pack(anchor=tk.W)
        Label(master=self.mainDisplayFrame, text=self.navbarOptions["detect"], font=self.txtHeadingFormatting).pack(anchor=tk.W)
        Label(master=self.mainDisplayFrame, text=self.detectPoseMessage, pady=self.defaultPadY, font=self.txtBodyFormatting).pack(anchor=tk.W)

    def draw_camera(self):
        self.mainDisplayFrame = tk.Frame(
            master=self.window,
            width = self.displayWidth,
            height= self.displayHeight)
        self.mainDisplayFrame.pack()

        #choose camera
        Label(master=self.mainDisplayFrame, text='Please choose the camera you wish to use', pady=self.defaultPadY,font=self.txtBodyFormatting).grid(column=0, row=0, ipadx=10)


        #create combobox of cameras
        chosenCam = StringVar()
        self.camCB = ttk.Combobox(self.mainDisplayFrame, textvariable=chosenCam, width=20)
        self.camCB['values'] = [m for m in self.cameraList]
        self.camCB['state'] = 'readonly'
        self.camCB.set("Pick an Option")
        self.camCB.grid(column=1, row=0, ipadx=10)

        Label(master=self.mainDisplayFrame, text='Preview Camera:', pady=self.defaultPadY,font=self.txtBodyFormatting).grid(column=0, row=1, ipadx=10)
        #create button
        button = Button(master=self.mainDisplayFrame, text="...", activebackground="gray99", activeforeground="gray50", font=self.txtBodyFormatting, command=self.previewCamera )
        button.grid(column=1, row=1, ipadx=10)

        Label(master=self.mainDisplayFrame, text='Camera Resolution:', pady=self.defaultPadY,font=self.txtBodyFormatting).grid(column=0, row=2, ipadx=10)
        
        #create combobox of camera resolutions
        camResolution = StringVar()
        self.resolutionCB = ttk.Combobox(self.mainDisplayFrame, textvariable=camResolution, width=20)
        self.resolutionCB['values'] = [resOption for resOption in self.resOptions]
        self.resolutionCB['state'] = 'readonly'
        self.resolutionCB.set("Resolution Types")
        self.resolutionCB.grid(column=1, row=2, ipadx=10)

        Label(master=self.mainDisplayFrame, text='Please enter the Frames Per Second (FPS):', pady=self.defaultPadY,font=self.txtBodyFormatting).grid(column=0, row=3)

        self.camFPS = Entry(master=self.mainDisplayFrame, width = 10)
        self.camFPS.grid(column=1, row=3)

        Button(master=self.mainDisplayFrame, text="Save", activebackground="gray99", activeforeground="gray50", font=self.txtBodyFormatting, command=self.setCam ).grid(column=2, row=4, padx=20)

        self.camSettingsRun = True

    def previewCamera(self):
        if (self.camCB.get() == ""):
            return
        else:
            index = int(self.camCB.get())
            cap = cv.VideoCapture(index)
            while True:
                ret, frame = cap.read()
                cv.imshow("Camera index {} - Press q to close".format(index), frame) 
                key = cv.waitKey(1) & 0xFF 
                if key == ord("q"): break
            cap.release()
            cv.destroyAllWindows()

    def setCam(self):
        self.camSettings = {}
        error = False
        errorMsg = ""
        if (self.camCB.get() == ""):
            self.camSet = False
            error = True
            errorMsg += "Camera not set \n"
        else:
            self.camSettings["index"] = int(self.camCB.get())
        if (self.resolutionCB.get() == ""):
            error = True
            errorMsg += "Resolution not set \n"
        else:
            self.camSettings["width"]= self.resOptions[self.resolutionCB.get()][0]
            self.camSettings["height"]= self.resOptions[self.resolutionCB.get()][1]
        try:
            fps = int(self.camFPS.get())
        except ValueError: 
            error = True
            errorMsg += "Camera FPS not set \n"
        else: 
            if fps <= 0:
                error = True
                errorMsg += "Camera FPS not positive \n"
            else:
                self.camSettings["fps"] = fps
        if (error):
            tk.messagebox.showerror(title="Camera Settings Error", message=errorMsg)
        else:
            tk.messagebox.showinfo(title="Camera Settings", message="Camera settings saved")
        

            

    def getCamList(self):
        #get a list of cameras
        self.cameraList = []
        for i in range(10):
            cap = cv.VideoCapture(i)
            if (cap.read()[0]):
                self.cameraList.append(i)
                cap.release()

    def draw_generate(self):
        self.mainDisplayFrame = tk.Frame(
            master=self.window,
            width = self.displayWidth,
            height= self.displayHeight)
        self.mainDisplayFrame.pack()


        Label(master=self.mainDisplayFrame, text='Please choose the directory where the ArUCo tag will be saved', pady=self.defaultPadY,font=self.txtBodyFormatting).grid(column=0, row=0)
        Button(master=self.mainDisplayFrame, text="...", activebackground="gray99", activeforeground="gray50", font=self.txtBodyFormatting, command=self.get_tag_dirpath ).grid(column=1, row=0)
        

        Label(master=self.mainDisplayFrame, text='Please enter the ARuCo Dictionary:', pady=self.defaultPadY,font=self.txtBodyFormatting).grid(column=0, row=1)

        chosenDict = StringVar()
        self.dictCB = ttk.Combobox(self.mainDisplayFrame, textvariable=chosenDict, width=20)
        self.dictCB['values'] = [m for m in ARUCO_DICT]
        self.dictCB['state'] = 'readonly'
        self.dictCB.grid(column=1, row=1, ipadx=10)

        Label(master=self.mainDisplayFrame, text='Please enter the ID of the tag(1, 2, 3, 4, ... etc.):', pady=self.defaultPadY,font=self.txtBodyFormatting, justify='left').grid(column=0, row=2)

        self.arucoTagIDText = Entry(master=self.mainDisplayFrame, width = 10)
        self.arucoTagIDText.grid(column=1, row=2)
        
        Label(master=self.mainDisplayFrame, text='Please enter the size of the tag: (mm)', pady=self.defaultPadY,font=self.txtBodyFormatting).grid(column=0, row=3)

        self.arucoTagSizeText = Entry(master=self.mainDisplayFrame, width = 10)
        self.arucoTagSizeText.grid(column=1, row=3)

        Button(master=self.mainDisplayFrame, text="Generate Tag", activebackground="gray99", activeforeground="gray50", font=self.txtBodyFormatting, command=self.generate_params ).grid(column=2, row=4, padx=20)

    def generate_params(self):
        arucoDict = self.dictCB.get()
        
        arucoTagSize = self.arucoTagSizeText.get()

        error = False
        errorMsg = ""

        if arucoDict == "" :
            error = True
            errorMsg += "Tag Dictionary not set\n"

        try:
            self.tagDirpath
        except AttributeError:
            error = True
            errorMsg += "Tag Directory not set\n"

        try:
            tagID = int(self.arucoTagIDText.get())
        except ValueError: 
            error = True
            errorMsg += "Tag ID not set \n"
        else: 
            if tagID <= 0:
                error = True
                errorMsg += "Tag ID not positive \n"
            else:
                arucoTagID = tagID
        try:
            tagSize = int(self.arucoTagSizeText.get())
        except ValueError: 
            error = True
            errorMsg += "Tag size not set \n"
        else: 
            if tagSize <= 0:
                error = True
                errorMsg += "Tag size not positive \n"
            else:
                self.arucoTagSize = tagSize
        if (not error):
            tagSettings = {}
            tagSettings["dict"] = arucoDict
            tagSettings["size"] = arucoTagSize
            tagSettings["id"] = arucoTagID
            tagSettings["dirpath"] = self.tagDirpath

            GenerateTags(tagSettings)

        if (error):
            tk.messagebox.showerror(title="Generate Tags Error", message=errorMsg)
        else:
            tk.messagebox.showinfo(title="Generate Tag", message="Tag Generated")
            

        
        

    def get_tag_dirpath(self):
        root = tk.Tk()
        root.withdraw()
        self.tagDirpath = filedialog.askdirectory()

    def get_calib_dirpath(self):
        root = tk.Tk()
        root.withdraw()
        self.calibDirpath = filedialog.askdirectory()


    def draw_calibrate(self):
        self.mainDisplayFrame = tk.Frame(
            master=self.window,
            width = self.displayWidth,
            height= self.displayHeight)
        self.mainDisplayFrame.pack()

        Label(master=self.mainDisplayFrame, text='Please choose the directory where the calibration images will be saved', pady=self.defaultPadY,font=self.txtBodyFormatting).grid(column=0, row=0)
        Button(master=self.mainDisplayFrame, text="...", activebackground="gray99", activeforeground="gray50", font=self.txtBodyFormatting, command=self.get_calib_dirpath ).grid(column=1, row=0)

        Label(master=self.mainDisplayFrame, text='Flip Camera:', pady=self.defaultPadY, font=self.txtBodyFormatting).grid(column=0, row=1)
        self.flipCamSel = StringVar()
        r1 = ttk.Radiobutton(master=self.mainDisplayFrame, text='yes', value='y', variable=self.flipCamSel).grid(column=1, row=1)
        r1 = ttk.Radiobutton(master=self.mainDisplayFrame, text='no', value='n', variable=self.flipCamSel).grid(column=2, row=1)

        Label(master=self.mainDisplayFrame, text='Checkerboard:', pady=self.defaultPadY, font=self.txtBodyFormatting).grid(column=0, row=3)
        Label(master=self.mainDisplayFrame, text='Height:', pady=self.defaultPadY, font=self.txtBodyFormatting).grid(column=0, row=4)
        self.checkerboardHeight = Entry(master=self.mainDisplayFrame, width = 10)
        self.checkerboardHeight.grid(column=1, row=4)

        Label(master=self.mainDisplayFrame, text='Width:', pady=self.defaultPadY, font=self.txtBodyFormatting).grid(column=0, row=5)
        self.checkerboardWidth = Entry(master=self.mainDisplayFrame, width = 10)
        self.checkerboardWidth.grid(column=1, row=5)

        Label(master=self.mainDisplayFrame, text='Checkerboard square size (mm):', pady=self.defaultPadY, font=self.txtBodyFormatting).grid(column=0, row=6)
        self.checkerboardSqSize = Entry(master=self.mainDisplayFrame, width = 10)
        self.checkerboardSqSize.grid(column=1, row=6)
        
        Button(master=self.mainDisplayFrame, text="Start Calibration ", activebackground="gray99", activeforeground="gray50", font=self.txtBodyFormatting, command=self.start_calibration ).grid(column=2, row=6, padx=10)

        
    def start_calibration(self):
        
        error = False
        errorMsg = ""

        flip = self.flipCamSel.get()
        if flip == "":
            if flip == 'n':
                flip = False
            else:
                flip = True
        else:
            error = True
            errorMsg += "Flip cam not set \n"

        try:
            self.calibDirpath
        except AttributeError:
            error = True
            errorMsg += "Tag Directory not set\n"

        try:
            checkHeight = int(self.checkerboardHeight.get())
        except ValueError: 
            error = True
            errorMsg += "Checkerboard height not set \n"
        else: 
            if checkHeight <= 0:
                error = True
                errorMsg += "Checkerboard height not positive \n"

        try:
            checkWidth = int(self.checkerboardWidth.get())
        except ValueError: 
            error = True
            errorMsg += "Checkerboard width not set \n"
        else: 
            if checkWidth <= 0:
                error = True
                errorMsg += "Checkerboard width not positive \n"
            
        try:
            sqSize = int(self.checkerboardSqSize.get())
        except ValueError: 
            error = True
            errorMsg += "Checkerboard square size not set \n"
        else: 
            if sqSize <= 0:
                error = True
                errorMsg += "Checkerboard square size not positive \n"

        try:
            self.camSettings
        except AttributeError:
            error = True
            errorMsg += "Please enter camera settings \n"

        if error:  
            tk.messagebox.showerror(title="Calibrate Error", message=errorMsg)
        else:
            Calibrate.camCapture(self.camSettings, flip, self.calibDirpath)
            Calibrate(self.calibDirpath, checkHeight, checkWidth, sqSize)
    
    def draw_detect(self):
        self.mainDisplayFrame = tk.Frame(
            master=self.window,
            width = self.displayWidth,
            height= self.displayHeight)
        self.mainDisplayFrame.pack()

        #marker size
        Label(master=self.mainDisplayFrame, text='Please enter the size of the tag: (mm)', pady=self.defaultPadY,font=self.txtBodyFormatting).grid(column=0, row=0)

        self.arucoTagSizeDetect = Entry(master=self.mainDisplayFrame, width = 10)
        self.arucoTagSizeDetect.grid(column=1, row=0)

        Label(master=self.mainDisplayFrame, text='Flip camera?', pady=self.defaultPadY,font=self.txtBodyFormatting).grid(column=0, row=1)
        self.flipCamSel = StringVar()
        r1 = ttk.Radiobutton(master=self.mainDisplayFrame, text='yes', value='y', variable=self.flipCamSel).grid(column=1, row=1)
        r1 = ttk.Radiobutton(master=self.mainDisplayFrame, text='no', value='n', variable=self.flipCamSel).grid(column=2, row=1)
        

        Label(master=self.mainDisplayFrame, text='Please enter aruco dictionary: ', pady=self.defaultPadY,font=self.txtBodyFormatting).grid(column=0, row=2)
        chosenDict = StringVar()
        self.drawdictCB = ttk.Combobox(self.mainDisplayFrame, textvariable=chosenDict, width=20)
        self.drawdictCB['values'] = [m for m in ARUCO_DICT]
        self.drawdictCB['state'] = 'readonly'
        self.drawdictCB.grid(column=1, row=2, ipadx=10)

        Button(master=self.mainDisplayFrame, text="Start Calibration ", activebackground="gray99", activeforeground="gray50", font=self.txtBodyFormatting, command=self.start_detection ).grid(column=2, row=3, padx=10)

    def start_detection(self):
        error = False
        errorMsg = ""
        tagSettings = {}

        tagSettings["dict"] = self.drawdictCB.get()

        try:
            tagSize = int(self.arucoTagSizeDetect.get())
        except ValueError: 
            error = True
            errorMsg += "Tag size not set \n"
        else: 
            if tagSize <= 0:
                error = True
                errorMsg += "Tag size not positive \n"
            else:
                tagSettings["tagSize"] = tagSize

        arucoDict = self.drawdictCB.get()
        if arucoDict == "":
            error = True
            errorMsg += "Dictionary not set"
            

        tagSettings["dict"] = arucoDict
        
        flip = self.flipCamSel.get()
        if flip == 'n':
            tagSettings["flip"] = False
        else:
            tagSettings["flip"] = True

        try:
            self.camSettings
        except AttributeError:
            error = True
            errorMsg += "Please enter camera settings \n"
        if error:  
            tk.messagebox.showerror(title="Detect Pose Error", message=errorMsg)
        else:
            PoseDetector.poseDetector(PoseDetector, None, None, None, tagSettings, self.camSettings)







        


       


gui = Gui()
#gui.home()
