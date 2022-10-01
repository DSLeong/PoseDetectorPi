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
    def EyeInHand(x, y, z, ex, ey, ez, inputEX, inputEY, inputEZ):
        print("EyeInHand")

        #TESTING STILL NEEDED

        if PanTiltEnable:
            pan = pantilthat.get_pan()
            if pan > -90 and pan < 90:
                if ey > inputEY:
                    pantilthat.pan(pan + 1)
                elif ey < inputEY:
                    pantilthat.pan(pan - 1)
            else:
                pantilthat.pan(pan)
            
            time.sleep(0.005)

            #=============================
            #Tilt
            #=============================
            tilt = pantilthat.get_tilt()
            if tilt > -90 and tilt < 90:
                if ex > inputEX:
                    pantilthat.tilt(tilt + 1)
                elif ex < inputEX:
                    pantilthat.tilt(tilt - 1)
            else:
                pantilthat.tilt(tilt)
            
            time.sleep(0.005)
