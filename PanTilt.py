import math
import time

#need to import
import pantilthat

class PanTilt:

    debugPanTilt = true

    #Reset To Default Posistion (Pan 0, Tilt 0)
    def reset():
        print("Reset")
        pantilthat.pan(0)
        pantilthat.tilt(0)


    #Eye to Hand (Stationary)
    def EyeToHand():
        print("EyeToHand")
        reset()

    #Eye in Hand (Follow)
    def EyeInHand(x,y,z,ex,ey,ez):
        print("EyeInHand")
        
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
        

        if debugPanTilt:
            #=============================
            #Pan
            #=============================
            pan = get_servo_one()
            #ey is left?
            if ey >= 0 and ey < 180:
                if y > inputY:
                    if pan + 1 > 90 or pan + 1 < -90:
                        print("Error")
                    else:
                        pantilthat.pan(pan + 1)
                else:
                    if pan + 1 > 90 or pan + 1 < -90:
                        print("Error")
                    else:
                        pantilthat.pan(pan + 1)

            #ey is Right?
            else:
                if y > inputY:
                    if pan + 1 > 90 or pan + 1 < -90:
                        print("Error")
                    else:
                        pantilthat.pan(pan + 1)
                else:
                    if pan + 1 > 90 or pan + 1 < -90:
                        print("Error")
                    else:
                        pantilthat.pan(pan + 1)


            #=============================
            #Tilt
            #=============================
            tilt = get_servo_two()
            if ex > 90 or ex > 0:
                if x < x:
                    print("EyeInHand")
                    #Keep Centre
            else:
                if x > x:
                    print("EyeInHand")
                    #Keep Centre

        Display(x,y,z,ex,ey,ez)


    #Display Pose
    def Display(x,y,z,ex,ey,ez):
        print("===========================")
        print("|    Translation  (mm)    |")
        print("===========================")
        print("|                          ")
        print("|  X: ",x)
        print("|  Y: ",y)
        print("|  Z: ",z)
        print("|                          ")
        print("===========================")
        print("|    Rotation  (Eular)    |")
        print("===========================")
        print("|                          ")
        print("| EulX: ",ex)
        print("| EulY: ",ey)
        print("| EulZ: ",ez)
        print("|                          ")
        print("===========================")
        print("|    Press 'q' to quit    |")
        print("===========================")