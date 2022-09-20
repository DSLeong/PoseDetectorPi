import math
import time

#import pantilthat

class PanTilt:

    debugEnablePanTilt = False

    #Reset To Default Posistion (Pan 0, Tilt 0)
    def reset():
        print("Reset")
        if debugEnablePanTilt:
            pantilthat.pan(0)
            pantilthat.tilt(0)


    #Eye to Hand (Stationary)
    def EyeToHand():
        print("EyeToHand")
        reset()

    #Eye in Hand (Follow)
    def EyeInHand(x,y,z,ex,ey,ez):
        print("EyeInHand")
        reset()

        inputX, inputY, inputZ = 0
        inputNum = false

        #Program to follow
        while not inputNum:
            print("Set Values:")
            inputX, inputY, inputZ = input("Set Follow Values (x,y,z)? ")

            if not inputX.isnumeric() or not inputY.isnumeric() or not inputY.isnumeric():
                inputNum = false
                print("Please input Numeric Values.")
            else:
                inputNum = true
                inputX, inputY, inputZ = int(inputX), int(inputY), int(inputZ)
        

        if debugEnablePanTilt:
            #=============================
            #Pan
            #=============================
            pan = get_servo_one() + 1
            #ey is left?
            if ey >= 0 and ey < 180:
                if y > inputY:
                    if pan > 90 or pan < -90:
                        print("Error")
                    else:
                        pantilthat.pan(pan)
                else:
                    if pan > 90 or pan < -90:
                        print("Error")
                    else:
                        pantilthat.pan(pan)

            #ey is Right?
            else:
                if y > inputY:
                    if pan > 90 or pan < -90:
                        print("Error")
                    else:
                        pantilthat.pan(pan)
                else:
                    if pan > 90 or pan < -90:
                        print("Error")
                    else:
                        pantilthat.pan(pan)


            #=============================
            #Tilt
            #=============================
            tilt = get_servo_two() + 1
            #ey is left?
            if ey >= 0 and ey < 180:
                if y > inputY:
                    if tilt > 90 or tilt < -90:
                        print("Error")
                    else:
                        pantilthat.tilt(tilt)
                else:
                    if tilt > 90 or tilt < -90:
                        print("Error")
                    else:
                        pantilthat.tilt(tilt)

            #ey is Right?
            else:
                if y > inputY:
                    if tilt > 90 or tilt < -90:
                        print("Error")
                    else:
                        pantilthat.tilt(tilt)
                else:
                    if tilt > 90 or tilt < -90:
                        print("Error")
                    else:
                        pantilthat.tilt(tilt)

        Display(x,y,z,ex,ey,ez)


    #Display Pose
    def Display(x,y,z,ex,ey,ez):
        print("\n===========================")
        print("|    Translation  (mm)    |")
        print("===========================")
        print("|                          ")
        print("|  X: {:4.0f}".format(x))
        print("|  Y: {:4.0f}".format(y))
        print("|  Z: {:4.0f}".format(z))
        print("|                          ")
        print("===========================")
        print("|    Rotation  (Eular)    |")
        print("===========================")
        print("|                          ")
        print("| EulX: {:4.0f}".format(ex))
        print("| EulY: {:4.0f}".format(ey))
        print("| EulZ: {:4.0f}".format(ez))
        print("|                          ")
        print("===========================")
        print("|Press 'q' on cap  to stop|")
        print("===========================\n")
