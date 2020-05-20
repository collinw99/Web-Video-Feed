# import the necessary packages
import cv2
import datetime

# defining face detector
face_cascade=cv2.CascadeClassifier("/home/collinw99/.local/lib/python3.8/site-packages/cv2/data/haarcascade_frontalface_alt2.xml")

class FaceCamera(object):
    def __init__(self, dev):
        #capturing video
        self.video = cv2.VideoCapture(dev)
    
    def __del__(self):
        #releasing camera
        self.video.release()

    def get_frame(self):
        #extracting frames
        ret, frame = self.video.read()

        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        face_rects = face_cascade.detectMultiScale(gray,1.3,5)

        for (x,y,w,h) in face_rects:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (0, frame.shape[0]-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # encode OpenCV raw frame to jpg and displaying it
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()