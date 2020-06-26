# import the necessary packages
import cv2
import datetime

# defining face detector
face_cascade=cv2.CascadeClassifier("/home/collinw99/.local/lib/python3.8/site-packages/cv2/data/haarcascade_frontalface_alt2.xml")

class FaceCamera(object):
    def __init__(self, dev, rec):
        #capturing video
        self.video = cv2.VideoCapture(dev)
        self.record = rec
        self.out = None
        self.detected = False
        self.prevDetected = False
    
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
            self.detected = True

        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (0, frame.shape[0]-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        # if chose to record and face detected
        if self.record == 1:
            if not self.prevDetected and self.detected:
                self.out = cv2.VideoWriter('./captures/' + datetime.datetime.now().strftime("%m-%d-%y:%X") + '.MOV', cv2.VideoWriter_fourcc(*'mp4v'), 25.0, (int(self.video.get(3)), int(self.video.get(4))))
                self.out.write(frame)
            elif self.prevDetected and self.detected:
                self.out.write(frame)
            elif self.prevDetected and not self.detected:
                self.out.release()
        
        # reset the detection value before returning
        self.prevDetected = self.detected
        self.detected = False

        # encode OpenCV raw frame to jpg and displaying it
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()