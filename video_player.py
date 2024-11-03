import frame_viewer as frview
import image_processor as iprocess
import time
while True:
        if iprocess.person()==True:
            frview.mediaplayerdefaultset()
            time.sleep(2)
        