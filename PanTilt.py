import math

#import pantilthat

class PanTilt:

    debugEnablePanTilt = False

    #Reset To Default Posistion (Pan 0, Tilt 0)
    def reset():
        print("Reset")
        if debugEnablePanTilt:
            pantilthat.pan(0)
            pantilthat.tilt(0)

    #Eye in Hand (Follow)
    def EyeInHand(x,y,z,ex,ey,ez):
        print("EyeInHand")

        if debugEnablePanTilt:
            #=============================
            #Pan
            #=============================
            pan = get_pan()
            if pan >= -90 and pan <= 90:
                #Quadrant 1
                if ez >= 90 and ez < 0:
                    if y > inputY:
                        pantilthat.pan(pan + 1)
                    elif y < inputY:
                        pantilthat.pan(pan - 1)

                #Quadrant 2
                if ez > 180 and ez < 90:
                    if x > inputX:
                        pantilthat.pan(pan - 1)
                    elif x < inputX:
                        pantilthat.pan(pan + 1)

                #Quadrant 3
                if ez >= -90 and ez < -180:
                    if y > inputY:
                        pantilthat.pan(pan - 1)
                    elif y < inputY:
                        pantilthat.pan(pan + 1)

                #Quadrant 4
                if ez > -90 and ez <= 0:
                    if x > inputX:
                        pantilthat.pan(pan + 1)
                    elif x < inputX:
                        pantilthat.pan(pan - 1)

            else:
                pantilthat.pan(pan)


            #=============================
            #Tilt
            #=============================
            tilt = get_tilt()
            if tilt >= -90 and tilt <= 90:
                #Quadrant 1
                if ez >= 90 and ez < 0:
                    if x > inputX:
                        pantilthat.tilt(tilt + 1)
                    elif x < inputX:
                        pantilthat.tilt(tilt - 1)

                #Quadrant 2
                if ez > 180 and ez < 90:
                    if y > inputY:
                        pantilthat.tilt(tilt - 1)
                    elif y < inputY:
                        pantilthat.tilt(tilt + 1)

                #Quadrant 3
                if ez >= -90 and ez < -180:
                    if x > inputX:
                        pantilthat.tilt(tilt - 1)
                    elif x < inputX:
                        pantilthat.tilt(tilt + 1)

                #Quadrant 4
                if ez > -90 and ez <= 0:
                    if y > inputY:
                        pantilthat.tilt(tilt + 1)
                    elif y < inputY:
                        pantilthat.tilt(tilt - 1)

            else:
                pantilthat.tilt(tilt)


    #Display Pose
    def Display(x,y,z,ex,ey,ez):
        print("===========================")
        print("|    Translation  (mm)    |")
        print("===========================")
        print("|                          ")
        print("|  X (Red)  : {:4.0f}".format(x))
        print("|  Y (Green): {:4.0f}".format(y))
        print("|  Z (Blue) : {:4.0f}".format(z))
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
        print("===========================")
        print(" ")
