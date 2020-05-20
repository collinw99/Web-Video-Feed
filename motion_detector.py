# import the necessary packages
import cv2
import imutils
import datetime
import time

class MotionCamera(object):
    def __init__(self, dev, minArea, rec):
        #capturing video
        self.video = cv2.VideoCapture(dev)
        self.out = None
        self.record = rec
        self.firstFrame = None
        self.minArea = minArea
        self.prevText = "Unoccupied"
    
    def __del__(self):
        #releasing camera
        self.video.release()

    def get_frame(self):
        #extracting frames
        ret, frame = self.video.read()

        # initially, the frame will be 'unoccupied'
        text = "Unoccupied"

        # get the grayscale frame and apply a blur to reduce false positives
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # initialize the first frame
        if self.firstFrame is None:
            self.firstFrame = gray
            time.sleep(5)

        # get the difference between first frame and current frame
        frameDelta = cv2.absdiff(self.firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

        # dilate the thresholded image to fill in holes, then find contours on it
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        # loop over contours
        for c in cnts:
            # if contour is too small, ignore it
            if cv2.contourArea(c) < self.minArea:
                continue

            # put bounding box around contours
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            text = "Occupied"

        # if chose to record video of movement
        if self.record == 1:
            # statements to start/stop recording
            if self.prevText == "Unoccupied" and text == "Occupied":
                self.out = cv2.VideoWriter('./captures/' + datetime.datetime.now().strftime("%m-%d-%y:%X") + '.MOV', cv2.VideoWriter_fourcc(*'mp4v'), 25.0, (int(self.video.get(3)), int(self.video.get(4))))
                self.out.write(frame)
            elif self.prevText == "Occupied" and text == "Occupied":
                self.out.write(frame)
            elif self.prevText == "Occupied" and text == "Unoccupied":
                self.out.release()
        
        # put text and timestamp on frame
        cv2.putText(frame, "Room Status: {}".format(text), (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (0, frame.shape[0]-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # set the previous text to the current text before returning
        self.prevText = text

        # encode OpenCV raw frame to jpg and displaying it
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()