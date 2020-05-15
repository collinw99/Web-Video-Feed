# import the necessary packages
import cv2
import datetime

# defining face detector
face_cascade=cv2.CascadeClassifier("/home/collinw99/.local/lib/python3.8/site-packages/cv2/data/haarcascade_frontalface_alt2.xml")
ds_factor=0.6
class VideoCamera(object):
    def __init__(self):
        #capturing video
        self.video = cv2.VideoCapture(2)
    
    def __del__(self):
        #releasing camera
        self.video.release()

    def get_frame(self):
        #extracting frames
        ret, frame = self.video.read()

        height = frame.shape[0]
        width = frame.shape[1]

        # gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        # face_rects = face_cascade.detectMultiScale(gray,1.3,5)

        # for (x,y,w,h) in face_rects:
        #     cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

        frame = cv2.putText(frame, str(datetime.datetime.now()), (0, height-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # encode OpenCV raw frame to jpg and displaying it
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()