from flask import Flask, render_template, Response
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=int, default=0, help="Video input device")
ap.add_argument("-m", "--mode", type=int, default=0, help="Detection mode: 0->none, 1->face, 2->motion")
ap.add_argument("-a", "--min-area", type=int, default=500, help="Minimum detection area")
args = vars(ap.parse_args())

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    if(args["mode"] == 0):
        from camera import VideoCamera
        return Response(gen(VideoCamera(args["video"])), mimetype='multipart/x-mixed-replace; boundary=frame')
    elif(args["mode"] == 1):
        from face_detector import FaceCamera
        return Response(gen(FaceCamera(args["video"])), mimetype='multipart/x-mixed-replace; boundary=frame')
    elif(args["mode"] == 2):
        from motion_detector import MotionCamera
        return Response(gen(MotionCamera(args["video"], args["min_area"])), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='3000', debug=True)