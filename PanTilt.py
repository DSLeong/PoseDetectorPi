import math
import time

PanTiltEnable = True
try:
    import pantilthat
except ImportError:
    PanTiltEnable = False
    pass

class PanTilt:

    #Reset To Default Posistion (Pan 0, Tilt 0)
    def reset():
        print("Reset")
        if PanTiltEnable:
            pantilthat.pan(0)
            pantilthat.tilt(0)

    #Eye in Hand (Follow)
    def EyeInHand(x,y,z,ex,ey,ez,inputX,inputY,inputZ):
        print("EyeInHand")

        if PanTiltEnable:
            #=============================
            #Pan
            #=============================
            pan = pantilthat.get_pan()
            if pan > -90 and pan < 90:
                #Quadrant 1
                if ez > 0 and ez <= 90:
                    if y > inputY:
                        pantilthat.pan(pan + 1)
                    elif y < inputY:
                        pantilthat.pan(pan - 1)

                #Quadrant 2
                elif ez > 90 and ez < 180:
                    if x > inputX:
                        pantilthat.pan(pan - 1)
                        time.sleep(0.005)
                    elif x < inputX:
                        pantilthat.pan(pan + 1)

                #Quadrant 3
                elif ez > -180 and ez <= -90:
                    if y > inputY:
                        pantilthat.pan(pan - 1)
                    elif y < inputY:
                        pantilthat.pan(pan + 1)

                #Quadrant 4
                elif ez > -90 and ez <= 0:
                    if x > inputX:
                        pantilthat.pan(pan + 1)
                    elif x < inputX:
                        pantilthat.pan(pan - 1)

            else:
                pantilthat.pan(pan)
            
            time.sleep(0.005)


            #=============================
            #Tilt
            #=============================
            tilt = pantilthat.get_tilt()
            if tilt > -90 and tilt < 90:
                #Quadrant 1
                if ez > 0 and ez <= 90:
                    if x > inputX:
                        pantilthat.tilt(tilt + 1)
                    elif x < inputX:
                        pantilthat.tilt(tilt - 1)

                #Quadrant 2
                elif ez > 90 and ez < 180:
                    if y > inputY:
                        pantilthat.tilt(tilt - 1)
                    elif y < inputY:
                        pantilthat.tilt(tilt + 1)

                #Quadrant 3
                elif ez > -180 and ez <= -90:
                    if x > inputX:
                        pantilthat.tilt(tilt - 1)
                    elif x < inputX:
                        pantilthat.tilt(tilt + 1)

                #Quadrant 4
                elif ez > -90 and ez <= 0:
                    if y > inputY:
                        pantilthat.tilt(tilt + 1)
                    elif y < inputY:
                        pantilthat.tilt(tilt - 1)

            else:
                pantilthat.tilt(tilt)
            
            time.sleep(0.005)
