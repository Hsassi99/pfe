from flask import Flask, Response
import cv2

app = Flask(__name__)

# Initialize the VideoCapture object
video_capture = cv2.VideoCapture('http://192.168.137.50:5000/video_feed')

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (640, 480)) # Adjust width and height as needed

def generate_frames():
    while True:
        # Capture frame-by-frame
        success, frame = video_capture.read()
        if not success:
            break
        else:
            # Write the frame to the output video file
            out.write(frame)
            # Convert the frame to JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            # Yield the frame in byte format
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
