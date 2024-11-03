import cv2
from imutils.video import VideoStream
import imutils
import time

def person():
    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()  # Assuming camera source is 2, adjust as needed
    time.sleep(2.0)
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    person_detected = False

    try:
        while True:
            frame = vs.read()
            frame = imutils.resize(frame, width=500)  # Resize frame for faster processing (optional)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                center = x + w // 2, y + h // 2
                radius = w // 2
                frame = cv2.circle(frame, center, radius, (0, 255, 0), 3)

            if len(faces) > 0:
                print("Person Detected")
                person_detected = True
                break
            else:
                print("Person Detected")
                person_detected = False
                break

    except Exception as e:
        print(f"Exception in person(): {e}")
        # Optionally handle or log the exception here

    finally:
        vs.stop()

    return person_detected


