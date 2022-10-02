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
    def EyeInHand(x, y, z, ex, ey, ez, inputX, inputY, inputZ):
        print("EyeInHand")

        if x < 0: x += 360
        if y < 0: y += 360
        if inputX < 0: inputX += 360
        if inputY < 0: inputY += 360

        if PanTiltEnable:
            #=============================
            #Pan (Vertical)
            # up = pan decrease
            # down = pan incease
            #=============================
            pan = pantilthat.get_pan()
            if pan > -90 and pan < 90:
                if x > inputX:
                    pantilthat.pan(pan + 1)
                elif x < inputX:
                    pantilthat.pan(pan - 1)
            else:
                 pantilthat.pan(pan)
            
            time.sleep(0.005)

            #=============================
            #Tilt (Horizontal)
            # left = tilt decrease
            # right = tilt incease
            #=============================
            tilt = pantilthat.get_tilt()
            if tilt > -90 and tilt < 90:
                if y > inputY:
                    pantilthat.tilt(tilt + 1)
                elif y < inputY:
                    pantilthat.tilt(tilt - 1)
            else:
                pantilthat.tilt(tilt)
            
            time.sleep(0.005)
