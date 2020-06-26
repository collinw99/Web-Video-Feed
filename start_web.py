from flask import Flask, render_template, Response, request, session
import argparse
import os

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=int, default=0, help="Video input device")
ap.add_argument("-m", "--mode", type=int, default=0, help="Detection mode: 0=none, 1=face, 2=motion")
ap.add_argument("-p", "--password", type=str, default=None, help="Set a password to protect video stream")
ap.add_argument("-a", "--min-area", type=int, default=500, help="Minimum detection area")
ap.add_argument("-r", "--record", type=int, default=0, help="Record video if motion captured")
args = vars(ap.parse_args())

app = Flask(__name__)

@app.route('/')
def index():
    if not session.get("logged_in") and args["password"] != None:
        return render_template("login.html")
    else:
        if(args["mode"] == 0):
            from camera import VideoCamera
            return Response(gen(VideoCamera(args["video"])), mimetype='multipart/x-mixed-replace; boundary=frame')
        elif(args["mode"] == 1):
            from face_detector import FaceCamera
            return Response(gen(FaceCamera(args["video"], args["record"])), mimetype='multipart/x-mixed-replace; boundary=frame')
        elif(args["mode"] == 2):
            from motion_detector import MotionCamera
            return Response(gen(MotionCamera(args["video"], args["min_area"], args["record"])), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/login', methods=['POST'])
def login():
    error = None
    if request.form['password'] == args["password"]:
        session['logged_in'] = True
        return index()
    else:
        error = "Incorrect password"
        return render_template("login.html", error=error)

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', port='3000', debug=True)