
import vlc
import time

# import RPi.GPIO as GPIO


#  GPIO.setmode(GPIO.BOARD)
 
# #set GPIO Pins
# GPIO_TRIGGER = 18
# GPIO_ECHO = 24
 
# #set GPIO direction (IN / OUT)
# GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
# GPIO.setup(GPIO_ECHO, GPIO.IN)

# def distance():
#     print('Calibrating')
#     # set Trigger to HIGH
#     GPIO.output(GPIO_TRIGGER, True)
#     print('')
#     # set Trigger after 0.01ms to LOW
#     time.sleep(0.00001)
#     GPIO.output(GPIO_TRIGGER, False)
 
#     StartTime = time.time()
#     StopTime = time.time()
 
#     # save StartTime
#     while GPIO.input(GPIO_ECHO) == 0:
#         StartTime = time.time()
 
#     # save time of arrival
#     while GPIO.input(GPIO_ECHO) == 1:
#         StopTime = time.time()
 
#     # time difference between start and arrival
#     TimeElapsed = StopTime - StartTime
#     # multiply with the sonic speed (34300 cm/s)
#     # and divide by 2, because there and back
#     distance = (TimeElapsed * 34300) / 2
 
#     return distance


# creating vlc media player object
# Reset the frame to 640x480 pixels


# creating vlc media player object
media_player = vlc.MediaPlayer()
# media object
media = vlc.Media("Robotic Eye.mp4")
media1 = vlc.Media("frame.mp4")


# setting media to the media player
media_player.set_fullscreen(True)
def mediaplayerdefaultset():
        media_player.set_media(media)
        media_player.play()
        time.sleep(8)

def mediaplayerset():
        media_player.set_media(media1)
        media_player.play()
        time.sleep(3)
        media_player.stop()

while True:
       mediaplayerdefaultset()


